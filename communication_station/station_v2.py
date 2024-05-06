import asyncio
import tkinter as tk
from tkinter import ttk, scrolledtext
import mysql.connector
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
        data = await reader.read(100)
        addr = writer.get_extra_info('peername')
        print(f"Received {data.decode()} from {addr}")
        # Tutaj: przetwarzanie danych, np. zapis do bazy

        # Przetwarzanie danych
        processed_data = self.data_processor.process_data(data.decode())

        # Zapis danych do bazy danych
        try:
            # Nawiązanie połączenia z bazą danych
            connection = mysql.connector.connect(
                host='mysql.agh.edu.pl',
                user='filipch1',
                password='TNh6aMviBtd1iUXw',
                database='filipch1'
            )

            # Utworzenie kursora
            cursor = connection.cursor()

            # Sprawdzenie, czy obrazek o danym ID już istnieje w bazie
            cursor.execute("SELECT * FROM odegrane_dane WHERE Nr_stacji = %s", (processed_data['id'],))
            existing_image = cursor.fetchone()

            if existing_image:
             # Aktualizacja istniejącego obrazka w bazie danych
             update_query = "UPDATE odegrane_dane SET Zdjecie = CONCAT(Zdjecie, %s) WHERE Nr_stacji = %s"
             cursor.execute(update_query, (processed_data['data'], processed_data['id']))
            else:
            # Wstawienie nowego obrazka do bazy danych
             insert_query = "INSERT INTO odegrane_dane (Nr_stacji, Zdjecie, Data_wyslania) VALUES (%s, %s, NOW())"
             cursor.execute(insert_query, (processed_data['id'], processed_data['data']))

            connection.commit()
            print("Data saved successfully to MySQL database")

        except mysql.connector.Error as error:
            print(f"Error while connecting to MySQL: {error}")           

        finally:
            # Zamknięcie kursora i połączenia
            cursor.close()
            connection.close()
        writer.close()

        

