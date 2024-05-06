import asyncio
from communication_station.station_v2 import CommunicationStation
from probe_simulator.probe import ProbeSimulator
from data_management.data_processor import DataProcessor
from data_management.data_storage import DataStorage
import tkinter as tk
from tkinter import ttk, scrolledtext

async def run_station(station):
    await station.start_server()

async def run_probe(probe):
    await probe.start_communication()


async def main():
    root = tk.Tk()
    root.title("Communication Station")

    data_processor = DataProcessor()
    data_storage = DataStorage()
    station = CommunicationStation('localhost', 49152, data_processor, data_storage, root)
    
    probes = [ProbeSimulator(f"Probe{i}", ('localhost', 49152)) for i in range(10)]
    probe_tasks = [asyncio.create_task(run_probe(probe)) for probe in probes]

    # Asynchronous loop for Tkinter GUI
    while True:
        root.update_idletasks()
        root.update()
        await asyncio.sleep(0.01)

if __name__ == '__main__':
    asyncio.run(main())
