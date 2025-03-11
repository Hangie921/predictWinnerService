from django.shortcuts import render
from rest_framework import generics
from django.contrib.auth.models import User
from .models import Weight, Game, Team, TeamStat, Pitcher, PitcherStat
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import UserSerializer,WeightSerializer,GameSerializer
from django.http import JsonResponse, HttpResponse
from . import const 
from crawl_mlb import execution

def calculate_power(home_team, away_team, home_starter, away_starter, diff_weight, home_away_weight, handed_weight, overall_weight, l10_weight):
    home_power = 0
    away_power = 0
    # diff
    if home_team.diff > away_team.diff:
        home_power += float(diff_weight)
    elif home_team.diff < away_team.diff:
        away_power += float(diff_weight)

    # home_away
    home_home_away_winning =  home_team.home_wins/(home_team.home_wins+home_team.home_losses)
    away_home_away_winning =  away_team.away_wins/(away_team.away_wins+away_team.away_losses)
    if home_home_away_winning > away_home_away_winning:
        home_power += (home_home_away_winning-away_home_away_winning)*float(home_away_weight)
    elif home_home_away_winning < away_home_away_winning:
        away_power += (away_home_away_winning-home_home_away_winning)*float(home_away_weight)
    
    # handed
    home_handed_winning = 0
    away_handed_winning = 0 
    if home_starter.handed is "LHP":
        away_handed_winning = away_team.left_handed_wins/(away_team.left_handed_wins+away_team.left_handed_losses)
    else:
        away_handed_winning = away_team.right_handed_wins/(away_team.right_handed_wins+away_team.right_handed_losses)
    if away_starter.handed is "LHP":
        home_handed_winning = home_team.left_handed_wins/(home_team.left_handed_wins+home_team.left_handed_losses)
    else:
        home_handed_winning = home_team.right_handed_wins/(home_team.right_handed_wins+home_team.right_handed_losses)

    if home_handed_winning > away_handed_winning:
        home_power += (home_handed_winning-away_handed_winning)*float(handed_weight)
    elif home_handed_winning < away_handed_winning:
        away_power += (away_handed_winning-home_handed_winning)*float(handed_weight)

    # overall
    home_team_overall_winning = home_team.overall_wins/(home_team.overall_wins+home_team.overall_losses)
    away_team_overall_winning = away_team.overall_wins/(away_team.overall_wins+away_team.overall_losses)
    if home_team_overall_winning > away_team_overall_winning:
        home_power += (home_team_overall_winning-away_team_overall_winning)*float(overall_weight)
    elif home_team_overall_winning < away_team_overall_winning:
        away_power += (away_team_overall_winning-home_team_overall_winning)*float(overall_weight)

    # last 10
    home_team_last_10_winning = home_team.last_10_wins/(home_team.last_10_wins+home_team.last_10_losses)
    away_team_last_10_winning = away_team.last_10_wins/(away_team.last_10_wins+away_team.last_10_losses)
    if home_team_last_10_winning > away_team_last_10_winning:
        home_power += (home_team_last_10_winning-away_team_last_10_winning)*float(l10_weight)
    elif home_team_last_10_winning < away_team_last_10_winning:
        away_power += (away_team_last_10_winning-home_team_last_10_winning)*float(l10_weight)
    
    

    return home_power, away_power

def compare_power(ele):
    return ele["_winningPointDiff"]

def get_supported_date(request):
    ret = [{
        "year": 2024,
        "type": "regularSeason",
        "startDate": "2024-03-20",
        "endDate": "2024-09-30",
    }]
    return JsonResponse(ret, safe=False)


