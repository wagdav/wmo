DROP TABLE IF EXISTS wmo;
CREATE TABLE wmo(
    id SERIAL PRIMARY KEY,
    url TEXT,
    status_code INT,
    response_time REAL,
    pattern TEXT,
    matches TEXT
);
