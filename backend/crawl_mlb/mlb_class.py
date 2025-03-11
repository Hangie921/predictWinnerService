import datetime
"""mlb_class is the module that contains all class from MLB.com"""

# const
DIFF_WIN_POINT_WEIGHTS = 1.5
L10_WIN_POINT_WEIGHTS = 1.1
GENERAL_WEIGHTS = 1


spring_training_start_date_2024 = "2024-02-23"
spring_training_end_date_2024= "2024-03-26"
spring_training_start_date_2024 = "2025-02-21"
spring_training_end_date_2024= "2025-03-26"

regular_season_start_date_2024 = "2024-03-20"
regular_season_end_date_2024= "2024-09-30"
regular_season_start_date_2025 = "2025-03-18"
regular_season_end_date_2025= "2024-09-30"


class GameDate():
    def __init__(self, start:str, end:str):
        self.start_date = start
        self.end_date = end
    
    def get_start_date(self):
        return datetime.datetime.strptime(self.start_date, "%Y-%m-%d")
    
    def get_end_date(self):
        return datetime.datetime.strptime(self.end_date, "%Y-%m-%d")

def fill_string(target: str, which: str, length: int):
    while len(target) <= length:
        target = target + which
    return target

class Game_status():
    def __init__(self, detail:str):
        self.detailed_state = detail

class Winning:
    def encode(self):
        return self.__dict__

    def __init__(self, win: int, loss: int, pct: str):
        self.win = win
        self.loss = loss
        self.pct = pct

    def get_stat(self):
        a = "{}-{}".format(self.win, self.loss)
        a = fill_string(a, " ", 7)
        return "{}{}".format(a, self.pct)


def compare_and_get_result(home_winning: Winning, away_winning: Winning):
    if home_winning.pct > away_winning.pct:
        return "home team"
    if home_winning.pct == away_winning.pct:
        return "equal    "
    return "away team"


class Filter:
    """Filter is used to define what field is used to sort the power rank"""

    def encode(self):
        return self.__dict__

    def __init__(self):
        self.item = {
            "overall": True,
            "home_or_away": True,
            "handed": True,
            "l10": True,
            "streak": True,
            "diff": True,
        }


class PitcherWinning:
    """PicherWinner is the class to show winning"""

    def encode(self):
        return self.__dict__

    def __init__(self, win: str, loss: str):
        self.win = int(win)
        self.loss = int(loss)

    def get_stat(self):
        return "{}-{}".format(self.win, self.loss)


class STRK:
    """STRK parse the winning or losing streak"""

    def encode(self):
        return self.__dict__

    def __init__(self, is_win: bool, streak_num: str):
        self.is_win = is_win
        self.streak_num = streak_num
        if self.is_win:
            self.steak_code = "W" + self.streak_num.__str__()
        else:
            self.steak_code = "L" + str(self.streak_num).__str__()


class Team:
    """Team parse the whole information of a team"""

    def encode(self):
        return self.__dict__

    def __init__(self, name: str, team_id: str):
        self.name = name
        self.win_points = 0
        self.handed_winning = Winning(0, 0, ".000")
        self.id = team_id
        self.overall_winning = {}
        self.home_winning = {}
        self.away_winning = {}
        self.vs_r_winning = {}
        self.vs_l_winning = {}
        self.vs_better_than_500_winning = {}
        self.vs_r_home_winning = {}
        self.vs_l_home_winning = {}
        self.vs_r_away_winning = {}
        self.vs_l_away_winning = {}
        self.diff = {}
        self.l10 = {}
        self.streak = {}
        self.starter = {}
        self.bull_pen_era = {}

    def set_overall_winning(self, winning: Winning):
        self.overall_winning = winning

    def set_home_winning(self, winning: Winning):
        self.home_winning = winning

    def set_away_winning(self, winning: Winning):
        self.away_winning = winning

    def set_vs_r_winning(self, winning: Winning):
        self.vs_r_winning = winning

    def set_vs_l_winning(self, winning: Winning):
        self.vs_l_winning = winning

    def set_vs_better_than_500_winning(self, winning: Winning):
        self.vs_better_than_500_winning = winning

    def set_vs_r_home_winning(self, winning: Winning):
        self.vs_r_home_winning = winning

    def set_vs_r_away_winning(self, winning: Winning):
        self.vs_r_away_winning = winning

    def set_vs_l_home_winning(self, winning: Winning):
        self.vs_l_home_winning = winning

    def set_vs_l_away_winning(self, winning: Winning):
        self.vs_l_away_winning = winning

    def set_diff(self, diff: int):
        self.diff = diff

    def set_l10(self, l10: Winning):
        self.l10 = l10

    def set_streak(self, streak: STRK):
        self.streak = streak

    def set_starter(self, starter):
        self.starter = starter

    def set_bullpen_era(self, era: str):
        self.bull_pen_era = era


