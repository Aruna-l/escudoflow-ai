import { createFileRoute } from "@tanstack/react-router";
import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Search, Globe2, Calendar, Loader2, AlertTriangle } from "lucide-react";
import { AppShell, PageHeader } from "@/components/app-shell";
import { GlassCard, RiskBadge, SectionHeading } from "@/components/cyber-ui";
import { Button } from "@/components/ui/button";
import { analyzeIOC, validateIOC, ThreatApiError, type IOCType, type ThreatIntelResponse } from "@/lib/threat-api";
import { scoreToLevel } from "@/components/cyber-ui"; // add to existing import

export const Route = createFileRoute("/threat-intelligence")({
  head: () => ({
    meta: [
      { title: "Threat Intelligence — EscudoFlow AI" },
      { name: "description", content: "Search IOCs across VirusTotal, PhishTank, AbuseIPDB, and internal feeds for enriched threat context." },
      { property: "og:title", content: "Threat Intelligence — EscudoFlow AI" },
      { property: "og:description", content: "Correlated IOC lookups across leading threat feeds." },
    ],
  }),
  component: ThreatIntel,
});

const TYPES: IOCType[] = ["Domain", "IP", "URL", "Hash", "Email"];

// Maps reputation string -> RiskBadge level (safe | low | suspicious | high | critical)
function reputationToLevel(reputation: string): "critical" | "high" | "suspicious" | "low" | "safe" {
  switch (reputation) {
    case "Malicious":
      return "critical";
    case "Suspicious":
      return "suspicious";
    case "Clean":
      return "safe";
    default:
      return "low"; // Unknown
  }
}

function reputationToTextColor(reputation: string): string {
  switch (reputation) {
    case "Malicious":
      return "text-red-400";
    case "Suspicious":
      return "text-amber-400";
    case "Clean":
      return "text-emerald-400";
    default:
      return "text-muted-foreground";
  }
}

