CREATE TABLE IF NOT EXISTS alerts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    datetime REAL,
    domain TEXT NOT NULL,
    criticity TEXT NOT NULL,
    issuer TEXT NOT NULL
);
