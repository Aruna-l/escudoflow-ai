import { createFileRoute } from "@tanstack/react-router";
import { useState } from "react";
import { motion } from "framer-motion";
import { Link2, Search, X, Globe, ShieldAlert, Clock, ExternalLink, Server, MapPin, Building } from "lucide-react";
import { AppShell, PageHeader } from "@/components/app-shell";
import { GlassCard, RiskBadge, RiskMeter, SectionHeading } from "@/components/cyber-ui";
import { Button } from "@/components/ui/button";
import { URL_ANALYSIS_MOCK } from "@/lib/mock-data";

export const Route = createFileRoute("/url-intelligence")({
  head: () => ({
    meta: [
      { title: "URL Intelligence — EscudoFlow AI" },
      { name: "description", content: "Behavioral URL analysis, WHOIS, DNS, SSL, brand similarity, and threat feed reputation in under 2 seconds." },
      { property: "og:title", content: "URL Intelligence — EscudoFlow AI" },
      { property: "og:description", content: "Behavioral URL scoring with explainable AI." },
    ],
  }),
  component: URLIntelligence,
});

function URLIntelligence() {
  const [url, setUrl] = useState(URL_ANALYSIS_MOCK.url);
  const [analyzed, setAnalyzed] = useState(false);
  const [loading, setLoading] = useState(false);
  const data = URL_ANALYSIS_MOCK;

  const runAnalysis = () => {
    setLoading(true);
    // TODO(api): POST /api/v1/url/analyze { url }
    setTimeout(() => { setLoading(false); setAnalyzed(true); }, 900);
  };

  return (
    <AppShell>
      <PageHeader
        eyebrow="URL Intelligence"
        title="Behavioral URL Analysis"
        description="Enter a URL to run WHOIS, DNS, SSL, redirect-chain, and behavioral sandbox analysis with explainable AI scoring."
      />

      <GlassCard className="mb-8">
        <div className="flex flex-col md:flex-row gap-3">
          <div className="flex-1 flex items-center gap-2 rounded-xl glass px-4 h-14">
            <Link2 className="h-4 w-4 text-cyan shrink-0" />
            <input
              className="bg-transparent flex-1 outline-none text-sm font-mono truncate"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              placeholder="https://example.com/path"
            />
            {url && (
              <button onClick={() => setUrl("")} className="text-muted-foreground hover:text-white">
                <X className="h-4 w-4" />
              </button>
            )}
          </div>
          <div className="flex gap-2">
            <Button onClick={runAnalysis} disabled={!url || loading} className="gradient-primary text-white glow-primary h-14 px-6">
              {loading ? "Analyzing…" : <><Search className="h-4 w-4 mr-2" />Analyze</>}
            </Button>
            <Button variant="outline" onClick={() => { setUrl(""); setAnalyzed(false); }} className="border-white/10 h-14 px-6">Clear</Button>
          </div>
        </div>
      </GlassCard>

      {analyzed && (
        <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} className="space-y-6">
          {/* Verdict row */}
          <div className="grid gap-4 lg:grid-cols-3">
            <GlassCard className="lg:col-span-1">
              <RiskMeter score={data.overallRisk} label="Overall Risk" />
            </GlassCard>
            <GlassCard>
              <div className="text-xs uppercase tracking-widest text-muted-foreground">Confidence</div>
              <div className="mt-2 text-4xl font-bold gradient-text">{data.confidence}%</div>
              <div className="mt-1 text-xs text-muted-foreground">Model ensemble agreement</div>
              <div className="mt-4 grid grid-cols-3 gap-2">
                {(["Safe", "Suspicious", "Dangerous"] as const).map((v) => (
                  <div
                    key={v}
                    className={`text-center py-2 rounded-lg text-xs border ${
                      data.verdict === v
                        ? v === "Dangerous" ? "bg-red-500/15 border-red-500/40 text-red-300"
                        : v === "Suspicious" ? "bg-amber-500/15 border-amber-500/40 text-amber-300"
                        : "bg-emerald-500/15 border-emerald-500/40 text-emerald-300"
                        : "border-white/10 text-muted-foreground"
                    }`}
                  >{v}</div>
                ))}
              </div>
            </GlassCard>
            <GlassCard>
              <div className="text-xs uppercase tracking-widest text-muted-foreground">Brand Similarity</div>
              <div className="mt-2 text-4xl font-bold">{data.brandSimilarity}%</div>
              <div className="mt-1 text-xs text-muted-foreground">Highest match: <span className="text-cyan">PayPal / Microsoft 365</span></div>
              <div className="mt-4 h-2 rounded-full bg-white/5 overflow-hidden">
                <motion.div initial={{ width: 0 }} animate={{ width: `${data.brandSimilarity}%` }} transition={{ duration: 1 }} className="h-full gradient-primary" />
              </div>
            </GlassCard>
          </div>

          {/* Details */}
          <div className="grid gap-4 lg:grid-cols-3">
            <GlassCard>
              <SectionHeading title="Domain & WHOIS" />
              <dl className="text-sm space-y-2">
                <Row icon={Clock} label="Domain Age" value={data.domainAge} />
                <Row icon={Building} label="Registrar" value={data.whois.registrar} />
                <Row icon={MapPin} label="Country" value={data.whois.country} />
                <Row icon={Globe} label="Created" value={data.whois.createdAt} />
                <Row icon={Server} label="Hosting" value={data.hosting} />
                <Row icon={Server} label="IP Address" value={data.ip} mono />
              </dl>
            </GlassCard>
            <GlassCard>
              <SectionHeading title="DNS & SSL" />
              <div className="space-y-1.5">
                {data.dns.map((r, i) => (
                  <div key={i} className="flex items-center justify-between text-xs font-mono">
                    <span className="px-1.5 py-0.5 rounded bg-white/5 text-cyan">{r.type}</span>
                    <span className="text-muted-foreground truncate ml-2">{r.value}</span>
                  </div>
                ))}
              </div>
              <div className="mt-4 rounded-lg glass p-3">
                <div className="text-xs uppercase tracking-widest text-muted-foreground">SSL Certificate</div>
                <div className="mt-1 text-sm">{data.ssl.issuer}</div>
                <div className="text-xs text-muted-foreground">{data.ssl.validFrom} → {data.ssl.validTo}</div>
                <RiskBadge className="mt-2" level={data.ssl.valid ? "low" : "critical"} label={data.ssl.valid ? "Valid" : "Invalid"} />
              </div>
            </GlassCard>
            <GlassCard>
              <SectionHeading title="Threat Reputation" />
              <ul className="space-y-2">
                {data.reputationFeeds.map((f) => (
                  <li key={f.name} className="flex items-center justify-between text-sm rounded-lg glass px-3 py-2">
                    <span className="font-medium">{f.name}</span>
                    <div className="text-right">
                      <div className="text-xs text-muted-foreground">{f.detections}</div>
                      <RiskBadge level="critical" label={f.verdict} className="mt-0.5" />
                    </div>
                  </li>
                ))}
              </ul>
            </GlassCard>
          </div>

          {/* Redirects + Timeline */}
          <div className="grid gap-4 lg:grid-cols-2">
            <GlassCard>
              <SectionHeading title="Suspicious Redirect Chain" />
              <ol className="space-y-2">
                {data.redirects.map((r, i) => (
                  <li key={i} className="flex items-center gap-3 text-sm">
                    <span className="grid place-items-center h-6 w-6 rounded-full glass text-xs font-bold text-cyan">{i + 1}</span>
                    <ExternalLink className="h-3 w-3 text-muted-foreground" />
                    <span className="font-mono text-xs truncate">{r}</span>
                  </li>
                ))}
              </ol>
            </GlassCard>
            <GlassCard>
              <SectionHeading title="Behavior Timeline" description="Headless sandbox execution" />
              <ol className="relative border-l border-white/10 pl-4 space-y-3">
                {data.timeline.map((t, i) => (
                  <li key={i} className="relative">
                    <span className="absolute -left-[21px] top-1 h-2.5 w-2.5 rounded-full bg-cyan glow-cyan" />
                    <div className="text-[11px] text-muted-foreground font-mono">{t.t}</div>
                    <div className="text-sm">{t.event}</div>
                  </li>
                ))}
              </ol>
            </GlassCard>
          </div>

          {/* AI Explanation */}
          <GlassCard>
            <div className="flex items-center gap-2 mb-3">
              <ShieldAlert className="h-4 w-4 text-cyan" />
              <SectionHeading title="Explainable AI Verdict" description="SHAP + LIME reasoning" />
            </div>
            <p className="text-sm text-muted-foreground leading-relaxed max-w-3xl">{data.aiExplanation.summary}</p>
            <div className="mt-5 grid md:grid-cols-2 gap-4">
              <div>
                <h4 className="text-sm font-semibold mb-2">Top Reasons</h4>
                <ul className="space-y-2">
                  {data.aiExplanation.reasons.map((r, i) => (
                    <li key={i} className="flex items-start gap-2 text-sm">
                      <span className="mt-1 h-1.5 w-1.5 rounded-full bg-red-400 shrink-0" />
                      <span>{r}</span>
                    </li>
                  ))}
                </ul>
              </div>
              <div>
                <h4 className="text-sm font-semibold mb-2">Recommended Actions</h4>
                <ul className="space-y-2">
                  {data.aiExplanation.recommendations.map((r, i) => (
                    <li key={i} className="flex items-start gap-2 text-sm">
                      <span className="mt-1 h-1.5 w-1.5 rounded-full bg-emerald-400 shrink-0" />
                      <span>{r}</span>
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          </GlassCard>
        </motion.div>
      )}
    </AppShell>
  );
}

function Row({ icon: Icon, label, value, mono }: { icon: any; label: string; value: string; mono?: boolean }) {
  return (
    <div className="flex items-center justify-between gap-3">
      <div className="flex items-center gap-2 text-muted-foreground text-xs">
        <Icon className="h-3.5 w-3.5" /> {label}
      </div>
      <div className={mono ? "font-mono text-xs" : "text-sm"}>{value}</div>
    </div>
  );
}