def get_prediction(request):
    # prediction?date=2024-08-01&diff_weight=1.5&l10_weight=1.4&home_away_weight=1.3&handed_weight=1.2&overall_weight=0.1
    if request.META["REQUEST_METHOD"] == "GET":
        print("request is", request.GET)
        print("diff_weight is", request.GET.get('diff_weight'))
        print("l10_weight is", request.GET.get('l_10_weight'))
        print("home_away_weight is", request.GET.get('home_away_weight'))
        print("handed_weight is", request.GET.get('handed_weight'))
        print("overall_weight is", request.GET.get('overall_weight'))
        print("date is", request.GET.get('date'))
        games = Game.objects.filter(game_date=request.GET.get('date'))
        
        if len(games) == 0:
            execution.fetch_data_to_db(request.GET.get('date'))
            games = Game.objects.filter(game_date=request.GET.get('date'))
            if len(games) == 0:
                return JsonResponse({"message": "No games data for this date yet"})

        detailed_games = []
        for game in games:
            # Get team stats
            
            home_team_stats = TeamStat.objects.filter(t_id=game.home_team_id, stat_date=request.GET.get('date')).first()
            away_team_stats = TeamStat.objects.filter(t_id=game.away_team_id, stat_date=request.GET.get('date')).first()
            home_team = Team.objects.filter(t_id=game.home_team_id).first()
            away_team = Team.objects.filter(t_id=game.away_team_id).first()
            
            # Get starting pitchers stats
            home_starter_stats = PitcherStat.objects.filter(p_id=game.home_starter_id, stat_date=request.GET.get('date')).first()
            away_starter_stats = PitcherStat.objects.filter(p_id=game.away_starter_id, stat_date=request.GET.get('date')).first()
            home_starter = Pitcher.objects.filter(p_id=game.home_starter_id).first()
            away_starter = Pitcher.objects.filter(p_id=game.away_starter_id).first()
            

            home_team_power, away_team_power = calculate_power(home_team_stats, away_team_stats, 
                                                               home_starter, away_starter,
                                                               request.GET.get('diff_weight'), 
                                                               request.GET.get('home_away_weight'), 
                                                               request.GET.get('handed_weight'), 
                                                               request.GET.get('overall_weight'), 
                                                               request.GET.get('l_10_weight'))
            winning_point_diff = abs(home_team_power-away_team_power)
            game_detail = {
                "_isHomeTeamWin": game.is_winner_home_team,
                "_winningPointDiff": winning_point_diff,
                const.GAME_GAME_ID_JSON_KEY: game.game_pk,
                const.GAME_GAME_DATE_JSON_KEY: game.game_date,
                const.GAME_HOME_TEAM_JSON_KEY: {
                    const.GAME_TEAM_ID: home_team.t_id,
                    const.GAME_NAME_JSON_KEY: home_team.t_name,
                    const.GAME_OVERALL_WINS_JSON_KEY: home_team_stats.overall_wins if home_team_stats is not None else 0,
                    const.GAME_OVERALL_LOSS_JSON_KEY: home_team_stats.overall_losses if home_team_stats is not None else 0,
                    const.GAME_HOME_WINS_JSON_KEY: home_team_stats.home_wins if home_team_stats is not None else 0,
                    const.GAME_HOME_LOSS_JSON_KEY: home_team_stats.home_losses if home_team_stats is not None else 0,
                    const.GAME_AWAY_WINS_JSON_KEY: home_team_stats.away_wins if home_team_stats is not None else 0,
                    const.GAME_AWAY_LOSS_JSON_KEY: home_team_stats.away_losses if home_team_stats is not None else 0,
                    const.GAME_LEFT_HANDED_WINS_JSON_KEY: home_team_stats.left_handed_wins if home_team_stats is not None else 0,
                    const.GAME_LEFT_HANDED_LOSS_JSON_KEY: home_team_stats.left_handed_losses if home_team_stats is not None else 0,
                    const.GAME_RIGHT_HANDED_WINS_JSON_KEY: home_team_stats.right_handed_wins if home_team_stats is not None else 0,
                    const.GAME_RIGHT_HANDED_LOSS_JSON_KEY: home_team_stats.right_handed_losses if home_team_stats is not None else 0,
                    const.GAME_LAST_10_WINS_JSON_KEY: home_team_stats.last_10_wins if home_team_stats is not None else 0,
                    const.GAME_LAST_10_LOSS_JSON_KEY: home_team_stats.last_10_losses if home_team_stats is not None else 0,
                    const.GAME_DIFF_JSON_KEY: home_team_stats.diff if home_team_stats is not None else 0,
                    const.GAME_STREAK_IS_WIN_JSON_KEY: home_team_stats.streak_is_win if home_team_stats is not None else False,
                    const.GAME_STREAK_JSON_KEY: home_team_stats.streak if home_team_stats is not None else 0,
                    const.GAME_PITCHER_JSON_KEY: {
                        const.GAME_NAME_JSON_KEY: home_starter.p_name,
                        const.GAME_PITCHER_HANDED_JSON_KEY: home_starter.handed,
                        const.GAME_PITCHER_ERA_JSON_KEY: home_starter_stats.era if home_starter_stats else 0,
                        const.GAME_PITCHER_WINS_JSON_KEY: home_starter_stats.wins if home_starter_stats else 0,
                        const.GAME_PITCHER_LOSS_JSON_KEY: home_starter_stats.losses if home_starter_stats else 0,
                        const.GAME_PITCHER_SO_JSON_KEY: home_starter_stats.so if home_starter_stats else 0
                    },
                    const.GAME_POWER: home_team_power
                },
                const.GAME_AWAY_TEAM_JSON_KEY: {
                    const.GAME_TEAM_ID: away_team.t_id,
                    const.GAME_NAME_JSON_KEY: away_team.t_name,
                    const.GAME_OVERALL_WINS_JSON_KEY: away_team_stats.overall_wins if away_team_stats is not None else 0,
                    const.GAME_OVERALL_LOSS_JSON_KEY: away_team_stats.overall_losses if away_team_stats is not None else 0,
                    const.GAME_HOME_WINS_JSON_KEY: away_team_stats.home_wins if away_team_stats is not None else 0,
                    const.GAME_HOME_LOSS_JSON_KEY: away_team_stats.home_losses if away_team_stats is not None else 0,
                    const.GAME_AWAY_WINS_JSON_KEY: away_team_stats.away_wins if away_team_stats is not None else 0,
                    const.GAME_AWAY_LOSS_JSON_KEY: away_team_stats.away_losses if away_team_stats is not None else 0,
                    const.GAME_LEFT_HANDED_WINS_JSON_KEY: away_team_stats.left_handed_wins if away_team_stats is not None else 0,
                    const.GAME_LEFT_HANDED_LOSS_JSON_KEY: away_team_stats.left_handed_losses if away_team_stats is not None else 0,
                    const.GAME_RIGHT_HANDED_WINS_JSON_KEY: away_team_stats.right_handed_wins if away_team_stats is not None else 0,
                    const.GAME_RIGHT_HANDED_LOSS_JSON_KEY: away_team_stats.right_handed_losses if away_team_stats is not None else 0,
                    const.GAME_LAST_10_WINS_JSON_KEY: away_team_stats.last_10_wins if away_team_stats is not None else 0,
                    const.GAME_LAST_10_LOSS_JSON_KEY: away_team_stats.last_10_losses if away_team_stats is not None else 0,
                    const.GAME_DIFF_JSON_KEY: away_team_stats.diff if away_team_stats is not None else 0,
                    const.GAME_STREAK_IS_WIN_JSON_KEY: away_team_stats.streak_is_win if away_team_stats is not None else False,
                    const.GAME_STREAK_JSON_KEY: away_team_stats.streak if away_team_stats is not None else 0,
                    const.GAME_PITCHER_JSON_KEY: {
                        const.GAME_NAME_JSON_KEY: away_starter.p_name,
                        const.GAME_PITCHER_HANDED_JSON_KEY: away_starter.handed,
                        const.GAME_PITCHER_ERA_JSON_KEY: away_starter_stats.era if away_starter_stats else 0,
                        const.GAME_PITCHER_WINS_JSON_KEY: away_starter_stats.wins if away_starter_stats else 0,
                        const.GAME_PITCHER_LOSS_JSON_KEY: away_starter_stats.losses if away_starter_stats else 0,
                        const.GAME_PITCHER_SO_JSON_KEY: away_starter_stats.so if away_starter_stats else 0
                    },
                    const.GAME_POWER: away_team_power
                }
            }
            detailed_games.append(game_detail)
            detailed_games.sort(key=compare_power, reverse=True)

        return JsonResponse(detailed_games, safe=False)
    return JsonResponse({"error": "Invalid request method"}, status=400)

