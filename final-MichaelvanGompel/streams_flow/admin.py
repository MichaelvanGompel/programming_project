from django.contrib import admin
from .models import User, Song, GenreWeek, ArtistWeek, Artist, Genre

admin.site.register(User)
admin.site.register(Song)
admin.site.register(GenreWeek)
admin.site.register(ArtistWeek)
admin.site.register(Artist)
admin.site.register(Genre)