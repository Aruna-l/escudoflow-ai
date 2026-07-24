import { createFileRoute } from "@tanstack/react-router";
import { useState } from "react";
import { motion } from "framer-motion";
import { Search, Globe2, Calendar } from "lucide-react";
import { AppShell, PageHeader } from "@/components/app-shell";
import { GlassCard, RiskBadge, SectionHeading } from "@/components/cyber-ui";
import { Button } from "@/components/ui/button";
import { THREAT_INTEL_MOCK } from "@/lib/mock-data";

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

const TYPES = ["Domain", "IP", "URL", "Hash", "Email"] as const;

function ThreatIntel() {
  const [q, setQ] = useState(THREAT_INTEL_MOCK.ioc);
  const [type, setType] = useState<(typeof TYPES)[number]>("IP");
  const [analyzed, setAnalyzed] = useState(true);
  const d = THREAT_INTEL_MOCK;

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
              onClick={() => setType(t)}
              className={`px-3 py-1.5 rounded-lg text-xs border transition ${
                t === type ? "gradient-primary text-white border-transparent" : "glass border-white/10 text-muted-foreground hover:text-white"
              }`}
            >{t}</button>
          ))}
        </div>
        <div className="flex gap-2">
          <div className="flex-1 flex items-center gap-2 rounded-xl glass px-4 h-14">
            <Globe2 className="h-4 w-4 text-cyan" />
            <input className="bg-transparent flex-1 outline-none text-sm font-mono" value={q} onChange={(e) => setQ(e.target.value)} />
          </div>
          <Button onClick={() => setAnalyzed(true)} className="gradient-primary text-white glow-primary h-14 px-6">
            <Search className="h-4 w-4 mr-2" /> Search
          </Button>
        </div>
      </GlassCard>

      {analyzed && (
        <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} className="space-y-6">
          <div className="grid gap-4 lg:grid-cols-4">
            <GlassCard>
              <div className="text-xs uppercase tracking-widest text-muted-foreground">Reputation</div>
              <div className="mt-2 text-3xl font-bold text-red-400">{d.reputation}</div>
              <RiskBadge className="mt-2" level="critical" />
            </GlassCard>
            <GlassCard>
              <div className="text-xs uppercase tracking-widest text-muted-foreground">Confidence</div>
              <div className="mt-2 text-3xl font-bold gradient-text">{d.confidence}%</div>
              <div className="mt-3 h-2 rounded-full bg-white/5 overflow-hidden">
                <motion.div initial={{ width: 0 }} animate={{ width: `${d.confidence}%` }} transition={{ duration: 1 }} className="h-full gradient-primary" />
              </div>
            </GlassCard>
            <GlassCard>
              <div className="text-xs uppercase tracking-widest text-muted-foreground">Malware Family</div>
              <div className="mt-2 text-lg font-semibold">{d.malwareFamily}</div>
              <div className="mt-1 text-xs text-muted-foreground">{d.knownCampaign}</div>
            </GlassCard>
            <GlassCard>
              <div className="text-xs uppercase tracking-widest text-muted-foreground">Timeline</div>
              <div className="mt-2 flex items-center gap-2 text-sm"><Calendar className="h-3.5 w-3.5 text-cyan" /> First seen <span className="ml-auto font-mono">{d.firstSeen}</span></div>
              <div className="mt-1 flex items-center gap-2 text-sm"><Calendar className="h-3.5 w-3.5 text-cyan" /> Last seen <span className="ml-auto font-mono">{d.lastSeen}</span></div>
            </GlassCard>
          </div>

          <GlassCard>
            <SectionHeading title="Threat Feeds" description="Correlated verdicts" />
            <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-3">
              {d.feeds.map((f) => (
                <div key={f.name} className="rounded-xl glass p-4">
                  <div className="text-xs uppercase tracking-widest text-muted-foreground">{f.name}</div>
                  <div className="mt-2 text-sm font-semibold">{f.verdict}</div>
                  <RiskBadge className="mt-3" level="critical" label="Malicious" />
                </div>
              ))}
            </div>
          </GlassCard>

          <GlassCard>
            <SectionHeading title="Recommended Actions" />
            <ul className="space-y-2">
              {d.actions.map((a, i) => (
                <li key={i} className="flex items-start gap-2 text-sm">
                  <span className="mt-1 h-1.5 w-1.5 rounded-full bg-cyan shrink-0" />
                  <span>{a}</span>
                </li>
              ))}
            </ul>
          </GlassCard>
        </motion.div>
      )}
    </AppShell>
  );
}
