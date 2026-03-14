from sqlalchemy import Column, Integer, String, ForeignKey, Enum, DateTime, Float
from sqlalchemy.orm import relationship
from .database import Base
import enum
from datetime import datetime

# Enums for Type Safety [cite: 120]
class NodeStatus(enum.Enum):
    NOT_CONFIGURED = "NOT_CONFIGURED"
    CONFIGURED = "CONFIGURED"
    MONITOR = "MONITOR"
    SLEEP = "SLEEP"

class SubscriptionTier(enum.Enum):
    BASIC = "Basic"
    PLUS = "Plus"
    PRO = "Pro"
    PREMIUM = "Premium"

# The Hierarchy [cite: 107-115]
class Client(Base):
    __tablename__ = "clients"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    subscription_tier = Column(Enum(SubscriptionTier), default=SubscriptionTier.BASIC)
    projects = relationship("Project", back_populates="client")

class Project(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    client_id = Column(Integer, ForeignKey("clients.id"))
    client = relationship("Client", back_populates="projects")
    zones = relationship("Zone", back_populates="project")

class Zone(Base):
    __tablename__ = "zones"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    project_id = Column(Integer, ForeignKey("projects.id"))
    project = relationship("Project", back_populates="zones")
    nodes = relationship("Node", back_populates="zone")

class Node(Base):
    __tablename__ = "nodes"
    id = Column(Integer, primary_key=True, index=True)
    zone_id = Column(Integer, ForeignKey("zones.id"))
    status = Column(Enum(NodeStatus), default=NodeStatus.NOT_CONFIGURED)
    battery_level = Column(Integer, default=100) # [cite: 39]
    signal_strength = Column(Integer, default=-50) # [cite: 39]
    last_ping = Column(DateTime, default=datetime.utcnow) # [cite: 39]

    zone = relationship("Zone", back_populates="nodes")

class DataFile(Base):
    __tablename__ = "data_files"
    id = Column(Integer, primary_key=True)
    filename = Column(String)
    upload_date = Column(DateTime, default=datetime.utcnow)
    node_id = Column(Integer, ForeignKey("nodes.id"))
