from fastapi import FastAPI
from app.routes.health import router as health_router
from app.routes.url import router as url_router

app = FastAPI(
    title="EscudoFlow AI",
    description="Intelligent Phishing Detection & Threat Intelligence Platform",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "project": "EscudoFlow AI",
        "status": "Running"
    }


app.include_router(health_router)
app.include_router(url_router)