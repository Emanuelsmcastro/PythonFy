import asyncio
import json
from modules.data import songs


async def handle_echo(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):    
    loop = asyncio.get_event_loop()
    addr = writer.get_extra_info('peername')
    print(f"Connected on {addr}")
    writer.write(await songs.get_songs(loop))
    await writer.drain()
    data = await reader.read(1024)
    print(data)
    try:
        ID_RECV = json.loads(data.decode())['ID']
    except json.decoder.JSONDecodeError:
        print('Transfer FAIL!')
    else:
        dict_songs = songs.__get_songs()
        if ID_RECV in dict_songs:
            song_path = await songs.get_full_path_song(loop, dict_songs[ID_RECV])
            writer.write(await songs.get_song_file(song_path))
            await writer.drain()
        
    print("Close the connection")
    writer.close()
    await writer.wait_closed()

async def main():
         
    server = await asyncio.start_server(
        handle_echo, 'localhost', 5555)

    addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
    print(f'Started on {addrs}')

    async with server:
        await server.serve_forever()

try:
    asyncio.run(main())
except KeyboardInterrupt:
    print('Server closed!')