import asyncio
import random

class ProbeSimulator:
    def __init__(self, probe_id, station_address, station):
        self.probe_id = probe_id
        self.station_address = station_address
        self.station = station
        self.running = False

    async def start_communication(self):
        while True:
            try:
                if not self.running:
                    await asyncio.sleep(1)
                    continue
                await asyncio.sleep(random.randint(10, 30))
                data = self.generate_data()
                await self.send_data(data)
                self.station.update_data(self.probe_id, data)
            except asyncio.CancelledError:
                print(f"[{self.probe_id}] Communication task was cancelled.")
                break

    def generate_data(self):
        temperature = random.uniform(-100, 100)
        humidity = random.uniform(0, 100)
        visibility = random.uniform(0, 100)
        passengers_count = random.randint(0, 100)
        pressure = random.uniform(900, 1100)
        data = {
            'probe_id': self.probe_id,
            'temperature': temperature,
            'humidity': humidity,
            'visibility': visibility,
            'passengers_count': passengers_count,
            'pressure': pressure
        }
        print(f"[{self.probe_id}] Sending data: {data}")
        return data

    async def send_data(self, data):
        try:
            reader, writer = await asyncio.open_connection(*self.station_address)
            encoded_data = ','.join(map(str, data.values())).encode()
            print(f"[{self.probe_id}] Sending data: {encoded_data}")
            writer.write(encoded_data)
            await writer.drain()
            ack = await reader.read(100)
            writer.close()
            await writer.wait_closed()
            if ack.decode() == "ACK":
                print(f"[{self.probe_id}] Data sent successfully and acknowledged.")
            else:
                raise Exception("Acknowledgment not received")
        except Exception as e:
            print(f"[{self.probe_id}] Error sending data: {e}")
            await self.station.data_storage.save_error(None, str(e))

    def start(self):
        self.running = True

    def stop(self):
        self.running = False

    async def send_data_with_retries(self, data, retries=3):
        for attempt in range(retries):
            try:
                await self.send_data(data)
                return
            except Exception as e:
                print(f"[{self.probe_id}] Error sending data: {e}. Retrying {attempt + 1}/{retries}...")
                await asyncio.sleep(5)
        print(f"[{self.probe_id}] Failed to send data after {retries} attempts.")
