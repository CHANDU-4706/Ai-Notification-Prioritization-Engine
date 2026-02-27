import asyncio
from datetime import datetime
from app.models import NotificationEvent, DecisionResult
from app.engine.classifier import ClassifierService
from app.engine.semantic_dedup import SemanticDeduplicator
from app.services.audit import AuditService
from app.services.history import HistoryService

class DecisionEngine:
    def __init__(self):
        self.classifier = ClassifierService()
        self.deduplicator = SemanticDeduplicator()
        self.audit = AuditService()
        self.history = HistoryService()

    async def process_event(self, event: NotificationEvent) -> DecisionResult:
        # 1. Validation & Pre-logging
        self.audit.log_event(event)

        # 2. Expiry Check
        if event.expires_at and event.expires_at < datetime.now():
            result = DecisionResult(
                event_id=event.id,
                user_id=event.user_id,
                decision="NEVER",
                reason="Event already expired",
                engine_used="RULE_ENGINE"
            )
            self.audit.log_decision(result)
            return result

        # 3. Exact & Semantic Deduplication
        # (In a real system, we'd use the dedupe_key if provided)
        duplicate_text = self.deduplicator.is_duplicate(event)
        if duplicate_text:
            result = DecisionResult(
                event_id=event.id,
                user_id=event.user_id,
                decision="NEVER",
                reason=f"Semantic duplicate of recent message: '{duplicate_text[:50]}...'",
                engine_used="SEMANTIC_DEDUP",
                confidence=0.98
            )
            self.audit.log_decision(result)
            return result

        # 4. AI Classification (Groq/Llama)
        # We start this early as it's the most expensive part
        ai_task = asyncio.create_task(self.classifier.classify(event))

        # 5. Smart Fatigue & Frequency Caps (ML-Driven)
        fatigue_score = self.history.get_user_fatigue_score(event.user_id)
        # Thresholds: >5 is noisy, >10 is very fatigued
        
        # 6. Final Decision Integration
        try:
            ai_result = await ai_task
            
            # Post-processing AI decision with fatigue context
            if ai_result.decision == "NOW":
                # Only let crucial alerts through if user is extremely fatigued
                if fatigue_score > 8.0 and event.priority_hint != "critical":
                    ai_result.decision = "LATER"
                    ai_result.reason += f" (Downgraded due to high fatigue score: {fatigue_score:.2f})"
                elif fatigue_score > 12.0:
                    ai_result.decision = "NEVER"
                    ai_result.reason += " (Suppressed: User is overloaded)"

            # Update deduplicator with the message if actually sent
            if ai_result.decision == "NOW":
                self.deduplicator.add_to_history(event)

            self.audit.log_decision(ai_result)
            return ai_result

        except Exception as e:
            fallback = DecisionResult(
                event_id=event.id,
                user_id=event.user_id,
                decision="NOW" if event.priority_hint == "critical" else "LATER",
                reason=f"System Error: {str(e)}",
                engine_used="FALLBACK"
            )
            self.audit.log_decision(fallback)
            return fallback
