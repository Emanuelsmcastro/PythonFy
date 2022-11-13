import asyncio
import json
from modules.data.songs import get_songs
from modules.utils import type_comparator


async def handle_echo(reader, writer):    
    data = await reader.read(1024)
    message = data
    addr = writer.get_extra_info('peername')
    print(f"Received {message} from {addr}")
    try:
        ID_RECV = json.loads(data.decode())['ID']
    except json.decoder.JSONDecodeError:
        print('Transfer FAIL!')

    print("Close the connection")
    writer.close()

async def main():
    
    # songs = get_songs()
    # if type_comparator.comparator(songs, dict):
    #     for index, song in songs.items():
    #         print(f'{index:<3} --> {song.replace(".mp3", "")}')
        
    server = await asyncio.start_server(
        handle_echo, 'localhost', 5555)

    addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
    print(f'Serving on {addrs}')

    async with server:
        await server.serve_forever()

try:
    asyncio.run(main())
except KeyboardInterrupt:
    print('Server closed!')