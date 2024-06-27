import asyncpg

class DataStorage:
    def __init__(self, dsn):
        self.dsn = dsn

    async def connect(self):
        self.conn = await asyncpg.connect(dsn=self.dsn)  # Nawiązanie połączenia z bazą danych

    async def save_reading(self, data):
        conn = await asyncpg.connect(dsn=self.dsn)
        try:
            sensor_id = await self.get_sensor_id(data['probe_id'])
            if sensor_id is None:
                raise ValueError(f"Sensor ID for probe {data['probe_id']} not found.")
            query = """
            INSERT INTO readings (sensor_id, timestamp, temperature, humidity, visibility, passengers_count, pressure) 
            VALUES ($1, NOW(), $2, $3, $4, $5, $6)
            """
            await conn.execute(query, sensor_id, data['temperature'], data['humidity'], data['visibility'], data['passengers_count'], data['pressure'])
            print("Reading data saved successfully.")
        finally:
            await conn.close()

    async def get_sensor_id(self, probe_id):
        conn = await asyncpg.connect(dsn=self.dsn)
        try:
            query = "SELECT id FROM sensors WHERE probe_id = $1"
            result = await conn.fetchrow(query, probe_id)
            if result:
                return result['id']
            return None
        finally:
            await conn.close()

    async def get_probe_readings(self, sensor_id):
        conn = await asyncpg.connect(dsn=self.dsn)
        try:
            query = "SELECT timestamp, temperature, humidity, visibility, passengers_count, pressure FROM readings WHERE sensor_id = $1 ORDER BY timestamp"
            results = await conn.fetch(query, sensor_id)
            return results
        finally:
            await conn.close()

    async def save_command(self, station_id, probe_id, command):
        conn = await asyncpg.connect(dsn=self.dsn)
        try:
            # Pobranie sensor_id na podstawie probe_id
            query_get_sensor_id = "SELECT id FROM sensors WHERE probe_id = $1"
            result = await conn.fetchrow(query_get_sensor_id, probe_id)
            if result:
                sensor_id = result['id']
                query = """
                INSERT INTO commands (station_id, sensor_id, command, timestamp) 
                VALUES ($1, $2, $3, NOW())
                """
                await conn.execute(query, station_id, sensor_id, command)
                print(f"Command data saved successfully for probe_id={probe_id}, command={command}.")
            else:
                print(f"Sensor ID not found for probe_id={probe_id}. Command not saved.")
        finally:
            await conn.close()




    async def save_error(self, sensor_id, error_message):
        conn = await asyncpg.connect(dsn=self.dsn)
        try:
            query = """
            INSERT INTO errors (sensor_id, error_message, timestamp) 
            VALUES ($1, $2, NOW())
            """
            await conn.execute(query, sensor_id, error_message)
            print("Error data saved successfully.")
        finally:
            await conn.close()
