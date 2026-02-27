from fastapi import APIRouter, HTTPException
from app.models import NotificationEvent, DecisionResult
from app.engine.decision_engine import DecisionEngine
from app.services.audit import AuditService

router = APIRouter()
engine = DecisionEngine()
audit = AuditService()

@router.post("/notify", response_model=DecisionResult)
async def process_notification(event: NotificationEvent):
    try:
        result = await engine.process_event(event)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/audit")
async def get_audit_logs(limit: int = 50):
    return audit.get_logs(limit)

@router.get("/metrics")
async def get_metrics():
    # Basic metrics retrieval from audit logs
    logs = audit.get_logs(limit=1000)
    total = len(logs)
    if total == 0:
        return {"total": 0, "now_rate": 0, "later_rate": 0, "never_rate": 0}
    
    now = len([l for l in logs if l['decision'] == 'NOW'])
    later = len([l for l in logs if l['decision'] == 'LATER'])
    never = len([l for l in logs if l['decision'] == 'NEVER'])
    
    return {
        "total": total,
        "now": now,
        "now_rate": round(now/total * 100, 2),
        "later": later,
        "later_rate": round(later/total * 100, 2),
        "never": never,
        "never_rate": round(never/total * 100, 2)
    }

from app.services.rules_service import RulesService
from app.models import SuppressionRule

rules_service = RulesService()

@router.get("/rules")
async def list_rules():
    return rules_service.get_active_rules()

@router.post("/rules")
async def create_rule(rule: SuppressionRule):
    rules_service.add_rule(rule)
    return {"message": "Rule created successfully"}

@router.delete("/rules/{rule_id}")
async def delete_rule(rule_id: int):
    rules_service.delete_rule(rule_id)
    return {"message": f"Rule {rule_id} deleted"}
