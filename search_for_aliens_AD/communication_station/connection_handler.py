class ConnectionHandler:
    def __init__(self, reader, writer, data_processor, data_storage, station):
        self.reader = reader
        self.writer = writer
        self.data_processor = data_processor
        self.data_storage = data_storage
        self.station = station

    async def process_connection(self):
        addr = self.writer.get_extra_info('peername')
        try:
            data = await self.reader.read(10000)  # Odczytanie danych
            print(f"Received data from {addr}")
            metadata = self.data_processor.extract_metadata(data)
            
            if self.data_processor.verify_data(data):
                await self.data_storage.save_reading(metadata)  # Zapisanie danych do bazy
                self.station.update_data(metadata['probe_id'], metadata)
                self.writer.write(b"ACK")  # Wysłanie potwierdzenia przesłania danych
                await self.writer.drain()
            else:
                self.writer.write(b"NACK")
                await self.writer.drain()
        except Exception as e:
            print(f"Error processing connection from {addr}: {e}")
            await self.data_storage.save_error(None, str(e))
            self.writer.write(b"NACK")
            await self.writer.drain()
        finally:
            self.writer.close()  # Zamknięcie połączenia
            await self.writer.wait_closed()
