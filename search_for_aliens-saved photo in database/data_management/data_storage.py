import asyncpg

class DataStorage:
    def __init__(self):
        self.conn = None
        self.incomplete_data = {}

    async def connect(self):
        self.conn = await asyncpg.connect(user='postgres', password='postgres', database='zdjecia', host='localhost', port=5433)

    async def save_data(self, probe_id, data):
        if not self.conn:
            await self.connect()
        query = "INSERT INTO photos (probe_id, zdjecie) VALUES ($1, $2)"
        await self.conn.execute(query, probe_id, data)
        print("Data saved successfully.")

    async def store_incomplete_data(self, probe_id, data):
        if probe_id not in self.incomplete_data:
            self.incomplete_data[probe_id] = b''
        self.incomplete_data[probe_id] += data
        if len(self.incomplete_data[probe_id]) >= 1024:  # Sprawdź, czy dane są kompletne
            await self.save_data(probe_id, self.incomplete_data[probe_id][:1024])
            self.incomplete_data[probe_id] = self.incomplete_data[probe_id][1024:]
        else:
            print(f"Incomplete data stored for probe_id {probe_id}")