function ThreatIntel() {
  const [q, setQ] = useState("");
  const [type, setType] = useState<IOCType>("IP");
  const [result, setResult] = useState<ThreatIntelResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleSearch() {
  const trimmed = q.trim();
  if (!trimmed) return;

  const validationError = validateIOC(trimmed, type);
  if (validationError) {
    setResult(null);
    setError(validationError);
    return;
  }

  setLoading(true);
  setError(null);
  try {
    const data = await analyzeIOC(trimmed, type);
    setResult(data);
  } catch (err) {
    setResult(null);
    setError(err instanceof ThreatApiError ? err.message : "Something went wrong analyzing this IOC.");
  } finally {
    setLoading(false);
  }
}

  return (
    <AppShell>
      <PageHeader
        eyebrow="Threat Intelligence"
        title="IOC Correlation Hub"
        description="Search any indicator of compromise. EscudoFlow correlates it across 20+ feeds and internal telemetry in real time."
      />

      <GlassCard className="mb-6">
        <div className="flex flex-wrap items-center gap-2 mb-3">
          {TYPES.map((t) => (
            <button
              key={t}
              onClick={() => { setType(t); setQ(""); setError(null); setResult(null); }}
              className={`px-3 py-1.5 rounded-lg text-xs border transition ${
                t === type ? "gradient-primary text-white border-transparent" : "glass border-white/10 text-muted-foreground hover:text-white"
              }`}
            >
              {t}
            </button>
          ))}
        </div>
        <div className="flex gap-2">
          <div className="flex-1 flex items-center gap-2 rounded-xl glass px-4 h-14">
            <Globe2 className="h-4 w-4 text-cyan" />
            <input
              className="bg-transparent flex-1 outline-none text-sm font-mono"
              value={q}
              onChange={(e) => setQ(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && handleSearch()}
              placeholder={
                type === "IP" ? "e.g. 185.220.101.1" :
                type === "Domain" ? "e.g. example.com" :
                type === "URL" ? "e.g. https://example.com/path" :
                type === "Hash" ? "e.g. 44d88612fea8a8f36de82e1278abb02f" :
                "e.g. user@example.com"
              }
            />
          </div>
          <Button onClick={handleSearch} disabled={loading} className="gradient-primary text-white glow-primary h-14 px-6">
            {loading ? <Loader2 className="h-4 w-4 mr-2 animate-spin" /> : <Search className="h-4 w-4 mr-2" />}
            {loading ? "Searching" : "Search"}
          </Button>
        </div>
      </GlassCard>

      {error && (
        <GlassCard className="mb-6 border-red-500/30">
          <div className="flex items-center gap-2 text-sm text-red-400">
            <AlertTriangle className="h-4 w-4" />
            {error}
          </div>
        </GlassCard>
      )}

      <AnimatePresence mode="wait">
        {result && !loading && (
          <motion.div
            key={result.ioc + result.type}
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -8 }}
            className="space-y-6"
          >
            <div className="grid gap-4 lg:grid-cols-4">
              <GlassCard>
                <div className="text-xs uppercase tracking-widest text-muted-foreground">Reputation</div>
                <div className={`mt-2 text-3xl font-bold ${reputationToTextColor(result.reputation)}`}>{result.reputation}</div>
                <RiskBadge className="mt-2" level={reputationToLevel(result.reputation)} />
              </GlassCard>
              <GlassCard>
                <div className="text-xs uppercase tracking-widest text-muted-foreground">Confidence</div>
                <div className="mt-2 text-3xl font-bold gradient-text">{result.confidence}%</div>
                <div className="mt-3 h-2 rounded-full bg-white/5 overflow-hidden">
                  <motion.div
                    initial={{ width: 0 }}
                    animate={{ width: `${result.confidence}%` }}
                    transition={{ duration: 1 }}
                    className="h-full gradient-primary"
                  />
                </div>
              </GlassCard>
              <GlassCard>
                <div className="text-xs uppercase tracking-widest text-muted-foreground">Malware Family</div>
                <div className="mt-2 text-lg font-semibold">{result.malwareFamily}</div>
                <div className="mt-1 text-xs text-muted-foreground">{result.knownCampaign}</div>
              </GlassCard>
              <GlassCard>
                <div className="text-xs uppercase tracking-widest text-muted-foreground">Timeline</div>
                <div className="mt-2 flex items-center gap-2 text-sm">
                  <Calendar className="h-3.5 w-3.5 text-cyan" /> First seen
                  <span className="ml-auto font-mono">{result.firstSeen}</span>
                </div>
                <div className="mt-1 flex items-center gap-2 text-sm">
                  <Calendar className="h-3.5 w-3.5 text-cyan" /> Last seen
                  <span className="ml-auto font-mono">{result.lastSeen}</span>
                </div>
              </GlassCard>
            </div>

            <GlassCard>
              <SectionHeading title="Threat Feeds" description="Correlated verdicts" />
              <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-3">
                {result.feeds.map((f) => {
                  const isError = ["Lookup failed", "No data", "Rate limited", "Not configured"].includes(f.verdict);
                  return (
                    <div key={f.name} className="rounded-xl glass p-4">
                      <div className="text-xs uppercase tracking-widest text-muted-foreground">{f.name}</div>
                      <div className="mt-2 text-sm font-semibold">{f.verdict}</div>
                      <RiskBadge
                        className="mt-3"
                        level={isError ? "low" : f.malicious ? "critical" : "safe"}
                        label={isError ? "No Signal" : f.malicious ? "Malicious" : "Clean"}
                      />
                    </div>
                  );
                })}
              </div>
            </GlassCard>

            <GlassCard>
              <SectionHeading title="Recommended Actions" />
              <ul className="space-y-2">
                {result.actions.map((a, i) => (
                  <li key={i} className="flex items-start gap-2 text-sm">
                    <span className="mt-1 h-1.5 w-1.5 rounded-full bg-cyan shrink-0" />
                    <span>{a}</span>
                  </li>
                ))}
              </ul>
            </GlassCard>
          </motion.div>
        )}
      </AnimatePresence>

      {!result && !loading && !error && (
        <GlassCard>
          <div className="text-sm text-muted-foreground text-center py-8">
            Enter an indicator of compromise above and hit search to correlate it across threat feeds.
          </div>
        </GlassCard>
      )}
    </AppShell>
  );
}