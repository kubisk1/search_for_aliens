import asyncio
import tkinter as tk
from communication_station.station_v2 import CommunicationStation
from data_management.data_processor import DataProcessor
from data_management.data_storage import DataStorage
from probe_simulator.probe import ProbeSimulator

async def run_station(station):
    await station.start_server()  # Uruchomienie serwera stacji

async def run_probe(probe):
    await probe.start_communication()  # Rozpoczęcie komunikacji z sondą

async def main():
    root = tk.Tk()  # Inicjalizacja interfejsu użytkownika
    root.title("Communication Station")

    data_processor = DataProcessor()
    dsn = 'postgresql://postgres:postgres@localhost:5433/zdjecia'
    data_storage = DataStorage(dsn)
    await data_storage.connect()  # Nawiązanie połączenia z bazą danych
    station = CommunicationStation('localhost', 49152, data_processor, data_storage, root)

    probes = [ProbeSimulator(f"Probe{i}", ('localhost', 49152), station) for i in range(10)]  # Inicjalizacja symulatorów sond
    global probe_tasks 
    probe_tasks = [asyncio.create_task(run_probe(probe)) for probe in probes]  # Utworzenie zadań dla każdej sondy

    try:
        while True:
            root.update_idletasks()
            root.update()
            await asyncio.sleep(0.01)  
    except KeyboardInterrupt:
        print("Zatrzymywanie serwera...")
    finally:
        await stop_probes()  # Zatrzymanie komunikacji sond
        await station.stop_server()  # Zatrzymanie serwera
        print("Serwer zatrzymany.")

if __name__ == '__main__':
    asyncio.run(main())  # Uruchomienie funkcji main

async def stop_probes():
    global probe_tasks
    for task in probe_tasks:
        task.cancel()  # Anulowanie zadań dla sond
    await asyncio.gather(*probe_tasks, return_exceptions=True)
    probe_tasks = []
