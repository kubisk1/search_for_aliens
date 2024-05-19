class DataProcessor:
    def __init__(self):
        pass

    def extract_metadata(self, data):
        # Przyjmuję, że dane zawierają metadane jako pierwszy bajt
        probe_id = data[0]
        image_chunk = data[1:]
        return probe_id, image_chunk

    def verify_data(self, data):
        # Sprawdza, czy dane mają odpowiednią długość (zakładam 1024 bajty dla pełnego zdjęcia)
        return len(data) == 1024



