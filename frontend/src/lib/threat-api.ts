
import { getSessionId } from "./session-id";
const API_BASE = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

export type IOCType = "Domain" | "IP" | "URL" | "Hash" | "Email";

export interface ThreatFeedResult {
  name: string;
  verdict: string;
  malicious: boolean;
}

export interface ThreatIntelResponse {
  ioc: string;
  type: string;
  reputation: string;
  confidence: number;
  malwareFamily: string;
  knownCampaign: string;
  firstSeen: string;
  lastSeen: string;
  feeds: ThreatFeedResult[];
  actions: string[];
}

export class ThreatApiError extends Error {}

export async function analyzeIOC(ioc: string, type: IOCType): Promise<ThreatIntelResponse> {
  const res = await fetch(`${API_BASE}/api/threat/analyze`, {
    method: "POST",
    headers: { "Content-Type": "application/json", "X-Session-Id": getSessionId() },
    body: JSON.stringify({ ioc, type }),
  });

  if (!res.ok) {
    const body = await res.json().catch(() => null);
    throw new ThreatApiError(body?.detail || `Request failed with status ${res.status}`);
  }

  return res.json();
}

export function validateIOC(ioc: string, type: IOCType): string | null {
  const value = ioc.trim();
  if (!value) return "Please enter a value to search.";

  switch (type) {
    case "Domain": {
      const domainRegex = /^([a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$/;
      if (!domainRegex.test(value)) {
        return "Enter a valid domain, e.g. example.com";
      }
      return null;
    }
    case "IP": {
      const ipv4Regex = /^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$/;
      const match = value.match(ipv4Regex);
      if (!match || match.slice(1).some((octet) => Number(octet) > 255)) {
        return "Enter a valid IPv4 address, e.g. 185.220.101.1";
      }
      return null;
    }
    case "URL": {
      try {
        const parsed = new URL(value);
        if (!["http:", "https:"].includes(parsed.protocol)) {
          return "URL must start with http:// or https://";
        }
        return null;
      } catch {
        return "Enter a full URL, e.g. https://example.com/path";
      }
    }
    case "Hash": {
      const hashRegex = /^[a-fA-F0-9]{32}$|^[a-fA-F0-9]{40}$|^[a-fA-F0-9]{64}$/;
      if (!hashRegex.test(value)) {
        return "Enter a valid MD5 (32), SHA-1 (40), or SHA-256 (64) hex hash.";
      }
      return null;
    }
    case "Email": {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailRegex.test(value)) {
        return "Enter a valid email address, e.g. user@example.com";
      }
      return null;
    }
    default:
      return null;
  }
}