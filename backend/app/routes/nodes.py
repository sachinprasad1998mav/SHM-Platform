from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from ..database import get_db
from .. import crud, models, schemas
from ..websocket_manager import manager
import json

router = APIRouter(prefix="/nodes", tags=["Nodes"])

@router.post("/", response_model=schemas.Node)
def create_node(node: schemas.NodeCreate, db: Session = Depends(get_db)):
    return crud.create_node(db=db, node=node)

@router.get("/", response_model=List[schemas.Node])
def read_nodes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    nodes = crud.get_nodes(db, skip=skip, limit=limit)
    return nodes

@router.patch("/{node_id}/ping")
async def node_ping(
    node_id: int,
    battery: int,
    signal: int,
    db: Session = Depends(get_db)
):
    db_node = db.query(models.Node).filter(models.Node.id == node_id).first()
    if not db_node:
        raise HTTPException(status_code=404, detail="Node not found")

    db_node.battery_level = battery
    db_node.signal_strength = signal
    db_node.last_ping = datetime.utcnow()
    db.commit()


    try:
        await redis_client.publish("node_updates", json.dumps(update_data))
    except Exception as e:
        print(f"⚠️ Redis Broadcast failed: {e}")
    update_data = {
        "id": db_node.id,
        "status": db_node.status.value,
        "battery_level": db_node.battery_level,
        "signal_strength": db_node.signal_strength,
        "last_ping": db_node.last_ping.isoformat()
    }

    from ..main import redis_client
    await redis_client.publish("node_updates", json.dumps(update_data))

    return {"message": "Ping received and broadcasted", "data": update_data}

@router.websocket("/ws/nodes")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)
