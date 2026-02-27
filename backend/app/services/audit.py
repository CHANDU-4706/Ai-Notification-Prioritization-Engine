import sqlite3
import os
from app.models import DecisionResult, NotificationEvent
from app.database.db_init import DB_PATH

class AuditService:
    def log_event(self, event: NotificationEvent):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO notification_events (id, user_id, event_type, message, source, priority_hint, channel, metadata, dedupe_key, expires_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            event.id, event.user_id, event.event_type, event.message,
            event.source, event.priority_hint, event.channel,
            str(event.metadata), event.dedupe_key,
            event.expires_at.isoformat() if event.expires_at else None
        ))
        conn.commit()
        conn.close()

    def log_decision(self, result: DecisionResult):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO audit_log (event_id, user_id, decision, reason, engine_used, confidence)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            result.event_id, result.user_id, result.decision,
            result.reason, result.engine_used, result.confidence
        ))
        conn.commit()
        conn.close()

    def get_logs(self, limit: int = 50):
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("""
            SELECT al.*, ne.message, ne.event_type 
            FROM audit_log al
            JOIN notification_events ne ON al.event_id = ne.id
            ORDER BY al.created_at DESC
            LIMIT ?
        """, (limit,))
        logs = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return logs
