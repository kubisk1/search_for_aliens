import asyncio
from communication_station.connection_handler import ConnectionHandler

class CommunicationStation:
    def __init__(self, host, port, data_processor, data_storage):
        self.host = host
        self.port = port
        self.data_processor = data_processor
        self.data_storage = data_storage

    async def start_server(self):
        print(f"Starting server on {self.host}:{self.port}")
        server = await asyncio.start_server(
            self.handle_connection, self.host, self.port)
        async with server:
            print(f"Serving on {server.sockets[0].getsockname()}")
            await server.serve_forever()


    async def handle_connection(self, reader, writer):
        data = await reader.read(100)
        addr = writer.get_extra_info('peername')
        print(f"Received {data.decode()} from {addr}")
        # Tutaj: przetwarzanie danych, np. zapis do bazy
        writer.close()

