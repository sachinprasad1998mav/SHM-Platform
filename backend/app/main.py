from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from .database import engine, Base, get_db
from . import models
from .routes import nodes, projects, analytics # Clean single-line import
import asyncio
import json
import redis.asyncio as aioredis
from .websocket_manager import manager

# Create tables [cite: 106]
Base.metadata.create_all(bind=engine)
redis_client = aioredis.from_url("redis://localhost:6379", encoding="utf-8", decode_responses=True)

app = FastAPI(title="Nirixense SHM Platform")

# Registering the different modules [cite: 27]
app.include_router(nodes.router)
app.include_router(projects.router)
app.include_router(analytics.router)

@app.get("/")
def health_check(db: Session = Depends(get_db)):
    try:
        # Check DB connectivity
        db.execute(text("SELECT 1"))
        return {
            "status": "online",
            "database": "connected",
            "message": "Day 1 Complete: Database, CRUD, and Lifecycle Logic are live."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection failed: {str(e)}")


async def redis_listener():
    """Listens to Redis 'node_updates' channel and broadcasts to WebSockets."""
    pubsub = redis_client.pubsub()
    await pubsub.subscribe("node_updates")

    try:
        while True:
            message = await pubsub.get_message(ignore_subscribe_messages=True)
            if message:
                data = json.loads(message["data"])
                await manager.broadcast(data)
            await asyncio.sleep(0.01) # Prevent CPU hogging
    except Exception as e:
        print(f"Redis Listener Error: {e}")

@app.on_event("startup")
async def startup_event():
    # Start the Redis listener in the background when the app starts
    asyncio.create_task(redis_listener())
