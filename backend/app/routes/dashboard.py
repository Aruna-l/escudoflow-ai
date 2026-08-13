from fastapi import APIRouter, HTTPException
from app.schemas.dashboard import DashboardSummary, DashboardFeed, DashboardInsights
from app.services.dashboard import dashboard_service

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/summary", response_model=DashboardSummary)
async def get_summary():
    try:
        return {
            "kpis": dashboard_service.compute_kpis(),
            "threatTrend": dashboard_service.compute_threat_trend(),
            "attackCategories": dashboard_service.compute_attack_categories(),
            "dailyInvestigations": dashboard_service.compute_daily_investigations(),
            "riskDistribution": dashboard_service.compute_risk_distribution(),
            "threatSources": dashboard_service.compute_threat_sources(),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/feed", response_model=DashboardFeed)
async def get_feed():
    try:
        return {
            "recentInvestigations": dashboard_service.compute_recent_investigations(),
            "alerts": dashboard_service.compute_alerts(),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/insights", response_model=DashboardInsights)
async def get_insights():
    try:
        return dashboard_service.compute_insights()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))