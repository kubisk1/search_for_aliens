class DataProcessor:
    def __init__(self):
        pass

    def extract_metadata(self, data):
        decoded_data = data.decode()  # Dekodowanie danych
        probe_id, temperature = decoded_data.split(',')
        return probe_id, float(temperature)  # Zwrot przetworzonych danych

    def verify_data(self, data):
        return True 




