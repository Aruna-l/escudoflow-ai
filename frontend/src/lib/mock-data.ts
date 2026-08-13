// Centralized mock data for EscudoFlow AI.
// Every export is shaped like an API response so it can be swapped
// for a FastAPI endpoint without changing consuming components.

export type RiskLevel = "safe" | "low" | "suspicious" | "high" | "critical";

export interface Investigation {
  id: string;
  date: string;
  source: string;
  target: string;
  threatType: string;
  riskScore: number;
  status: "resolved" | "investigating" | "blocked" | "escalated";
}

export interface Alert {
  id: string;
  title: string;
  severity: RiskLevel;
  time: string;
  source: string;
}

export const HOMEPAGE_STATS = [
  { label: "Threats Detected", value: 1_284_302, suffix: "+" },
  { label: "Emails Investigated", value: 8_942_115, suffix: "+" },
  { label: "URLs Analyzed", value: 12_640_892, suffix: "+" },
  { label: "Organizations Protected", value: 2_413, suffix: "+" },
  { label: "Avg Detection Time", value: 1.8, suffix: "s" },
  { label: "Detection Accuracy", value: 99.4, suffix: "%" },
];

export const DASHBOARD_KPIS = [
  { label: "Threats Today", value: "342", delta: "+12.4%", tone: "danger" as const },
  { label: "Investigations", value: "1,284", delta: "+3.1%", tone: "primary" as const },
  { label: "Critical Alerts", value: "27", delta: "-8.0%", tone: "danger" as const },
  { label: "Blocked Attacks", value: "612", delta: "+18.2%", tone: "success" as const },
  { label: "Safe Messages", value: "94,120", delta: "+2.4%", tone: "success" as const },
  { label: "Detection Accuracy", value: "99.4%", delta: "+0.2%", tone: "cyan" as const },
  { label: "Risk Level", value: "Elevated", delta: "24h", tone: "warning" as const },
  { label: "Avg Investigation Time", value: "1.8s", delta: "-0.3s", tone: "primary" as const },
];

export const THREAT_TREND = Array.from({ length: 14 }).map((_, i) => ({
  day: `D${i + 1}`,
  threats: Math.round(180 + Math.sin(i / 2) * 60 + Math.random() * 90),
  blocked: Math.round(140 + Math.cos(i / 2) * 40 + Math.random() * 70),
}));

export const ATTACK_CATEGORIES = [
  { name: "Credential Phishing", value: 38 },
  { name: "BEC", value: 22 },
  { name: "Malware", value: 16 },
  { name: "Brand Impersonation", value: 14 },
  { name: "Callback / Vishing", value: 6 },
  { name: "Other", value: 4 },
];

export const DAILY_INVESTIGATIONS = Array.from({ length: 7 }).map((_, i) => ({
  day: ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"][i],
  investigations: Math.round(180 + Math.random() * 120),
  resolved: Math.round(140 + Math.random() * 100),
}));

export const RISK_DISTRIBUTION = [
  { name: "Safe", value: 62 },
  { name: "Low", value: 18 },
  { name: "Suspicious", value: 11 },
  { name: "High", value: 6 },
  { name: "Critical", value: 3 },
];

export const THREAT_SOURCES = [
  { country: "Russia", value: 28 },
  { country: "China", value: 22 },
  { country: "Nigeria", value: 14 },
  { country: "USA", value: 11 },
  { country: "Brazil", value: 8 },
  { country: "India", value: 7 },
  { country: "Other", value: 10 },
];

export const RECENT_INVESTIGATIONS: Investigation[] = [
  { id: "INV-92841", date: "2m ago", source: "billing@paypa1-secure.co", target: "finance@acme.com", threatType: "Brand Impersonation", riskScore: 94, status: "blocked" },
  { id: "INV-92840", date: "6m ago", source: "hr-updates@dropbx-share.io", target: "j.reed@acme.com", threatType: "Credential Phishing", riskScore: 88, status: "investigating" },
  { id: "INV-92839", date: "14m ago", source: "ceo@acmee-corp.com", target: "cfo@acme.com", threatType: "BEC", riskScore: 97, status: "escalated" },
  { id: "INV-92838", date: "22m ago", source: "no-reply@microsft-alerts.com", target: "it@acme.com", threatType: "Credential Phishing", riskScore: 76, status: "blocked" },
  { id: "INV-92837", date: "35m ago", source: "docs@onedrivve-share.net", target: "legal@acme.com", threatType: "Malware", riskScore: 82, status: "resolved" },
  { id: "INV-92836", date: "51m ago", source: "invoice@stripee-pay.com", target: "ap@acme.com", threatType: "Invoice Fraud", riskScore: 71, status: "blocked" },
  { id: "INV-92835", date: "1h ago", source: "support@zoomm-meet.io", target: "sales@acme.com", threatType: "Credential Phishing", riskScore: 65, status: "resolved" },
  { id: "INV-92834", date: "1h ago", source: "hr@acme-benefit.co", target: "all@acme.com", threatType: "BEC", riskScore: 90, status: "escalated" },
];

