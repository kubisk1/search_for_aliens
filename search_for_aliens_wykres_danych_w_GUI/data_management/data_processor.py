class DataProcessor:
    def __init__(self):
        pass

    def extract_metadata(self, data):
        # Przyjmuję, że dane są w formacie "probe_id,temperature"
        decoded_data = data.decode()
        probe_id, temperature = decoded_data.split(',')
        return probe_id, float(temperature)

    def verify_data(self, data):
        # Zakładamy, że dane są zawsze poprawne
        return True




