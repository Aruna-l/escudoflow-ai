from typing import List, Optional
from pydantic import BaseModel


class DashboardKPIs(BaseModel):
    threatsToday: int
    threatsTodayDeltaPct: Optional[float] = None
    investigations: int
    investigationsDeltaPct: Optional[float] = None
    criticalAlerts: int
    criticalAlertsDeltaPct: Optional[float] = None
    blockedAttacks: int
    blockedAttacksDeltaPct: Optional[float] = None
    safeMessages: int
    safeMessagesDeltaPct: Optional[float] = None
    detectionAccuracy: float
    riskLevel: str
    avgInvestigationTimeSeconds: float

class ThreatTrendPoint(BaseModel):
    day: str
    threats: int
    blocked: int


class AttackCategory(BaseModel):
    name: str
    value: int


class DailyInvestigation(BaseModel):
    day: str
    investigations: int
    resolved: int


class RiskDistributionItem(BaseModel):
    name: str
    value: int


class ThreatSource(BaseModel):
    country: str
    value: int


class RecentInvestigation(BaseModel):
    id: str
    date: str
    source: str
    target: str
    threatType: str
    riskScore: int
    status: str


class Alert(BaseModel):
    id: str
    severity: str
    time: str
    title: str
    source: str


class AIFinding(BaseModel):
    title: str
    score: int
    detail: str


class DashboardSummary(BaseModel):
    kpis: DashboardKPIs
    threatTrend: List[ThreatTrendPoint]
    attackCategories: List[AttackCategory]
    dailyInvestigations: List[DailyInvestigation]
    riskDistribution: List[RiskDistributionItem]
    threatSources: List[ThreatSource]


class DashboardFeed(BaseModel):
    recentInvestigations: List[RecentInvestigation]
    alerts: List[Alert]


class DashboardInsights(BaseModel):
    findings: List[AIFinding]
    recommendations: List[str]