# data_management/data_storage.py
import asyncpg

class DataStorage:
    def __init__(self, dsn):
        self.dsn = dsn

    async def connect(self):
        self.conn = await asyncpg.connect(dsn=self.dsn)

    async def save_temperature(self, probe_id, temperature):
        conn = await asyncpg.connect(dsn=self.dsn)
        try:
            query = "INSERT INTO temperatures (probe_id, temperature) VALUES ($1, $2)"
            await conn.execute(query, probe_id, temperature)
            print("Temperature data saved successfully.")
        finally:
            await conn.close()

    async def get_probe_temperatures(self, probe_id):
        conn = await asyncpg.connect(dsn=self.dsn)
        try:
            query = "SELECT temperature, data_wys FROM temperatures WHERE probe_id = $1 ORDER BY data_wys"
            results = await conn.fetch(query, probe_id)
            return results
        finally:
            await conn.close()
