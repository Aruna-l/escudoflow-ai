import { getSessionId } from "./session-id";

const API_BASE = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";

export interface ThreatItem {
  name: string;
  severity: "safe" | "low" | "suspicious" | "high" | "critical";
}

export interface AttachmentAnalysis {
  riskScore: number;
  riskLabel: string;
  fileName: string;
  fileType: string;
  size: string;
  macros: boolean;
  embeddedScripts: number;
  suspiciousExecutables: number;
  sha256: string;
  threats: ThreatItem[];
  recommendation: string;
}

export async function analyzeAttachment(file: File): Promise<AttachmentAnalysis> {
  const formData = new FormData();
  formData.append("file", file);

  const res = await fetch(`${API_BASE}/attachment/analyze`, {
    method: "POST",
    headers: { "X-Session-Id": getSessionId() },
    body: formData,
  });

  if (!res.ok) {
    const body = await res.json().catch(() => null);
    throw new Error(body?.detail ?? `Analysis failed (${res.status})`);
  }

  return res.json();
}