import asyncio
import tkinter as tk
from communication_station.station_v2 import CommunicationStation
from probe_simulator.probe import ProbeSimulator
from data_management.data_processor import DataProcessor
from data_management.data_storage import DataStorage

async def run_station(station):
    await station.start_server()

async def run_probe(probe):
    await probe.start_communication()

async def main():
    root = tk.Tk()
    root.title("Communication Station")

    data_processor = DataProcessor()
    data_storage = DataStorage()
    await data_storage.connect()  # Nawiązanie połączenia z bazą danych
    station = CommunicationStation('localhost', 49152, data_processor, data_storage, root)

    image_folder = 'C:\\Users\\user\\Documents\\01 Studia\\SAMOGŁOSKI AiR\\1 semestr\\Systemy rozproszone\\search_for_aliens-first_gui'
    probes = [ProbeSimulator(f"Probe{i}", ('localhost', 49152), image_folder) for i in range(10)]
    probe_tasks = [asyncio.create_task(run_probe(probe)) for probe in probes]

    while True:
        root.update_idletasks()
        root.update()
        await asyncio.sleep(0.01)

if __name__ == '__main__':
    asyncio.run(main())
