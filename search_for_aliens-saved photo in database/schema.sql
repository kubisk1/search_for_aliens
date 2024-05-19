CREATE TABLE photos (
    id SERIAL PRIMARY KEY,
    probe_id INTEGER NOT NULL,
    zdjecie BYTEA,
    data_wyslania TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
