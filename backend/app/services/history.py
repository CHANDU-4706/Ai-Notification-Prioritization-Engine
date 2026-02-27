import sqlite3
from datetime import datetime, timedelta
from app.database.db_init import DB_PATH

class HistoryService:
    def get_user_fatigue_score(self, user_id: str) -> float:
        """
        Calculates a fatigue score using an exponential decay model.
        Score = Sum( e^(-lambda * (now - t_i)) )
        Higher score means more 'spent' user attention.
        """
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Get notifications from the last 24 hours
        one_day_ago = (datetime.now() - timedelta(hours=24)).isoformat()
        cursor.execute("""
            SELECT created_at FROM audit_log 
            WHERE user_id = ? AND decision = 'NOW' AND created_at > ?
        """, (user_id, one_day_ago))
        
        timestamps = cursor.fetchall()
        conn.close()

        if not timestamps:
            return 0.0

        score = 0.0
        now = datetime.now()
        decay_constant = 0.1 # Adjust this to change how fast fatigue 'wears off'
        
        for (ts_str,) in timestamps:
            ts = datetime.fromisoformat(ts_str.replace(' ', 'T'))
            diff_hours = (now - ts).total_seconds() / 3600
            score += 2.71828 ** (-decay_constant * diff_hours)
            
        return score

    def get_event_frequency(self, user_id: str, event_type: str, minutes: int = 5) -> int:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        window = (datetime.now() - timedelta(minutes=minutes)).isoformat()
        
        cursor.execute("""
            SELECT COUNT(*) FROM audit_log 
            WHERE user_id = ? AND decision = 'NOW' AND created_at > ?
        """, (user_id, window))
        
        count = cursor.fetchone()[0]
        conn.close()
        return count
