from sqlalchemy.orm import Session
from . import models, schemas
from datetime import datetime
from . import models

# Logic to get all nodes [cite: 105]
def get_nodes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Node).offset(skip).limit(limit).all()

# Logic to create a new node [cite: 47]
def create_node(db: Session, node: schemas.NodeCreate):
    db_node = models.Node(**node.model_dump())
    db.add(db_node)
    db.commit()
    db.refresh(db_node)
    return db_node

# Logic for Zones [cite: 33]
def create_zone(db: Session, zone: schemas.ProjectBase, project_id: int):
    db_zone = models.Zone(name=zone.name, project_id=project_id)
    db.add(db_zone)
    db.commit()
    db.refresh(db_zone)
    return db_zone

# Logic to update a Node's state [cite: 40-57]
def update_node_status(db: Session, node_id: int, status: models.NodeStatus):
    db_node = db.query(models.Node).filter(models.Node.id == node_id).first()
    if db_node:
        db_node.status = status
        db_node.last_ping = datetime.utcnow()
        db.commit()
        db.refresh(db_node)
    return db_node



def transition_node_state(db: Session, node_id: int, event: str):
    db_node = db.query(models.Node).filter(models.Node.id == node_id).first()
    if not db_node:
        return None

    # Implement the Lifecycle Logic
    if event == "setup_wifi" and db_node.status == models.NodeStatus.NOT_CONFIGURED:
        db_node.status = models.NodeStatus.CONFIGURED

    elif event == "activate_lora" and db_node.status == models.NodeStatus.CONFIGURED:
        # Simplified: In a real app, we'd check if it's "selected" [cite: 50]
        db_node.status = models.NodeStatus.MONITOR

    elif event == "deactivate" and db_node.status == models.NodeStatus.MONITOR:
        db_node.status = models.NodeStatus.SLEEP

    db_node.last_ping = datetime.utcnow()
    db.commit()
    db.refresh(db_node)
    return db_node
