class ConnectionHandler:
    def __init__(self, reader, writer, data_processor, data_storage):
        self.reader = reader
        self.writer = writer
        self.data_processor = data_processor
        self.data_storage = data_storage

    async def process_connection(self):
        data = await self.reader.read(100)
        # Tutaj: Użycie data_processor do przetwarzania danych
        processed_data = self.data_processor.process_data(data.decode())
        # I data_storage do zapisu danych
        await self.data_storage.save_data(processed_data)
        self.writer.close()
