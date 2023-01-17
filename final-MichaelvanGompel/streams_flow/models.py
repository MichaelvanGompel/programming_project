from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator

class User(AbstractUser):
    lastfm_name = models.CharField(max_length=64)

class Song(models.Model):
    fm_user = models.ForeignKey(settings.AUTH_USER_MODEL, default=None, null=True, blank=True, on_delete=models.CASCADE, related_name="listener")
    lastfm_account = models.CharField(max_length=64)
    song_name = models.CharField(max_length=64)
    uts = models.FloatField(validators=[MinValueValidator(1)])
    week_number = models.FloatField(validators=[MinValueValidator(1)])
    artist = models.ForeignKey("Artist", on_delete=models.CASCADE, null=True, blank=True, related_name='songs_by' )
    song_genre = models.ManyToManyField("Genre", related_name="genre_songs")

    def __str__(self):
        return self.song_name

class ArtistWeek(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=None, null=True, blank=True, on_delete=models.CASCADE, related_name='user_artist_week')
    week_number = models.FloatField(validators=[MinValueValidator(1)])
    artist = models.ForeignKey("Artist", on_delete=models.CASCADE, related_name='artist_in_week')
    artist_plays = models.FloatField(validators=[MinValueValidator(1)], default=1)

    def __str__(self):
        return f'{self.artist}: {self.artist_plays} in week {self.week_number}'

class GenreWeek(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=None, null=True, blank=True, on_delete=models.CASCADE, related_name='user_genre_week') 
    week_number = models.FloatField(validators=[MinValueValidator(1)])
    genre = models.ForeignKey("Genre", on_delete=models.CASCADE, related_name='genre_in_week')
    genre_plays = models.FloatField(validators=[MinValueValidator(1)], default=1)
    
    def __str__(self):
        return f'{self.genre}: {self.genre_plays} in week {self.week_number}'

class Artist(models.Model):
    artist_name = models.CharField(max_length=64, unique=True)
    genre = models.ManyToManyField("Genre", related_name='artist_in_genre')
    playcount = models.FloatField(validators=[MinValueValidator(1)], default=1)

    def __str__(self):
        return self.artist_name

class Genre(models.Model):
    genre_name = models.CharField(max_length=64, unique=True)
    playcount = models.FloatField(validators=[MinValueValidator(1)], default=1)

    def __str__(self):
        return self.genre_name
# class Userfm(models.Model):
#     lastfm_name = models.CharField(max_length=64)
#     Userfm = models.OneToOneField(settings.AUTH_USER_MODEL, null=True, Blank=True, on_delete=models.CASCADE, related_name='Username')
