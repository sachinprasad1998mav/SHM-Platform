from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models

router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.get("/{node_id}")
async def get_node_analytics(
    node_id: int,
    tier: str = Query(..., description="User subscription tier"),
    db: Session = Depends(get_db)
):
    # 1. Verify node exists in the database
    db_node = db.query(models.Node).filter(models.Node.id == node_id).first()
    if not db_node:
        raise HTTPException(status_code=404, detail="Node not found")

    # 2. Implement Tiered Logic [cite: 71-77]
    tier = tier.lower()
    response_data = {
        "node_id": node_id,
        "subscription_tier": tier,
    }

    if tier == "basic":
        # Basic unlocks Current Status
        response_data["current_status"] = db_node.status.value

    elif tier == "plus":
        # Plus unlocks Historical Data
        response_data["history"] = [
            {"timestamp": "2026-03-01T10:00:00Z", "battery": 80},
            {"timestamp": "2026-03-01T11:00:00Z", "battery": 78}
        ]

    elif tier == "pro":
        # Pro unlocks Trend Analytics
        response_data["trends"] = {"signal_stability": "High", "battery_drain": "0.5%/day"}

    elif tier == "premium":
        # Premium unlocks Predictive Alerts
        response_data["predictive_alert"] = "No structural failure predicted for 180 days."

    else:
        raise HTTPException(status_code=400, detail="Invalid subscription tier")

    return response_data
