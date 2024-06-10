CREATE TABLE photos (
    id SERIAL PRIMARY KEY,
    probe_id INTEGER NOT NULL,
    zdjecie BYTEA,
    data_wyslania TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE temperatures (
    id SERIAL PRIMARY KEY,
    probe_id INTEGER NOT NULL,
    temperature NUMERIC,
    data_wys TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS temperatures (
    id SERIAL PRIMARY KEY,
    probe_id VARCHAR(50) NOT NULL,
    temperature NUMERIC,
    data_wys TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);