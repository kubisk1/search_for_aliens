import asyncio
from communication_station.station_v2 import CommunicationStation
from probe_simulator.probe import ProbeSimulator
from data_management.data_processor import DataProcessor
from data_management.data_storage import DataStorage

async def run_station(station):
    await station.start_server()

async def run_probe(probe):
    await probe.start_communication()

async def main():
    data_processor = DataProcessor()
    data_storage = DataStorage()

    # Inicjalizacja i uruchomienie stacji
    station = CommunicationStation('localhost', 49152, data_processor, data_storage)
    print ("XD")
    station_task = asyncio.create_task(run_station(station))

    # Uruchomienie symulatorów sond
    probes = [ProbeSimulator(f"Probe{i}", ('localhost', 49152)) for i in range(10)]
    probe_tasks = [asyncio.create_task(run_probe(probe)) for probe in probes]

    # Czekamy na zakończenie pracy stacji i wszystkich sond
    await asyncio.gather(station_task, *probe_tasks)

if __name__ == '__main__':
    asyncio.run(main())
