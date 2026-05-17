from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers import api, dashboard

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="DocuForge API",
    description="Document processing API — Excel, CSV, PDF automation for developers",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api.router)
app.include_router(dashboard.router)
