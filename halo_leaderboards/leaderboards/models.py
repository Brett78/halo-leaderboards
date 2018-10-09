from django.db import models


class Player(models.Model):
    gamer_tag = models.CharField(max_length=255, unique=True, db_index=True)


class Season(models.Model):
    ref = models.CharField(max_length=255, unique=True, db_index=True)
    name = models.CharField(max_length=255)
    start_date = models.DateTimeField(db_index=True)
    end_date = models.DateTimeField(null=True, blank=True, db_index=True)
    is_active = models.BooleanField(db_index=True)


class Playlist(models.Model):
    ref = models.CharField(max_length=255)
    name = models.CharField(max_length=255, db_index=True)
    season = models.ForeignKey(Season, on_delete=models.CASCADE)


class Designation(models.Model):
    name = models.CharField(max_length=255, unique=True, db_index=True)
    ref = models.IntegerField(unique=True, db_index=True)


class Tier(models.Model):
    designation = models.ForeignKey(Designation, on_delete=models.CASCADE)
    level = models.IntegerField(db_index=True)
    image_url = models.CharField(max_length=255)


class Rank(models.Model):
    player = models.ForeignKey(Player, on_delete=models.DO_NOTHING)
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    csr = models.IntegerField(db_index=True)
    tier = models.ForeignKey(Tier, on_delete=models.DO_NOTHING)
    rank = models.IntegerField(db_index=True)

    class Meta:
        unique_together = (('player', 'playlist', 'season'),)



