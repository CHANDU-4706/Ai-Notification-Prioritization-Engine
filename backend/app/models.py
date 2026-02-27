from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime
import uuid

class NotificationEvent(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    event_type: str
    message: str
    source: Optional[str] = "unknown"
    priority_hint: Optional[str] = "medium"
    channel: Optional[str] = "in-app"
    metadata: Optional[Dict[str, Any]] = {}
    dedupe_key: Optional[str] = None
    expires_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.now)

class DecisionResult(BaseModel):
    event_id: str
    user_id: str
    decision: str  # NOW, LATER, NEVER
    reason: str
    engine_used: str # GROQ_LLAMA, RULE_ENGINE, FALLBACK
    score: float = 0.0
    confidence: float = 0.0

class SuppressionRule(BaseModel):
    id: Optional[int] = None
    rule_name: str
    condition_field: str
    condition_value: str
    action: str
