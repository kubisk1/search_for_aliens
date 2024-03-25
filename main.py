import asyncio
from communication_station.station import CommunicationStation
from probe_simulator.probe import ProbeSimulator
from data_management.data_processor import DataProcessor
from data_management.data_storage import DataStorage

async def main():
    data_processor = DataProcessor()
    data_storage = DataStorage()

    # Inicjalizacja i start stacji odbiorczej z przekazaniem obiektów processor i storage
    station = CommunicationStation('localhost', 49152, data_processor, data_storage)
    await asyncio.create_task(station.start_server())

    # Symulacja działania sondy
    probe = ProbeSimulator("Probe1", ('localhost', 49152))
    await asyncio.create_task(probe.start_communication())

if __name__ == '__main__':
    asyncio.run(main())
