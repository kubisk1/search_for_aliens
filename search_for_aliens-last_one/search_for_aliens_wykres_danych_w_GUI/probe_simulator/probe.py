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
                    await asyncio.sleep(1)  # Krótkie opóźnienie, aby nie przeciążać pętli
                    continue
                await asyncio.sleep(random.randint(10, 30))  # Symulacja okna komunikacyjnego
                temperature = self.generate_temperature()
                await self.send_data(temperature) 
                self.station.update_temperature(self.probe_id, temperature)  # Aktualizacja temperatury w GUI
            except asyncio.CancelledError:
                print(f"[{self.probe_id}] Communication task was cancelled.")
                break

    def generate_temperature(self):
        # Generowanie losowej temperatury w zakresie -100 do 100 stopni Celsjusza
        temperature = random.uniform(-100, 100)
        print(f"[{self.probe_id}] Sending temperature: {temperature:.2f}")
        return temperature

    async def send_data(self, temperature):
        try:
            reader, writer = await asyncio.open_connection(*self.station_address)  # Nawiązanie połączenia
            data = f"{self.probe_id},{temperature}".encode()
            print(f"[{self.probe_id}] Sending data: {data}")
            writer.write(data)  # Wysłanie danych
            await writer.drain()
            ack = await reader.read(100)  # Odczytanie potwierdzenia wysłania danych
            writer.close()
            await writer.wait_closed()
            if ack.decode() == "ACK":
                print(f"[{self.probe_id}] Data sent successfully and acknowledged.")
            else:
                raise Exception("Acknowledgment not received")
        except Exception as e:
            print(f"[{self.probe_id}] Error sending data: {e}")

    def start(self):
        self.running = True  # Rozpoczęcie komunikacji

    def stop(self):
        self.running = False  # Zatrzymanie komunikacji

    async def send_data_with_retries(self, temperature, retries=3):
        for attempt in range(retries):
            try:
                await self.send_data(temperature)  # Próba wysłania danych
                return
            except Exception as e:
                print(f"[{self.probe_id}] Error sending data: {e}. Retrying {attempt + 1}/{retries}...")
                await asyncio.sleep(5)  
        print(f"[{self.probe_id}] Failed to send data after {retries} attempts.")
