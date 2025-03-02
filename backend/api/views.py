from django.shortcuts import render
from rest_framework import generics
from django.contrib.auth.models import User
from .models import Weight, Game, Team, TeamStat, Pitcher, PitcherStat
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import UserSerializer,WeightSerializer,GameSerializer
from django.http import JsonResponse, HttpResponse
from . import const 


class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class CreateWeightView(generics.ListCreateAPIView):
    queryset = Weight.objects.all()
    serializer_class = WeightSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Weight.objects.filter(owner=user)

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(owner=self.request.user)
        else:
            print(serializer.errors)

class UpdateWeightView(generics.UpdateAPIView):
    queryset = Weight.objects.all()
    serializer_class = WeightSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Weight.objects.filter(owner=user)

    def perform_update(self, serializer):
        if serializer.is_valid():
            serializer.save(owner=self.request.user)
        else:
            print(serializer.errors)

def get_prediction(request):
    if request.META["REQUEST_METHOD"] == "GET":
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
            
            game_detail = {
                const.GAME_GAME_ID_JSON_KEY: game.game_pk,
                const.GAME_GAME_DATE_JSON_KEY: game.game_date,
                const.GAME_HOME_TEAM_JSON_KEY: {
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
                    }
                },
                const.GAME_AWAY_TEAM_JSON_KEY: {
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
                    }
                }
            }
            detailed_games.append(game_detail)
            
        return JsonResponse(detailed_games, safe=False)
    return JsonResponse({"error": "Invalid request method"}, status=400)


# def get_prediction(request):

#     print("diff_weight is", request.GET.get('diff_weight'))
#     print("date is", request.GET.get('date'))
#     if request.META["REQUEST_METHOD"] == "GET":
#         # return JsonResponse({"prediction": "This is a prediction"})
#         games = Game.objects.filter(game_date=request.GET.get('date'))
#         print("len", len(games))
#         if len(games) == 0:
#             return JsonResponse({"prediction": "No games data for this date yet"})
#             # return HttpResponse(status=204)
#         serializer = GameSerializer(games, many=True)
#         print("typeof", type(serializer.data))
#         return JsonResponse(serializer.data, safe=False)
    