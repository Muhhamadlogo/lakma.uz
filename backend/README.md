# Backend (FastAPI)

## Run
```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --port 8000
```

## Endpoints
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
