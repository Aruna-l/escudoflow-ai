
from contextlib import asynccontextmanager
 
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
 
from app.core.config import settings
from app.database import ensure_indexes
 
from app.api.auth import router as auth_router
from app.routes.health import router as health_router
from app.routes.url import router as url_router
from app.routes.email import router as email_router
from app.routes.visual import router as visual_router
from app.routes.attachment import router as attachment_router
from app.routes.threat import router as threat_router
from app.routes.reports import router as reports_router
from app.routes.settings import router as settings_router
from app.api.auth_password_reset import router as password_reset_router
from app.routes import dashboard


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Runs once on startup
    await ensure_indexes()
    yield
    # (place any shutdown/cleanup code here if needed later)
 
 
app = FastAPI(
    title="EscudoFlow AI",
    description="Intelligent Phishing Detection & Threat Intelligence Platform",
    version="1.0.0",
    lifespan=lifespan,
)
 
 
@app.get("/")
def home():
    return {
        "project": "EscudoFlow AI",
        "status": "Running"
    }
 
 
app.include_router(health_router)
app.include_router(auth_router)
app.include_router(url_router)
app.include_router(email_router)
app.include_router(visual_router)
app.include_router(attachment_router)
app.include_router(threat_router, prefix="/api")
app.include_router(reports_router)
app.include_router(settings_router)
app.include_router(password_reset_router)
app.include_router(dashboard.router, prefix="/api")


app.add_middleware(
    CORSMiddleware,
    allow_origins=list(set(
        settings.cors_origin_list
        + [
            "http://localhost:8080",
            "http://127.0.0.1:8080",
        ]
    )),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)