import sqlite3

DB_PATH = 'safeflow.db'

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    print("Database connected...")

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS nodes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            floor INTEGER NOT NULL,
            is_exit INTEGER DEFAULT 0
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS edges (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            from_node INTEGER NOT NULL,
            to_node INTEGER NOT NULL,
            distance REAL NOT NULL,
            risk_level REAL DEFAULT 0.0,
            FOREIGN KEY (from_node) REFERENCES nodes(id),
            FOREIGN KEY (to_node) REFERENCES nodes(id)
        )
    ''')

    nodes_data = [
        ('Room 101', 1, 0),
        ('Room 102', 1, 0),
        ('Corridor A', 1, 0),
        ('Main Exit', 1, 1)
    ]
    cursor.executemany('INSERT OR IGNORE INTO nodes (name, floor, is_exit) VALUES (?, ?, ?)', nodes_data)

    edges_data = [
        (1, 3, 10.5, 0.2),
        (2, 3, 15.0, 0.1),
        (3, 4, 20.0, 0.0)
    ]
    cursor.executemany('INSERT OR IGNORE INTO edges (from_node, to_node, distance, risk_level) VALUES (?, ?, ?, ?)', edges_data)

    conn.commit()
    conn.close()
    print("✅ Database setup complete!")

if __name__ == '__main__':
    init_db()