import asyncio
import json
from modules.player import media_player

choice_song = lambda id: {'ID': id}

async def tcp_echo_client():
    song_started = False
    reader, writer = await asyncio.open_connection(
        '000.000.0.000', 5555)
    data = await reader.read(1024)
    print(data)
    choice = choice_song(int(input('Choice a song ID: ')))
    print(f'Send: {choice!r}')
    writer.write(json.dumps(choice).encode())
    await writer.drain()
    song = b''
    while True:
        data = await reader.read(1024)
        if data == b'':
            break
        if data.startswith(b'/start/'):
            print('Download started')
            initial_data = data.replace(b'/start/', b'')
            song_started = True
            song += initial_data
        elif song_started:
            song += data
        if song_started and data.endswith(b'/stop/'):
            final_data = data.replace(b'/stop/', b'')
            song += final_data
            song_started = False
            print('Download finished')

    print('Close the connection')
    writer.close()
    media_player.play(song)

while True:
    try:
        asyncio.run(tcp_echo_client())
    except KeyboardInterrupt:
        break
    