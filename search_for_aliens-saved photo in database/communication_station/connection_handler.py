class ConnectionHandler:
    def __init__(self, reader, writer, data_processor, data_storage):
        self.reader = reader
        self.writer = writer
        self.data_processor = data_processor
        self.data_storage = data_storage

    async def process_connection(self):
        addr = self.writer.get_extra_info('peername')
        data = await self.reader.read(10000)  # Zwiększono rozmiar bufora
        print(f"Received data from {addr}")
        probe_id, image_chunk = self.data_processor.extract_metadata(data)
        
        if self.data_processor.verify_data(image_chunk):
            await self.data_storage.save_data(probe_id, image_chunk)
        else:
            await self.data_storage.store_incomplete_data(probe_id, image_chunk)

        self.writer.close()

