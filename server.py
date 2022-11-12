import asyncio
import json
import os

async def list_mp3_files():
    files = list(os.walk('audio/'))[0][2]
    mp3_files = []
    for file in files:
        if file.endswith('mp3'):
            mp3_files.append(file)
        await asyncio.sleep(0)
    return mp3_files

with open('audio/test.mp3', 'rb') as file:
    music = file.read()

async def handle_echo(reader, writer):
    mp3_object = {index: music.encode() for (index, music) in zip(range(len(await list_mp3_files())), await list_mp3_files())}
    data = await reader.read(1024)
    message = data
    addr = writer.get_extra_info('peername')
    print(f"Received {message} from {addr}")
    try:
        ID_RECV = json.loads(data.decode())['ID']
    except json.decoder.JSONDecodeError:
        print('Transfer FAIL!')
    else:
        for (ID, MUSIC) in mp3_object.items():
            if ID == ID_RECV:
                writer.write(MUSIC)
                await writer.drain()

    print("Close the connection")
    writer.close()

async def main():
    server = await asyncio.start_server(
        handle_echo, 'localhost', 8888)

    addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
    print(f'Serving on {addrs}')

    async with server:
        await server.serve_forever()

asyncio.run(main())