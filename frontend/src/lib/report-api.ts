import { getSessionId } from "./session-id";

const API_BASE = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

export interface IOCItem {
  type: string;
  value: string;
}

export interface TimelineEvent {
  t: string;
  event: string;
}

export interface ThreatOverview {
  vector: string;
  target: string;
  impact: string;
}

export interface EvidenceItem {
  filename: string;
  sourceType: string;
}

export interface ReportResponse {
  id: string;
  title: string;
  createdAt: string;
  analyst: string;
  severity: "Critical" | "High" | "Suspicious" | "Low" | "Safe";
  riskScore: number;
  confidence: number;
  executiveSummary: string;
  threatOverview: ThreatOverview;
  iocs: IOCItem[];
  timeline: TimelineEvent[];
  recommendations: string[];
  evidence: EvidenceItem[];
  analystNotes: string | null;
}

export class ReportApiError extends Error {}

async function handle<T>(res: Response): Promise<T> {
  if (!res.ok) {
    const body = await res.json().catch(() => null);
    throw new ReportApiError(body?.detail || `Request failed with status ${res.status}`);
  }
  return res.json();
}

export async function getLatestReport(): Promise<ReportResponse> {
  const res = await fetch(`${API_BASE}/report/latest`, {
    headers: { "X-Session-Id": getSessionId() },
    cache: "no-store",
  });
  return handle<ReportResponse>(res);
}

export async function updateReportNotes(id: string, notes: string): Promise<ReportResponse> {
  const res = await fetch(`${API_BASE}/report/${id}/notes`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json", "X-Session-Id": getSessionId() },
    body: JSON.stringify({ notes }),
  });
  return handle<ReportResponse>(res);
}

export function exportReportUrl(id: string, format: "csv" | "json" | "pdf"): string {
  return `${API_BASE}/report/${id}/export/${format}`;
}