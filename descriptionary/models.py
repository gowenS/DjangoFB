from django.db import models

class Game(models.Model):
    game_id = models.AutoField(primary_key=True)
    game_name = models.CharField(max_length=4)
    tot_players = models.IntegerField()
    players_in_lobby = models.IntegerField(null=True)
    game_state = models.IntegerField()

    def __str__(self):
        return self.game_name

class Player_List(models.Model):
    player_id = models.IntegerField(null=False)
    game_inst = models.ForeignKey(Game, on_delete=models.CASCADE)
    player_name = models.CharField(max_length=15)
    text_clues = models.CharField(max_length=3000)
    submit_state = models.IntegerField()

    def __str__(self):
        return self.player_name
