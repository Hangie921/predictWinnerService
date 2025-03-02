from django.db import models
from django.contrib.auth.models import User

class Weight(models.Model):
    diff_win_point_weight = models.FloatField()
    last_10_winning_weight = models.FloatField()
    home_or_away_winning_weight = models.FloatField()
    pitcher_handed_winning_weight = models.FloatField()
    overall_winning_weight = models.FloatField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='weight')

    def __str__(self):
        return self.owner


class Game(models.Model):
    game_pk = models.IntegerField()
    game_date = models.DateField()
    winner_t_id = models.IntegerField()
    home_team_power = models.FloatField()
    away_team_power = models.FloatField()
    is_winner_home_team = models.BooleanField()
    home_starter_id = models.IntegerField()
    away_starter_id = models.IntegerField()
    home_team_id = models.IntegerField()
    away_team_id = models.IntegerField()

class Pitcher(models.Model):
    p_id = models.IntegerField()
    p_name = models.TextField(max_length=100)
    handed = models.TextField()

class PitcherStat(models.Model):
    p_id = models.IntegerField()
    stat_date = models.DateField()
    wins = models.IntegerField()
    losses = models.IntegerField()
    era = models.FloatField()
    so = models.IntegerField()

class Team(models.Model):
    t_id = models.IntegerField()
    t_name = models.TextField()

class TeamStat(models.Model):
    t_id           = models.TextField()
    stat_date      = models.DateField()
    overall_wins   = models.IntegerField()
    overall_losses   = models.IntegerField()
    home_wins      = models.IntegerField()
    home_losses      = models.IntegerField()
    away_wins      = models.IntegerField()
    away_losses      = models.IntegerField()
    left_handed_wins  = models.IntegerField()
    left_handed_losses  = models.IntegerField()
    right_handed_wins  = models.IntegerField()
    right_handed_losses  = models.IntegerField()
    last_10_wins   = models.IntegerField()
    last_10_losses   = models.IntegerField()
    diff           = models.IntegerField()
    streak_is_win  = models.BooleanField()
    streak         = models.IntegerField()