class Match:
    def encode(self):
        return self.__dict__

    def __init__(self, match_id: str, home_team: Team, away_team: Team, f: Filter, date: str):
        self.id = match_id
        self.home_team = home_team
        self.away_team = away_team
        self.winning_point_diff = -1
        self.filter = f
        self.winner_team = ""
        self.loser_team = ""
        self.winner_team_id = ""
        self.loser_team_id = ""
        self.is_winner_home_team = False
        self.date = date
        self.status = {}

    def set_status(self, status: Game_status):
        self.status = status

    def compare_all_item(self):
        # diff
        print("compare_all_item", self.status)
        if self.filter.item["diff"]:
            if self.home_team.diff > self.away_team.diff:
                self.home_team.win_points += DIFF_WIN_POINT_WEIGHTS
            elif self.away_team.diff > self.home_team.diff:
                self.away_team.win_points += DIFF_WIN_POINT_WEIGHTS
        # l10
        if self.filter.item["l10"]:
            if self.home_team.l10.pct > self.away_team.l10.pct:
                self.home_team.win_points += L10_WIN_POINT_WEIGHTS
            elif self.away_team.l10.pct > self.home_team.l10.pct:
                self.away_team.win_points += L10_WIN_POINT_WEIGHTS
        # home/away winning
        if self.filter.item["home_or_away"]:
            if self.home_team.home_winning.pct > self.away_team.away_winning.pct:
                self.home_team.win_points += float(
                    self.home_team.home_winning.pct
                ) - float(self.away_team.away_winning.pct)
            if self.away_team.away_winning.pct > self.home_team.home_winning.pct:
                self.away_team.win_points += float(
                    self.away_team.away_winning.pct
                ) - float(self.home_team.home_winning.pct)

        # pitcher handed winning
        if self.filter.item["handed"]:
            if (
                self.home_team.starter.handed == "RHP"
                and self.away_team.starter.handed == "RHP"
            ):
                self.home_team.handed_winning = self.home_team.vs_r_winning
                self.away_team.handed_winning = self.away_team.vs_r_winning
                if self.home_team.vs_r_winning.pct > self.away_team.vs_r_winning.pct:
                    self.home_team.win_points += float(
                        self.home_team.vs_r_winning.pct
                    ) - float(self.away_team.vs_r_winning.pct)
                elif self.away_team.vs_r_winning.pct > self.home_team.vs_r_winning.pct:
                    self.away_team.win_points += float(
                        self.away_team.vs_r_winning.pct
                    ) - float(self.home_team.vs_r_winning.pct)
            elif (
                self.home_team.starter.handed == "LHP"
                and self.away_team.starter.handed == "LHP"
            ):
                self.home_team.handed_winning = self.home_team.vs_l_winning
                self.away_team.handed_winning = self.away_team.vs_l_winning
                if self.home_team.vs_l_winning.pct > self.away_team.vs_l_winning.pct:
                    self.home_team.win_points += float(
                        self.home_team.vs_l_winning.pct
                    ) - float(self.away_team.vs_l_winning.pct)
                elif self.away_team.vs_l_winning.pct > self.home_team.vs_l_winning.pct:
                    self.away_team.win_points += float(
                        self.away_team.vs_l_winning.pct
                    ) - float(self.home_team.vs_l_winning.pct)
            elif (
                self.home_team.starter.handed == "RHP"
                and self.away_team.starter.handed == "LHP"
            ):
                self.home_team.handed_winning = self.home_team.vs_l_winning
                self.away_team.handed_winning = self.away_team.vs_r_winning
                if self.home_team.vs_l_winning.pct > self.away_team.vs_r_winning.pct:
                    self.home_team.win_points += float(
                        self.home_team.vs_l_winning.pct
                    ) - float(self.away_team.vs_r_winning.pct)
                elif self.away_team.vs_r_winning.pct > self.home_team.vs_l_winning.pct:
                    self.away_team.win_points += float(
                        self.away_team.vs_r_winning.pct
                    ) - float(self.home_team.vs_l_winning.pct)
            elif (
                self.home_team.starter.handed == "LHP"
                and self.away_team.starter.handed == "RHP"
            ):
                self.home_team.handed_winning = self.home_team.vs_r_winning
                self.away_team.handed_winning = self.away_team.vs_l_winning
                if self.home_team.vs_r_winning.pct > self.away_team.vs_l_winning.pct:
                    self.home_team.win_points += float(
                        self.home_team.vs_r_winning.pct
                    ) - float(self.away_team.vs_l_winning.pct)
                elif self.away_team.vs_l_winning.pct > self.home_team.vs_r_winning.pct:
                    self.away_team.win_points += float(
                        self.away_team.vs_l_winning.pct
                    ) - float(self.home_team.vs_r_winning.pct)
        # overall winning
        if self.filter.item["overall"]:
            if self.home_team.overall_winning.pct > self.away_team.overall_winning.pct:
                self.home_team.win_points += float(
                    self.home_team.overall_winning.pct
                ) - float(self.away_team.overall_winning.pct)
            if self.away_team.overall_winning.pct > self.home_team.overall_winning.pct:
                self.away_team.win_points += float(
                    self.away_team.overall_winning.pct
                ) - float(self.home_team.overall_winning.pct)
        if self.home_team.win_points > self.away_team.win_points:
            self.winning_point_diff = (
                self.home_team.win_points - self.away_team.win_points
            )
        else:
            self.winning_point_diff = (
                self.away_team.win_points - self.home_team.win_points
            )
        # self.away_team.win_points

    def append(self, pool, target):
        pool.append(target)

    def print_stats(self, is_current: bool):
        ret_string = []
        tmp = "+++++++++++++++++++++++++++++++++++++++++++++++++"
        self.append(ret_string, tmp)
        tmp = "Match ID: "+self.id
        self.append(ret_string, tmp)
        # tmp = f"Winner is home team {self.is_winner_home_team}"
        # self.append(ret_string, tmp)
        # tmp = f"Winner is  {self.winner_team}"
        # self.append(ret_string, tmp)
        # tmp = f"Loser is  {self.loser_team}"
        # self.append(ret_string, tmp)
        tmp = fill_string(
            f"Home: ({self.home_team.id}) {self.home_team.name}  ", " ", 21
        ) + str(self.home_team.win_points)
        self.append(ret_string, tmp)
        tmp = fill_string(
            f"Away: ({self.away_team.id}) {self.away_team.name}  ", " ", 21
        ) + str(self.away_team.win_points)
        self.append(ret_string, tmp)
        tmp = "+++++++++++++++++++++++++++++++++++++++++++++++++"
        self.append(ret_string, tmp)
        tmp = (
            fill_string(f"Home Starter: {self.home_team.starter.name} ({self.home_team.starter.id})", " ", 40)
            + f" {self.home_team.starter.handed} {self.home_team.starter.winning.get_stat()} {self.home_team.starter.era} {self.home_team.starter.so}SO"
        )
        self.append(ret_string, tmp)
        tmp = (
            fill_string(f"Away Starter: {self.away_team.starter.name} ({self.away_team.starter.id})", " ", 40)
            + f" {self.away_team.starter.handed} {self.away_team.starter.winning.get_stat()} {self.away_team.starter.era} {self.away_team.starter.so}SO"
        )
        self.append(ret_string, tmp)
        self.append(ret_string, "")
        self.append(ret_string, "Item\t\t Home Team\t Away Team\t Compare")
        if self.filter.item["overall"]:
            tmp = (
                "Overall\t\t "
                + self.home_team.overall_winning.get_stat()
                + "\t "
                + self.away_team.overall_winning.get_stat()
                + "\t "
                + compare_and_get_result(
                    self.home_team.overall_winning, self.away_team.overall_winning
                )
            )
            self.append(ret_string, tmp)
        if self.filter.item["home_or_away"]:
            tmp = (
                "Home/Away\t "
                + self.home_team.home_winning.get_stat()
                + "\t "
                + self.away_team.away_winning.get_stat()
                + "\t "
                + compare_and_get_result(
                    self.home_team.home_winning, self.away_team.away_winning
                )
            )
            self.append(ret_string, tmp)
        if self.filter.item["handed"]:
            tmp = (
                "Handed\t\t "
                + self.home_team.handed_winning.get_stat()
                + "\t "
                + self.away_team.handed_winning.get_stat()
                + "\t "
                + compare_and_get_result(
                    self.home_team.handed_winning, self.away_team.handed_winning
                )
            )
            self.append(ret_string, tmp)
        if self.filter.item["l10"]:
            tmp = (
                "l10\t\t "
                + self.home_team.l10.get_stat()
                + "\t "
                + self.away_team.l10.get_stat()
            )
            self.append(ret_string, tmp)
        if self.filter.item["streak"]:
            tmp = (
                "Streak\t\t "
                + self.home_team.streak.steak_code
                + "\t\t "
                + self.away_team.streak.steak_code
            )
            self.append(ret_string, tmp)
        if self.filter.item["diff"]:
            tmp = (
                "Diff\t\t "
                + str(self.home_team.diff)
                + "\t\t "
                + str(self.away_team.diff)
            )
            self.append(ret_string, tmp)
        if is_current is False:
            tmp = "Winner\t\t "
            if self.is_winner_home_team:
                tmp += "True\t\t False"
            else:
                tmp += "False\t\t True"
            self.append(ret_string, tmp)
        self.append(ret_string, "=================================================")
        return "\n".join(ret_string)


class Pitcher:
    """Starter is the data of the starting pitcher"""

    def encode(self):
        return self.__dict__

    def __init__(
        self, name: str, handed: str, winning: PitcherWinning, era, so: int, url: str, id: str
    ):
        self.id = id
        self.name = name
        self.handed = handed
        self.winning = winning
        self.era = era
        self.so = so
        self.url = url
