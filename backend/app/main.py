from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text
from .database import engine, Base, get_db
from . import models
from .routes import nodes, projects, analytics
import asyncio
import json
import redis.asyncio as aioredis
from .websocket_manager import manager

Base.metadata.create_all(bind=engine)
redis_client = aioredis.from_url("redis://localhost:6379", encoding="utf-8", decode_responses=True)

app = FastAPI(title="Nirixense SHM Platform")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(nodes.router)
app.include_router(projects.router)
app.include_router(analytics.router)

@app.get("/")
def health_check(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {
            "status": "online",
            "database": "connected",
            "message": "Day 1 Complete: Database, CRUD, and Lifecycle Logic are live."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection failed: {str(e)}")


async def redis_listener():
    pubsub = redis_client.pubsub()
    await pubsub.subscribe("node_updates")

    try:
        while True:
            message = await pubsub.get_message(ignore_subscribe_messages=True)
            if message:
                data = json.loads(message["data"])
                await manager.broadcast(data)
            await asyncio.sleep(0.01)
    except Exception as e:
        print(f"Redis Listener Error: {e}")

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(redis_listener())
