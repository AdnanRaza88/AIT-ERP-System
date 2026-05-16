from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.config import settings
from backend.database.session import engine, Base
from backend.database import seed
from backend.routes import (
    auth, students, teachers, admissions, attendance,
    fees, exams, courses, hr, analytics, chatbot
)

Base.metadata.create_all(bind=engine)
seed.seed()

app = FastAPI(title="AiT ERP API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

for r in [auth, students, teachers, admissions, attendance,
          fees, exams, courses, hr, analytics, chatbot]:
    app.include_router(r.router)


@app.get("/")
def root():
    return {"service": "AiT ERP API", "status": "online"}