import asyncio
import random

class ProbeSimulator:
    def __init__(self, probe_id, station_address):
        self.probe_id = probe_id
        self.station_address = station_address

    async def start_communication(self):
        while True:
            await asyncio.sleep(random.randint(10, 30))  # Symulacja okna komunikacyjnego
            data = self.generate_data()
            await self.send_data(data)

    def generate_data(self):
        return f"Data from {self.probe_id}"

    async def send_data(self, data):
        reader, writer = await asyncio.open_connection(*self.station_address)
        print(f"[Probe {self.probe_id}] Sending data: {data}")
        writer.write(data.encode())
        await writer.drain()
        writer.close()
        await writer.wait_closed()
        print(f"[Probe {self.probe_id}] Data sent successfully.")

