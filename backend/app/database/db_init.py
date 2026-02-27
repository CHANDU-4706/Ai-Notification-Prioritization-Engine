import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "notifications.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Notifications and Events table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS notification_events (
        id TEXT PRIMARY KEY,
        user_id TEXT NOT NULL,
        event_type TEXT NOT NULL,
        message TEXT NOT NULL,
        source TEXT,
        priority_hint TEXT,
        channel TEXT,
        metadata TEXT,
        dedupe_key TEXT,
        expires_at DATETIME,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # Audit Log table for explainability
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS audit_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        event_id TEXT,
        user_id TEXT,
        decision TEXT, -- NOW, LATER, NEVER
        reason TEXT,
        engine_used TEXT,
        confidence REAL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(event_id) REFERENCES notification_events(id)
    )
    """)
    
    # Suppression Rules (Human-configurable)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS suppression_rules (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        rule_name TEXT UNIQUE,
        condition_field TEXT, -- e.g., 'source'
        condition_value TEXT, -- e.g., 'Promotional'
        action TEXT, -- NEVER, LATER
        is_active INTEGER DEFAULT 1
    )
    """)
    
    # User History / Counters for Fatigue
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS notification_history (
        user_id TEXT,
        event_type TEXT,
        last_sent_at DATETIME,
        sent_count_1h INTEGER DEFAULT 0,
        sent_count_24h INTEGER DEFAULT 0,
        PRIMARY KEY(user_id, event_type)
    )
    """)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print(f"Database initialized at {DB_PATH}")
