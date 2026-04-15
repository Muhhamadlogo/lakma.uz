# AI-powered Telegram Mini App Store MVP

University project MVP: intelligent online clothing/accessories store with classic e-commerce flow and AI conversational agents.

## Project structure
- `backend/` — FastAPI + SQLAlchemy + PostgreSQL-ready REST API
- `frontend/` — React + Vite + TypeScript Telegram Mini App UI

## Quick start
### 1) Backend
```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --port 8000
```

### 2) Frontend
```bash
cd frontend
npm install
npm run dev
```

## Implemented API
- `GET /health`
- `GET /products`
- `GET /products/{id}`
- `POST /products`
- `GET /cart/{user_id}`
- `POST /cart/items`
- `PATCH /cart/items/{id}`
- `DELETE /cart/items/{id}`
- `POST /orders`
- `POST /chat`
- `GET /analytics/summary`
