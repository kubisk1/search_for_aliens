import asyncio
from communication_station.connection_handler import ConnectionHandler
import mysql.connector

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

        

