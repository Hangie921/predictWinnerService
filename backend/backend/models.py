from django.db import models
from django.contrib.auth.models import User

class Weight(models.Model):
    diff_win_point_weight = models.FloatField()
    last_10_win_weight = models.FloatField()
    home_or_away_winning_weight = models.FloatField()
    pitcher_handed_winning_weight = models.FloatField()
    overall_winning_weight = models.FloatField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='weights')

    def __str__(self):
        return self.owner