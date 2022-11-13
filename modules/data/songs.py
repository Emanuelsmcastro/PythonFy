from modules.flags import global_flags
import asyncio


def get_songs() -> dict:
    return global_flags.Song.SONGS.value
        

def show_song(song: str) -> None:
    print(song)