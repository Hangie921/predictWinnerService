import time
from datetime import datetime
import pytz
import json
from types import SimpleNamespace

from .mlb_class import Filter
from .mlb_class import PitcherWinning
from .mlb_class import Winning
from .mlb_class import Team
from .mlb_class import Pitcher
from .mlb_class import Match
from .mlb_class import STRK
from .mlb_class import Game_status


import bs4
import requests

# from selenium import webdriver

# driver = webdriver.Chrome()

# TODO
# 1. check >.500
# 2. check 1 run game
# 3. compare starter and l, r winning
# 4. bullpen AVG ERA


rank_pos = [0, 1, 2, 3, 4]

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0",
}

today_match = []


advanced_split_url = "https://www.mlb.com/standings/advanced-splits"
standings_split_url = "https://www.mlb.com/standings"
propable_pitchers_url = "https://www.mlb.com/probable-pitchers/"
bullpen_stats_url = (
    "https://www.covers.com/sport/baseball/mlb/statistics/team-bullpenera/2022"
)

# If the date of the standing API is newer than current time
# the API will response the current standings.
standings_api_url = "https://statsapi.mlb.com/api/v1/standings?leagueId=103,104&standingsTypes=regularSeason&season="

history_standings_api_url = "https://statsapi.mlb.com/api/v1/schedule?sportId=1&leagueId=103,104&hydrate=team,linescore,flags,liveLookin,review&useLatestGames=false&language=en&date="
history_standings_api_url_with_date = "https://statsapi.mlb.com/api/v1/schedule?sportId=1&leagueId=103,104&hydrate=team,linescore,flags,liveLookin,review&useLatestGames=false&language=en&date=2024-08-30"


def getStandingAPIURL(year, date):
    return standings_api_url+year+"&date="+date

def QueryDataFromRequest(url):
    with requests.Session() as rq:
        rq.headers.update(headers)
        r = rq.get(url, verify=False).text
        return r


# def QueryDataFromSelenium(url):
#     driver.get(url)
#     time.sleep(3)
#     return driver.page_source

def check_is_predicting_next(et_date:str):
    now = datetime.now()
    target_date = datetime.strptime(et_date, "%Y-%m-%d")
    is_predict_next = False

    if now.date() == target_date.date() and now.hour >= 4:
        is_predict_next = True
    print("[crawl] is_predicting_next:", is_predict_next)
    return is_predict_next

