from fastapi import FastAPI
from app.api.v1 import auth
from app.db.session import engine, Base
from datetime import datetime


Base.metadata.create_all(bind=engine)


app = FastAPI(title="Auth Service")
app.include_router(auth.router)


@app.get("/health")
async def health():
    return {"status": "ok", "time": datetime.utcnow().isoformat()}