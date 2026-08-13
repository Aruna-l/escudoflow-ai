import { getSessionId } from "./session-id";
const API_BASE = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

export interface DashboardKPIs {
  threatsToday: number;
  threatsTodayDeltaPct: number | null;
  investigations: number;
  investigationsDeltaPct: number | null;
  criticalAlerts: number;
  criticalAlertsDeltaPct: number | null;
  blockedAttacks: number;
  blockedAttacksDeltaPct: number | null;
  safeMessages: number;
  safeMessagesDeltaPct: number | null;
  detectionAccuracy: number;
  riskLevel: string;
  avgInvestigationTimeSeconds: number;
}

export interface ThreatTrendPoint { day: string; threats: number; blocked: number; }
export interface AttackCategory { name: string; value: number; }
export interface DailyInvestigation { day: string; investigations: number; resolved: number; }
export interface RiskDistributionItem { name: string; value: number; }
export interface ThreatSource { country: string; value: number; }

export interface DashboardSummary {
  kpis: DashboardKPIs;
  threatTrend: ThreatTrendPoint[];
  attackCategories: AttackCategory[];
  dailyInvestigations: DailyInvestigation[];
  riskDistribution: RiskDistributionItem[];
  threatSources: ThreatSource[];
}

export interface RecentInvestigation {
  id: string;
  date: string;
  source: string;
  target: string;
  threatType: string;
  riskScore: number;
  status: string;
}

export interface DashboardAlert {
  id: string;
  severity: string;
  time: string;
  title: string;
  source: string;
}

export interface DashboardFeed {
  recentInvestigations: RecentInvestigation[];
  alerts: DashboardAlert[];
}

export interface AIFinding { title: string; score: number; detail: string; }

export interface DashboardInsights {
  findings: AIFinding[];
  recommendations: string[];
}

export class DashboardApiError extends Error {}

async function getJSON<T>(path: string): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    headers: { "X-Session-Id": getSessionId() },
  });

  if (!res.ok) {
    const body = await res.json().catch(() => null);
    throw new DashboardApiError(body?.detail || `Request failed with status ${res.status}`);
  }

  return res.json();
}

export const getDashboardSummary = () => getJSON<DashboardSummary>("/api/dashboard/summary");
export const getDashboardFeed = () => getJSON<DashboardFeed>("/api/dashboard/feed");
export const getDashboardInsights = () => getJSON<DashboardInsights>("/api/dashboard/insights");

export interface KpiCard {
  label: string;
  value: string;
  delta?: string;
  tone: "primary" | "cyan" | "success" | "warning" | "danger";
}

function fmtDelta(pct: number | null): string | undefined {
  if (pct === null || pct === undefined) return undefined;
  return `${pct >= 0 ? "+" : ""}${pct.toFixed(1)}%`;
}

function riskLevelTone(level: string): KpiCard["tone"] {
  if (level === "Critical") return "danger";
  if (level === "Elevated") return "warning";
  return "success";
}

export function formatKpiCards(kpis: DashboardKPIs): KpiCard[] {
  return [
    { label: "Threats Today", value: kpis.threatsToday.toLocaleString(), delta: fmtDelta(kpis.threatsTodayDeltaPct), tone: "danger" },
    { label: "Investigations", value: kpis.investigations.toLocaleString(), delta: fmtDelta(kpis.investigationsDeltaPct), tone: "primary" },
    { label: "Critical Alerts", value: kpis.criticalAlerts.toLocaleString(), delta: fmtDelta(kpis.criticalAlertsDeltaPct), tone: "danger" },
    { label: "Blocked Attacks", value: kpis.blockedAttacks.toLocaleString(), delta: fmtDelta(kpis.blockedAttacksDeltaPct), tone: "success" },
    { label: "Safe Messages", value: kpis.safeMessages.toLocaleString(), delta: fmtDelta(kpis.safeMessagesDeltaPct), tone: "success" },
    { label: "Detection Accuracy", value: `${kpis.detectionAccuracy}%`, tone: "cyan" }, // static model metric — no live delta, see backend note
    { label: "Risk Level", value: kpis.riskLevel, delta: "24h", tone: riskLevelTone(kpis.riskLevel) },
    { label: "Avg Investigation Time", value: `${kpis.avgInvestigationTimeSeconds}s`, tone: "primary" }, // constant until per-call latency is tracked
  ];
}