import asyncio
import tkinter as tk
from tkinter import ttk, scrolledtext, Canvas
from communication_station.connection_handler import ConnectionHandler
import matplotlib.pyplot as plt
from probe_simulator.probe import ProbeSimulator

class CommunicationStation:

    def __init__(self, host, port, data_processor, data_storage, root):
        self.host = host
        self.port = port
        self.data_processor = data_processor
        self.data_storage = data_storage
        self.root = root
        self.server = None
        self.probes = {}  # Słownik do przechowywania stanu sond
        self.diode_canvas = {}  # Przechowywanie obiektów Canvas dla diod
        self.temperature_labels = {}  # Przechowywanie etykiet dla temperatur
        self.server_diode_canvas = None  # Przechowywanie obiektu Canvas dla diody serwera
        self.message_index = 0  # Indeks do śledzenia, w której kolumnie dodawane są wiadomości
        self.setup_gui()  # Ustawienie GUI

    def setup_gui(self):
        self.root.title("Communication Station")

        # Główne ramki
        control_frame = ttk.Frame(self.root)
        control_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

        # Ramka kontrolna
        server_frame = ttk.LabelFrame(control_frame, text="Server Control")
        server_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5)

        probe_control_frame = ttk.LabelFrame(control_frame, text="Probe Control")
        probe_control_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        # Przyciski serwera
        ttk.Button(server_frame, text="Start Server", command=lambda: asyncio.create_task(self.start_server())).pack(pady=5)
        ttk.Button(server_frame, text="Stop Server", command=lambda: asyncio.create_task(self.stop_server())).pack(pady=5)

        # Dioda sygnalizacyjna serwera
        self.server_diode_canvas = Canvas(server_frame, width=20, height=20, bg='red')
        self.server_diode_canvas.pack(pady=5)

        # Przyciski sond
        probe_button_frame = ttk.Frame(probe_control_frame)
        probe_button_frame.pack(side=tk.TOP, fill=tk.X)

        self.probe_buttons = {}
        for i in range(10):
            probe_id = f"Probe{i}"
            self.probes[probe_id] = {'connected': False, 'probe_instance': None, 'task': None}

            frame = ttk.LabelFrame(probe_button_frame, text=f"{probe_id}")
            frame.grid(row=0, column=i, padx=5, pady=5)

            connection_frame = ttk.LabelFrame(frame, text="Connection")
            connection_frame.pack(fill=tk.X, pady=2)

            ttk.Button(connection_frame, text="Connect", command=lambda probe_id=probe_id: asyncio.create_task(self.connect_probe(probe_id))).pack(pady=2)
            ttk.Button(connection_frame, text="Disconnect", command=lambda probe_id=probe_id: asyncio.create_task(self.disconnect_probe(probe_id))).pack(pady=2)

            plot_frame = ttk.LabelFrame(frame, text="Plots")
            plot_frame.pack(fill=tk.X, pady=2)

            ttk.Button(plot_frame, text="Temperature", command=lambda probe_id=probe_id: asyncio.create_task(self.fetch_and_plot_readings(probe_id, 'temperature'))).pack(pady=2)
            ttk.Button(plot_frame, text="Humidity", command=lambda probe_id=probe_id: asyncio.create_task(self.fetch_and_plot_readings(probe_id, 'humidity'))).pack(pady=2)
            ttk.Button(plot_frame, text="Visibility", command=lambda probe_id=probe_id: asyncio.create_task(self.fetch_and_plot_readings(probe_id, 'visibility'))).pack(pady=2)
            ttk.Button(plot_frame, text="Passengers Count", command=lambda probe_id=probe_id: asyncio.create_task(self.fetch_and_plot_readings(probe_id, 'passengers_count'))).pack(pady=2)
            ttk.Button(plot_frame, text="Pressure", command=lambda probe_id=probe_id: asyncio.create_task(self.fetch_and_plot_readings(probe_id, 'pressure'))).pack(pady=2)

            # Dioda sygnalizacyjna sondy
            diode_canvas = Canvas(frame, width=20, height=20, bg='red')
            diode_canvas.pack(pady=5)
            self.diode_canvas[probe_id] = diode_canvas

            temperature_label = ttk.Label(frame, text="Last Temp: N/A")
            temperature_label.pack(pady=2)
            self.temperature_labels[probe_id] = temperature_label

        ttk.Button(probe_control_frame, text="Connect All Probes", command=lambda: asyncio.create_task(self.connect_all_probes())).pack(pady=5)
        ttk.Button(probe_control_frame, text="Disconnect All Probes", command=lambda: asyncio.create_task(self.disconnect_all_probes())).pack(pady=5)

        # Pole tekstowe do wiadomości
        messages_frame = ttk.LabelFrame(self.root, text="Messages")
        messages_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Tworzenie 3 kolumn dla wiadomości
        self.messages_text = [scrolledtext.ScrolledText(messages_frame, width=40, height=15) for _ in range(3)]
        for i, text_widget in enumerate(self.messages_text):
            text_widget.grid(row=0, column=i, padx=5, pady=5, sticky="nsew")

        # Rozciąganie kolumn
        for i in range(3):
            messages_frame.grid_columnconfigure(i, weight=1)

    def update_diode(self, probe_id, connected):
        if connected:
            self.diode_canvas[probe_id].config(bg='green')  # Zmiana koloru diody na zielony
        else:
            self.diode_canvas[probe_id].config(bg='red')  # Zmiana koloru diody na czerwony

    def update_server_diode(self, running):
        if running:
            self.server_diode_canvas.config(bg='green')  # Zmiana koloru diody serwera na zielony
        else:
            self.server_diode_canvas.config(bg='red')  # Zmiana koloru diody serwera na czerwony

    async def start_server(self):
        print(f"Starting server on {self.host}:{self.port}")
        try:
            self.server = await asyncio.start_server(lambda r, w: ConnectionHandler(r, w, self.data_processor, self.data_storage, self).process_connection(), self.host, self.port)
            self.update_server_diode(True) 
            async with self.server:
                print(f"Serving on {self.server.sockets[0].getsockname()}")
                self.insert_message("Server has been started.\n")
                await self.data_storage.save_command(1, None, "start_server")
                await self.server.serve_forever()  
        except Exception as e:
            await self.data_storage.save_error(None, str(e))

    async def stop_server(self):
        if self.server:
            self.server.close()
            await self.server.wait_closed()
            self.server = None
            self.update_server_diode(False)  
            print("Server has been stopped.")
            self.insert_message("Server has been stopped.\n")
            await self.data_storage.save_command(1, None, "stop_server")

    async def fetch_and_plot_readings(self, probe_id, data_type):
        try:
            sensor_id = await self.data_storage.get_sensor_id(probe_id)
            if sensor_id:
                readings = await self.data_storage.get_probe_readings(sensor_id)  # Pobranie danych z bazy
                if readings:
                    readings = sorted(readings, key=lambda x: x['timestamp'], reverse=True)[:5]
                    timestamps = [record['timestamp'] for record in readings]
                    data_values = [record[data_type] for record in readings]
                    plt.figure(figsize=(10, 5))
                    plt.plot(timestamps, data_values, marker='o', color='red')
                    plt.title(f"{data_type.capitalize()} Data for {probe_id}")
                    plt.xlabel("Timestamp")
                    plt.ylabel(f"{data_type.capitalize()} Value")
                    plt.grid(True)
                    plt.show() 
                    await self.data_storage.save_command(1, probe_id, f"plot_{data_type}")
                else:
                    self.insert_message(f"No readings data found for {probe_id}.\n")
            else:
                self.insert_message(f"Sensor ID for probe {probe_id} not found.\n")
        except Exception as e:
            print(f"Error fetching data for {probe_id}: {e}")
            self.insert_message(f"Error fetching data for {probe_id}: {e}\n")
            await self.data_storage.save_error(probe_id, str(e))

    async def connect_probe(self, probe_id):
        if not self.probes[probe_id]['connected']:
            probe = ProbeSimulator(probe_id, (self.host, self.port), self)
            task = asyncio.create_task(probe.start_communication())  
            self.probes[probe_id]['connected'] = True
            self.probes[probe_id]['probe_instance'] = probe
            self.probes[probe_id]['task'] = task
            probe.start()  # Uruchomienie komunikacji
            self.update_diode(probe_id, True)
            await self.data_storage.save_command(1, probe_id, "connect")
            self.insert_message(f"{probe_id} connected.\n")
            print(f"{probe_id} connected.")
        else:
            self.insert_message(f"{probe_id} is already connected.\n")
            print(f"{probe_id} is already connected.")

    async def disconnect_probe(self, probe_id):
        if self.probes[probe_id]['connected']:
            probe = self.probes[probe_id]['probe_instance']
            task = self.probes[probe_id]['task']
            probe.stop()  # Zatrzymanie komunikacji
            task.cancel()
            await asyncio.gather(task, return_exceptions=True)
            self.probes[probe_id]['connected'] = False
            self.probes[probe_id]['probe_instance'] = None
            self.probes[probe_id]['task'] = None
            self.update_diode(probe_id, False)
            await self.data_storage.save_command(1, probe_id, "disconnect")
            self.insert_message(f"{probe_id} disconnected.\n")
            print(f"{probe_id} disconnected.")
        else:
            self.insert_message(f"{probe_id} is not connected.\n")
            print(f"{probe_id} is not connected.")

    async def connect_all_probes(self):
        tasks = [self.connect_probe(probe_id) for probe_id in self.probes.keys()]
        await asyncio.gather(*tasks)  # Połączenie wszystkich sond jednocześnie
        await self.data_storage.save_command(1, None, "connect_all_probes")  # Dodaj tę linię


    async def disconnect_all_probes(self):
        tasks = [self.disconnect_probe(probe_id) for probe_id in self.probes.keys()]
        await asyncio.gather(*tasks)  # Rozłączenie wszystkich sond jednocześnie
        await self.data_storage.save_command(1, None, "disconnect_all_probes")  # Dodaj tę linię

    def update_data(self, probe_id, data):
        self.temperature_labels[probe_id].config(text=f"Last Temp: {data['temperature']:.2f}°C")  # Aktualizacja etykiety temperatury

    def insert_message(self, message):
        if self.message_index >= len(self.messages_text):
            self.message_index = 0

        self.messages_text[self.message_index].insert(tk.END, message)
        self.messages_text[self.message_index].see(tk.END)

        if len(self.messages_text[self.message_index].get(1.0, tk.END)) > 2000:  
            self.message_index += 1

if __name__ == "__main__":
    root = tk.Tk()
    data_processor = None  
    data_storage = None  
    station = CommunicationStation('localhost', 8000, data_processor, data_storage, root)
    root.mainloop()
