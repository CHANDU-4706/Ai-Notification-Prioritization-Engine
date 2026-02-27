import sqlite3
import os
from typing import List, Optional
from app.models import NotificationEvent, DecisionResult, SuppressionRule
from app.database.db_init import DB_PATH

class RulesService:
    def get_active_rules(self) -> List[SuppressionRule]:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM suppression_rules WHERE is_active = 1")
        rules = [SuppressionRule(**dict(row)) for row in cursor.fetchall()]
        conn.close()
        return rules

    def evaluate_rules(self, event: NotificationEvent) -> Optional[DecisionResult]:
        rules = self.get_active_rules()
        for rule in rules:
            field_value = getattr(event, rule.condition_field, None)
            if field_value and str(field_value).lower() == rule.condition_value.lower():
                return DecisionResult(
                    event_id=event.id,
                    user_id=event.user_id,
                    decision=rule.action,
                    reason=f"Matched suppression rule: {rule.rule_name}",
                    engine_used="RULE_ENGINE",
                    confidence=1.0
                )
        return None

    def add_rule(self, rule: SuppressionRule):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO suppression_rules (rule_name, condition_field, condition_value, action)
            VALUES (?, ?, ?, ?)
        """, (rule.rule_name, rule.condition_field, rule.condition_value, rule.action))
        conn.commit()
        conn.close()

    def delete_rule(self, rule_id: int):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM suppression_rules WHERE id = ?", (rule_id,))
        conn.commit()
        conn.close()
