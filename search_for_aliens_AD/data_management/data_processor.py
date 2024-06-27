class DataProcessor:
    def __init__(self):
        pass

    def extract_metadata(self, data):
        decoded_data = data.decode()  # Dekodowanie danych
        fields = decoded_data.split(',')
        probe_id = fields[0]
        temperature = float(fields[1])
        humidity = float(fields[2])
        visibility = float(fields[3])
        passengers_count = int(fields[4])
        pressure = float(fields[5])
        return {
            'probe_id': probe_id,
            'temperature': temperature,
            'humidity': humidity,
            'visibility': visibility,
            'passengers_count': passengers_count,
            'pressure': pressure
        }

    def verify_data(self, data):
        return True 
