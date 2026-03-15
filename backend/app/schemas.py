from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from .models import NodeStatus, SubscriptionTier

class NodeBase(BaseModel):
    zone_id: int
    battery_level: int = 100
    signal_strength: int = -50
    status: NodeStatus = NodeStatus.NOT_CONFIGURED

class NodeCreate(NodeBase):
    pass

class Node(NodeBase):
    id: int
    last_ping: datetime

    class Config:
        from_attributes = True

class ProjectBase(BaseModel):
    name: str
    client_id: int

class Project(ProjectBase):
    id: int
    class Config:
        from_attributes = True

class ClientBase(BaseModel):
    name: str
    subscription_tier: SubscriptionTier = SubscriptionTier.BASIC

class Client(ClientBase):
    id: int
    projects: List[Project] = []

    class Config:
        from_attributes = True
