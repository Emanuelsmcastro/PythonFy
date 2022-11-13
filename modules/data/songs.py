from modules.flags import global_flags
import asyncio
import json
import aiofiles
import os

def __get_songs() -> dict:
    __songs = [song for song in list(os.listdir('audios/')) if song.endswith('mp3')]
    return {index: song for (index, song) in zip(range(len(__songs)), __songs)}

def __dump_dict_to_json_and_encode(value: dict):
    return json.dumps(value).encode()

async def get_songs(loop: asyncio.AbstractEventLoop) -> None:
   result = await loop.run_in_executor(None, __get_songs)
   
   await asyncio.sleep(0)
   
   result_dumped_and_encoded = await loop.run_in_executor(None, __dump_dict_to_json_and_encode, result)
   
   await asyncio.sleep(0)
   
   return result_dumped_and_encoded

def __full_path(song_name: str) -> str:
    return global_flags.Song.full_path_song(song_name)

async def get_full_path_song(loop: asyncio.AbstractEventLoop, song_name: str) -> str:
    result = await loop.run_in_executor(None, __full_path, song_name)
    return result


async def get_song_file(path_song_file: str):
    async with aiofiles.open(path_song_file, 'rb') as file:
        song =  await file.read() 
    return b'/start/' + song + b'/stop/'