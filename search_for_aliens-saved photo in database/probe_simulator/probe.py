import asyncio
import random
import os

class ProbeSimulator:
    def __init__(self, probe_id, station_address, image_folder):
        self.probe_id = probe_id
        self.station_address = station_address
        self.image_folder = image_folder

    async def start_communication(self):
        while True:
            await asyncio.sleep(random.randint(10, 30))  # Symulacja okna komunikacyjnego
            data = self.generate_data()
            if data:
                await self.send_data(data)

    def generate_data(self):
        # Pobierz listę plików w folderze
        image_files = os.listdir(self.image_folder)
        if not image_files:
            print(f"No images found in folder {self.image_folder}")
            return None
        
        # Wybierz losowy plik z folderu
        image_file = random.choice(image_files)
        image_path = os.path.join(self.image_folder, image_file)
        
        # Odczytaj zawartość pliku jako dane binarne
        with open(image_path, 'rb') as file:
            data = file.read()
        
        print(f"[Probe {self.probe_id}] Sending image: {image_file}")
        return data

    async def send_data(self, data):
        reader, writer = await asyncio.open_connection(*self.station_address)
        print(f"[Probe {self.probe_id}] Sending data of size: {len(data)} bytes")
        writer.write(data)
        await writer.drain()
        writer.close()
        await writer.wait_closed()
        print(f"[Probe {self.probe_id}] Data sent successfully.")


