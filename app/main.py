from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.db import init_db
from app.routers import auth as auth_router
from app.routers import qe_proxy as qe_router

app = FastAPI(title=settings.APP_NAME, version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.CORS_ORIGINS] if settings.CORS_ORIGINS != "*" else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    init_db()

app.include_router(auth_router.router)
app.include_router(qe_router.router)

@app.get("/")
def root():
    return {"ok": True, "app": settings.APP_NAME}

@app.get("/_ah/health")
def healthz():
    return {"ok": True, "env": settings.ENV}
