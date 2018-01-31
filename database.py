import sqlite3


class Database:
    def __init__(self, backing=None):
        if backing is None:
            backing = ':memory:'

        self.backing = backing
        self.connection = sqlite3.connect(backing)
        self.setup()

    def setup(self):
        self.connection.executescript("""
CREATE TABLE IF NOT EXISTS peers
(
  ip TEXT NOT NULL,
  port INT NOT NULL,
  last_seen DATETIME
);

CREATE UNIQUE INDEX IF NOT EXISTS peers_ip_port_uindex
  ON peers (ip, port);
""")