# 包裝函式, 此函式應該要為傳 ET 日期的當天(預測隔天）或是之前(回測）的日期
# AWS 的 server 開在 亞洲，所以應該要考慮亞洲時間跟美洲時間的轉換
et_timezone = pytz.timezone("US/Eastern")
def GetContent(format, filter_items, et_date_string):
    is_predicting_next_game = check_is_predicting_next(et_date_string)
    
    target_content_date = datetime.strptime(et_date_string, "%Y-%m-%d")
    target_content_year = target_content_date.strftime("%Y")

    utc_now = datetime.now(pytz.UTC)
    print("utc_now.tzinfo   =", utc_now.astimezone().tzinfo)
    print("utc_now.hour =",utc_now.hour)

    et_now = utc_now.astimezone(et_timezone)

    if "diff" not in filter_items:
        return "filter required"
    print("is_predicting_next_game (ET) ", is_predicting_next_game)
    print("(ET) now is  ", et_now)    

    # current_year = et_now.strftime("%Y")
    # current_date = et_now.strftime("%Y-%m-%d")
    r = QueryDataFromRequest(propable_pitchers_url + target_content_date.strftime("%Y-%m-%d"))
    # bull_pen_root = rq.get(bullpen_stats_url, verify=False).text
    # print(bull_pen_root)
    data = QueryDataFromRequest(getStandingAPIURL(target_content_year, target_content_date.strftime("%Y-%m-%d")))
    standings = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
    match_root = bs4.BeautifulSoup(r, "html.parser")
    match_container = match_root.find(class_="probable-pitchers__container")
    matches = match_container.find_all(class_="probable-pitchers__matchup")

    final_matches = []
    history = {}
    history_standings = {}
    if is_predicting_next_game is False:
        history = QueryDataFromRequest(history_standings_api_url + target_content_date.strftime("%Y-%m-%d"))
        tmp = json.loads(history, object_hook=lambda d: SimpleNamespace(**d))
        if len(tmp.dates) > 0 :
            history_standings = tmp.dates[0]
    for match in matches:
        names = match.find(class_="probable-pitchers__game")
        away_team = Team(
            match.find(class_="probable-pitchers__team-name--away").get_text().strip(),
            names["data-team-id-away"],
        )
        home_team = Team(
            match.find(class_="probable-pitchers__team-name--home").get_text().strip(),
            names["data-team-id-home"],
        )
        game_id = match.attrs["data-gamepk"]
        f = Filter()
        f.item = filter_items
        m = Match(game_id, home_team, away_team, f, et_date_string)
        starters = match.find_all(class_="probable-pitchers__pitcher-summary")
        starter_index = 0
        for starter in starters:
            id = "none"
            name = "TBD"
            url = "non"
            handed = "non"
            win = "0"
            loss = "0"
            era = "0.00"
            so = "0"
            if (
                starter.find(class_="probable-pitchers__pitcher-name")
                .get_text()
                .strip()
                != "TBD"
            ):
                name = (
                    starter.find(class_="probable-pitchers__pitcher-name-link")
                    .get_text()
                    .strip()
                )
                url = (
                    "https://www.mlb.com"
                    + starter.find(class_="probable-pitchers__pitcher-name-link").attrs[
                        "href"
                    ]
                )
                tmp = url.split("-")
                id = tmp[len(tmp)-1]
                handed = (
                    starter.find(class_="probable-pitchers__pitcher-pitch-hand")
                    .get_text()
                    .strip()
                )
                win = (
                    starter.find(class_="probable-pitchers__pitcher-wins")
                    .get_text()
                    .strip()
                )
                loss = (
                    starter.find(class_="probable-pitchers__pitcher-losses")
                    .get_text()
                    .strip()
                )
                era = (
                    starter.find(class_="probable-pitchers__pitcher-era")
                    .get_text()
                    .strip("ERA")
                    .strip()
                )
                so = (
                    starter.find(class_="probable-pitchers__pitcher-so")
                    .get_text()
                    .strip(" SO")
                    .strip()
                )
            p_winning = PitcherWinning(win, loss)
            s = Pitcher(name, handed, p_winning, era, so, url, id)
            if starter_index == 0:
                m.away_team.set_starter(s)
            else:
                m.home_team.set_starter(s)

            for record in standings.records:
                for tr in record.teamRecords:
                    target_team = Team("tmp", "0")
                    if m.away_team.name in tr.team.name or (
                        m.away_team.name == "D-backs"
                        and tr.team.name == "Arizona Diamondbacks"
                    ):
                        target_team = m.away_team
                    elif m.home_team.name in tr.team.name or (
                        m.home_team.name == "D-backs"
                        and tr.team.name == "Arizona Diamondbacks"
                    ):
                        target_team = m.home_team
                    strek = STRK(tr.streak.streakType == "wins", tr.streak.streakNumber)
                    target_team.set_streak(strek)
                    target_team.set_diff(tr.runDifferential)
                    overall = Winning(
                        tr.leagueRecord.wins,
                        tr.leagueRecord.losses,
                        tr.leagueRecord.pct,
                    )
                    target_team.set_overall_winning(overall)
                    for r in tr.records.splitRecords:
                        if r.type == "lastTen":
                            w = Winning(r.wins, r.losses, r.pct)
                            target_team.set_l10(w)
                        if r.type == "right":
                            w = Winning(r.wins, r.losses, r.pct)
                            target_team.set_vs_r_winning(w)
                        if r.type == "left":
                            w = Winning(r.wins, r.losses, r.pct)
                            target_team.set_vs_l_winning(w)
                        if r.type == "home":
                            w = Winning(r.wins, r.losses, r.pct)
                            target_team.set_home_winning(w)
                        if r.type == "away":
                            w = Winning(r.wins, r.losses, r.pct)
                            target_team.set_away_winning(w)
                        if r.type == "leftHome":
                            w = Winning(r.wins, r.losses, r.pct)
                            target_team.set_vs_l_home_winning(w)
                        if r.type == "rightHome":
                            w = Winning(r.wins, r.losses, r.pct)
                            target_team.set_vs_r_home_winning(w)
                        if r.type == "leftAway":
                            w = Winning(r.wins, r.losses, r.pct)
                            target_team.set_vs_l_away_winning(w)
                        if r.type == "rightAway":
                            w = Winning(r.wins, r.losses, r.pct)
                            target_team.set_vs_r_away_winning(w)
                    if m.away_team.name in tr.team.name or (
                        m.away_team.name == "D-backs"
                        and tr.team.name == "Arizona Diamondbacks"
                    ):
                        m.away_team = target_team
                    elif m.home_team.name in tr.team.name or (
                        m.home_team.name == "D-backs"
                        and tr.team.name == "Arizona Diamondbacks"
                    ):
                        m.home_team = target_team
            if is_predicting_next_game is False:
                print("predicting next game is [FALSE]")
                for game in history_standings.games:
                    if m.id == str(game.gamePk):
                        status = Game_status(game.status.detailedState)
                        m.status = status
                        if m.status.detailed_state == "Postponed":
                            continue
                        if game.teams.away.isWinner is True:
                            m.is_winner_home_team = False
                            m.winner_team = game.teams.away.team.teamName
                            m.loser_team = game.teams.home.team.teamName
                            m.winner_team_id = game.teams.away.team.id
                            m.loser_team_id = game.teams.home.team.id
                        else:
                            m.is_winner_home_team = True
                            m.winner_team = game.teams.home.team.teamName
                            m.loser_team = game.teams.away.team.teamName
                            m.winner_team_id = game.teams.home.team.id
                            m.loser_team_id = game.teams.away.team.id
            starter_index += 1
        if hasattr(m.status, "detailed_state") is False or m.status.detailed_state != "Postponed":
            # m.compare_all_item()
            final_matches.append(m)
        print("match s ", m)
    final_matches.sort(key=sortMatch, reverse=True)
    count = 1
    ret_string = []

    print("This season is", target_content_year)
    print("is_predicting_next_game (ET) ", is_predicting_next_game)
    print("(ET) now is  ", et_now)    
    print("et_date_string    =", et_date_string)


    if format == "object":
        return final_matches
    elif format == "json":
        return json.dumps(final_matches, default=lambda o: o.encode(), indent=4)
    elif format == "result":
        for m in final_matches:
            a = "No.{}".format(count)
            ret_string.append(a)
            ret_string.append(m.print_stats(is_predicting_next_game))
            ret_string.append("\n")
            count += 1
        return "\n".join(ret_string)


def sortMatch(ele):
    return ele.winning_point_diff
