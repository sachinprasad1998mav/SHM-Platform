# Nirixense SHM Mini-Platform

A real-time Structural Health Monitoring (SHM) dashboard built with a high-performance Python/React stack.

## 🚀 Tech Stack
- **Backend:** FastAPI (Python 3.11)
- **Database:** PostgreSQL with SQLAlchemy ORM
- **Real-Time Hub:** Redis Pub/Sub & WebSockets
- **Frontend:** React + Vite + Tailwind CSS
- **Visuals:** Recharts (Live Trends) & Lucide-React (Icons)

## 🏗️ Architectural Thinking
- **Event-Driven Updates:** Instead of the frontend polling the database, I implemented a Redis Pub/Sub architecture. When a node pings the API, the backend publishes an event to Redis, which then broadcasts via WebSockets to all connected clients for instant UI updates.
- **Relational Integrity:** Designed a strict Client -> Project -> Zone -> Node hierarchy to ensure data scalability.
- **State Machine Logic:** Nodes follow a strictly defined lifecycle (Enum-based) to maintain monitoring consistency.

## 🛠️ How to Run
1. **Backend:** - `cd backend && source venv/bin/activate`
   - `pip install -r requirements.txt`
   - `python3 test_db.py` (to seed initial client/project data)
   - `uvicorn app.main:app --reload`
2. **Infrastructure:** - Ensure `redis-server` is running on `localhost:6379`.
3. **Frontend:**
   - `cd frontend && npm install && npm run dev`


   
