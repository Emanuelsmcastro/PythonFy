import os 
from enum import Enum


class Song(Enum):
    __songs = [song for song in list(os.walk('audios/'))[0][2] if song.endswith('mp3')]
    path_songs = 'audios/'
    full_path_song = lambda song_name: os.path.join(Song.path_songs.value, song_name) 
    SONGS = {index: song for (index, song) in zip(range(len(__songs)), __songs)}