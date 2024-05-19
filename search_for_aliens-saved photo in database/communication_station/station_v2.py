import asyncio
import tkinter as tk
from tkinter import ttk, scrolledtext
from communication_station.connection_handler import ConnectionHandler

class CommunicationStation:
    
    def __init__(self, host, port, data_processor, data_storage, root):
        self.host = host
        self.port = port
        self.data_processor = data_processor
        self.data_storage = data_storage
        self.root = root
        self.server = None  # Zmienna przechowująca obiekt serwera
        self.setup_gui()
        

    def setup_gui(self):
        self.messages_text = scrolledtext.ScrolledText(self.root, width=70, height=10)
        self.messages_text.pack(pady=10)

        ttk.Button(self.root, text="Start Server", command=lambda: asyncio.create_task(self.start_server())).pack(pady=10)
        ttk.Button(self.root, text="Stop Server", command=lambda: asyncio.create_task(self.stop_server())).pack(pady=10)

    async def start_server(self):
        print(f"Starting server on {self.host}:{self.port}")
        self.server = await asyncio.start_server(self.handle_connection, self.host, self.port)
        async with self.server:
            print(f"Serving on {self.server.sockets[0].getsockname()}")
            self.messages_text.insert(tk.END, "Server has been started.\n")
            await self.server.serve_forever()

    async def stop_server(self):
        if self.server:
            self.server.close()  # Zamknięcie serwera
            await self.server.wait_closed()  # Oczekiwanie na zamknięcie serwera
            print("Server has been stopped.")
            self.messages_text.insert(tk.END, "Server has been stopped.\n")

    async def handle_connection(self, reader, writer):
        handler = ConnectionHandler(reader, writer, self.data_processor, self.data_storage)
        await handler.process_connection()
