from django.db import models
from django.contrib.auth.models import User

class Weight(models.Model):
    diff_win_point_weight = models.FloatField()
    last_10_win_weight = models.FloatField()
    home_or_away_winning_weight = models.FloatField()
    pitcher_handed_winning_weight = models.FloatField()
    overall_winning_weight = models.FloatField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='weight')

    def __str__(self):
        return self.owner

class Game(models.Model):
    game_pk = models.TextField()
    game_date = models.DateField()
    winner_t_id = models.TextField()
    is_winner_home_team = models.BooleanField()
    h_starter_id = models.TextField()
    a_starter_id = models.TextField()
    home_team_id = models.TextField()
    away_team_id = models.TextField()

class Pitcher(models.Model):
    p_id = models.TextField()
    p_name = models.TextField()
    handed = models.TextField()

class PitcherStat(models.Model):
    p_id = models.TextField()
    stat_date = models.DateField()
    wins = models.IntegerField()
    loss = models.IntegerField()
    era = models.FloatField()
    so = models.IntegerField()

class Team(models.Model):
    t_id = models.TextField()
    t_name = models.TextField()

class TeamStat(models.Model):
    t_id           = models.TextField()
    stat_date      = models.DateField()
    overall_wins   = models.IntegerField()
    overall_loss   = models.IntegerField()
    home_wins      = models.IntegerField()
    home_loss      = models.IntegerField()
    away_wins      = models.IntegerField()
    away_loss      = models.IntegerField()
    l_handed_wins  = models.IntegerField()
    l_handed_loss  = models.IntegerField()
    r_handed_wins  = models.IntegerField()
    r_handed_loss  = models.IntegerField()
    last_10_wins   = models.IntegerField()
    last_10_loss   = models.IntegerField()
    diff           = models.IntegerField()
    streak_is_win  = models.BooleanField()
    streak         = models.IntegerField()

class PredictionQuery(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()

class PredictionAccuracy(models.Model):
    accuracy = models.FloatField()