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
            data = await self.reader.read(10000)  # Zwiększono rozmiar bufora
            print(f"Received data from {addr}")
            probe_id, temperature = self.data_processor.extract_metadata(data)
            
            if self.data_processor.verify_data(data):
                await self.data_storage.save_temperature(probe_id, temperature)
                self.station.update_temperature(probe_id, temperature)
                self.writer.write(b"ACK")
                await self.writer.drain()
            else:
                self.writer.write(b"NACK")
                await self.writer.drain()
        except Exception as e:
            print(f"Error processing connection from {addr}: {e}")
            self.writer.write(b"NACK")
            await self.writer.drain()
        finally:
            self.writer.close()
            await self.writer.wait_closed()
