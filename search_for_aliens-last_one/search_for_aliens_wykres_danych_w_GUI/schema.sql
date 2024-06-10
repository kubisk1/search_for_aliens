CREATE TABLE IF NOT EXISTS temperatures (
    id SERIAL PRIMARY KEY,
    probe_id VARCHAR(50),
    temperature FLOAT,
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