export const ALERTS: Alert[] = [
  { id: "A-4821", title: "Credential harvesting campaign targeting Finance dept", severity: "critical", time: "3m ago", source: "URL Intelligence" },
  { id: "A-4820", title: "New BEC pattern matched CEO impersonation signature", severity: "critical", time: "11m ago", source: "Email Intelligence" },
  { id: "A-4819", title: "Suspicious login page cloning Microsoft 365 detected", severity: "high", time: "28m ago", source: "Visual Intelligence" },
  { id: "A-4818", title: "Malicious .docm attachment with macro dropper", severity: "high", time: "44m ago", source: "Attachment Intelligence" },
  { id: "A-4817", title: "IOC match with APT-29 infrastructure feed", severity: "suspicious", time: "1h ago", source: "Threat Intel" },
  { id: "A-4816", title: "Newly-registered lookalike domain observed", severity: "suspicious", time: "2h ago", source: "URL Intelligence" },
];

export const RECOMMENDATIONS = [
  "Enable enforced MFA on 14 privileged mailboxes flagged as high-risk.",
  "Quarantine 3 lookalike domains matched by the Brand Detection engine.",
  "Rotate 2 API keys observed in outbound traffic to unclassified endpoints.",
  "Review DMARC policy — currently p=none for acme.com. Recommend p=reject.",
];

export const AI_FINDINGS = [
  { title: "CEO Impersonation cluster", detail: "5 emails share identical linguistic fingerprint and Reply-To pivot.", score: 96 },
  { title: "Emerging campaign: HR benefits", detail: "New template observed across 3 tenants in last 48h.", score: 88 },
  { title: "Malicious CDN cluster", detail: "12 URLs share hosting ASN AS-58794, flagged by 4 feeds.", score: 82 },
];

export const URL_ANALYSIS_MOCK = {
  url: "",
  overallRisk: 92,
  confidence: 96,
  verdict: "Dangerous" as "Safe" | "Suspicious" | "Dangerous",
  domainAge: "4 days",
  whois: { registrar: "NameCheap Inc.", createdAt: "2026-07-20", country: "PA" },
  dns: [
    { type: "A", value: "185.243.115.42" },
    { type: "NS", value: "ns1.cloudobscure.net" },
    { type: "MX", value: "mail.paypa1-secure.co" },
  ],
  ssl: { issuer: "Let's Encrypt", validFrom: "2026-07-21", validTo: "2026-10-19", valid: true },
  hosting: "Cloudflare (via bulletproof reseller)",
  ip: "185.243.115.42",
  country: "Panama",
  redirects: [
    "https://paypa1-secure.co/login",
    "https://paypa1-secure.co/login/verify",
    "https://cdn-obf.top/collect",
  ],
  brandSimilarity: 94,
  reputationFeeds: [
    { name: "VirusTotal", detections: "12 / 89", verdict: "malicious" },
    { name: "PhishTank", detections: "Reported", verdict: "malicious" },
    { name: "AbuseIPDB", detections: "Confidence 88%", verdict: "malicious" },
  ],
  timeline: [
    { t: "0.0s", event: "Navigated to landing page" },
    { t: "0.4s", event: "Redirected to /login/verify" },
    { t: "1.1s", event: "Fake Microsoft 365 login rendered" },
    { t: "1.8s", event: "Credential form submits to cdn-obf.top" },
    { t: "2.4s", event: "OAuth token exfiltration attempt blocked" },
  ],
  aiExplanation: {
    summary: "This URL impersonates PayPal using a homoglyph domain (paypa1 vs paypal). Combined with a 4-day-old registration, bulletproof hosting, and a credential form posting to an unrelated CDN, the model classifies it as a high-confidence credential harvesting page.",
    reasons: [
      "Homoglyph domain: 'paypa1-secure.co' vs 'paypal.com' (edit distance 2)",
      "Domain registered 4 days ago — high-risk age band",
      "Credential form POSTs cross-origin to cdn-obf.top",
      "Visual layout matches Microsoft 365 login (94% CV similarity)",
      "Listed on 3 threat feeds within the last 24 hours",
    ],
    recommendations: [
      "Block domain paypa1-secure.co at DNS and mail gateway",
      "Purge related messages from 47 mailboxes",
      "Add IOCs to SIEM and rotate credentials of clicked users",
    ],
  },
};

