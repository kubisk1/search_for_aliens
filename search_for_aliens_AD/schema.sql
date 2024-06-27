CREATE TABLE temperatures (
    id SERIAL PRIMARY KEY,
    probe_id INTEGER NOT NULL,
    temperature NUMERIC,
    data_wys TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