export const EMAIL_ANALYSIS_MOCK = {
  subject: "URGENT: Wire transfer authorization needed today",
  from_email: "ceo@acmee-corp.com",
  reply_to: "ceo.finance@protonmail.com",
  to: "cfo@acme.com",
  riskScore: 97,
  spamScore: 4.2,
  phishingProbability: 0.96,
  bec: true,
  urgency: 0.91,
  impersonation: 0.94,
  authentication: {
    spf: "FAIL",
    dkim: "NONE",
    dmarc: "FAIL",
    score: 20,
  },
  reply_analysis: {
  match: false,
  reason: "Reply-To domain mismatch",
  },
  entities: {
    person: ["John Miller (CEO)"],
    amount: ["$248,500"],
    bank: ["First National Bank of Panama"],
    deadline: ["End of business today"],
  },
  senderReputation: "Newly observed — 0 prior sends",
  headerSummary: "Message originated from IP 185.243.115.42 (Panama). SPF hard-fail. Reply-To domain differs from From.",
  suspiciousLinks: [
    { url: "https://acmee-corp.com/wire-details.pdf", risk: 88 },
  ],
  suspiciousAttachments: [
    { name: "wire-instructions.docm", risk: 92 },
  ],
  highlighted: [
    { text: "URGENT — do not discuss with anyone else on the team", tag: "Isolation Pressure" },
    { text: "Wire $248,500 today to secure the acquisition", tag: "Financial Urgency" },
    { text: "I'm in back-to-back board meetings, only reply to this address", tag: "Reply-To Pivot" },
  ],
  aiExplanation: {
  summary: "This email exhibits a Business Email Compromise pattern.",
  reasons: [
    "Contains 'urgent'",
    "Contains 'wire'",
    "Reply-To differs from sender"
  ],
  recommendations: [
    "Do not click suspicious links.",
    "Verify the sender through another channel."
  ]
},
};

export const VISUAL_ANALYSIS_MOCK = {
  targetUrl: "https://microsft-alerts.com/account/verify",
  detectedBrand: "Microsoft 365",
  visualSimilarity: 96,
  fakeLoginDetected: true,
  logoSimilarity: 98,
  colorSimilarity: 94,
  layoutSimilarity: 92,
  explanation:
    "CLIP embedding distance to the reference Microsoft 365 sign-in page is 0.04. The clone reproduces the logo, color grid, and form geometry with pixel-level fidelity, but posts credentials to a domain unaffiliated with Microsoft.",
};

export const ATTACHMENT_ANALYSIS_MOCK = {
  fileName: "invoice-Q3-final.docm",
  fileType: "DOCX (macro-enabled)",
  size: "184 KB",
  sha256: "9b3f2a1c8e7d4b0f5a6c9d2e1f0a8b7c6d5e4f3a2b1c0d9e8f7a6b5c4d3e2f10",
  riskScore: 91,
  macros: true,
  embeddedScripts: 2,
  suspiciousExecutables: 1,
  threats: [
    { name: "AutoOpen macro invokes PowerShell", severity: "critical" as const },
    { name: "Base64-encoded payload downloader", severity: "high" as const },
    { name: "Fetches remote binary from newly-registered domain", severity: "high" as const },
  ],
  recommendation: "Quarantine the file, block the callback domain, and audit any host that opened it.",
};

export const THREAT_INTEL_MOCK = {
  ioc: "185.243.115.42",
  type: "IPv4",
  reputation: "Malicious",
  confidence: 92,
  knownCampaign: "OceanLotus / APT32 infrastructure cluster",
  malwareFamily: "CobaltStrike loader",
  firstSeen: "2026-05-12",
  lastSeen: "2026-07-23",
  feeds: [
    { name: "VirusTotal", verdict: "22 / 92 vendors" },
    { name: "AbuseIPDB", verdict: "Confidence 88%" },
    { name: "PhishTank", verdict: "Reported (14 URLs)" },
    { name: "AlienVault OTX", verdict: "3 pulses" },
  ],
  actions: [
    "Block IP at perimeter and egress filters",
    "Sweep endpoints for beacon traffic to this host",
    "Correlate with mail gateway logs for the past 30 days",
  ],
};

export const REPORT_MOCK = {
  id: "AF-INC-2026-08421",
  title: "BEC Wire-Fraud Attempt — Finance Department",
  createdAt: "2026-07-24 14:22 UTC",
  analyst: "Priya Ramanathan",
  severity: "Critical" as const,
  executiveSummary:
    "On 2026-07-24, EscudoFlow AI detected a targeted Business Email Compromise attempt against Acme Corp's CFO. The attacker impersonated CEO John Miller via the lookalike domain acmee-corp.com and requested a $248,500 wire transfer. The message was blocked before delivery. No user interaction occurred.",
  iocs: [
    { type: "Domain", value: "acmee-corp.com" },
    { type: "IPv4", value: "185.243.115.42" },
    { type: "Email", value: "ceo.finance@protonmail.com" },
    { type: "SHA256", value: "9b3f2a1c8e7d4b0f5a6c9d2e1f0a8b7c6d5e4f3a2b1c0d9e8f7a6b5c4d3e2f10" },
  ],
  timeline: [
    { t: "14:19", event: "Inbound message received by mail gateway" },
    { t: "14:19", event: "EscudoFlow Email Intelligence scored 0.96 phishing" },
    { t: "14:20", event: "BEC classifier confirmed CEO impersonation" },
    { t: "14:20", event: "Message quarantined; recipient notified" },
    { t: "14:22", event: "Incident report generated automatically" },
  ],
  recommendations: [
    "Enforce DMARC p=reject on acme.com",
    "Add acmee-corp.com to blocklist across mail and web",
    "Run BEC awareness micro-training for Finance team",
  ],
};
