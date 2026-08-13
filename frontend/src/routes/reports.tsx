import { createFileRoute } from "@tanstack/react-router";
import { useEffect, useState } from "react";
import { FileText, Download, User, Loader2 } from "lucide-react";
import { AppShell, PageHeader } from "@/components/app-shell";
import { GlassCard, RiskBadge, SectionHeading } from "@/components/cyber-ui";
import { Button } from "@/components/ui/button";
import {
  getLatestReport,
  updateReportNotes,
  exportReportUrl,
  ReportApiError,
  type ReportResponse,
} from "@/lib/report-api";

export const Route = createFileRoute("/reports")({
  head: () => ({
    meta: [
      { title: "Investigation Reports — EscudoFlow AI" },
      { name: "description", content: "Executive-ready incident reports with IOCs, timeline, evidence, and analyst notes." },
      { property: "og:title", content: "Investigation Reports — EscudoFlow AI" },
      { property: "og:description", content: "Automatically generated incident reports for SOC and leadership." },
    ],
  }),
  component: Reports,
});

const severityToLevel = (s: string): "critical" | "high" | "suspicious" | "low" | "safe" => {
  switch (s) {
    case "Critical": return "critical";
    case "High": return "high";
    case "Suspicious": return "suspicious";
    case "Low": return "low";
    default: return "safe";
  }
};

function Reports() {
  const [r, setR] = useState<ReportResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [notes, setNotes] = useState("");
  const [savingNotes, setSavingNotes] = useState(false);

  useEffect(() => {
    (async () => {
      try {
        const data = await getLatestReport();
        setR(data);
        setNotes(data.analystNotes ?? "");
      } catch (err) {
        setError(
          err instanceof ReportApiError
            ? err.message
            : "No report available yet — run an analysis on the Email, URL, Attachment, or Threat pages first."
        );
      } finally {
        setLoading(false);
      }
    })();
  }, []);

  const saveNotes = async () => {
    if (!r) return;
    setSavingNotes(true);
    try {
      const updated = await updateReportNotes(r.id, notes);
      setR(updated);
    } catch {
      // keep local notes on failure; user can retry by blurring again
    } finally {
      setSavingNotes(false);
    }
  };

  if (loading) {
    return (
      <AppShell>
        <PageHeader eyebrow="Reports" title="Investigation Report" description="Automatically generated, analyst-editable, executive-ready." />
        <GlassCard>
          <div className="flex items-center justify-center gap-2 py-12 text-sm text-muted-foreground">
            <Loader2 className="h-4 w-4 animate-spin" /> Loading latest report…
          </div>
        </GlassCard>
      </AppShell>
    );
  }

  if (error || !r) {
    return (
      <AppShell>
        <PageHeader eyebrow="Reports" title="Investigation Report" description="Automatically generated, analyst-editable, executive-ready." />
        <GlassCard>
          <div className="text-sm text-muted-foreground text-center py-12">{error}</div>
        </GlassCard>
      </AppShell>
    );
  }

  return (
    <AppShell>
      <PageHeader
        eyebrow="Reports"
        title="Investigation Report"
        description="Automatically generated, analyst-editable, executive-ready."
        actions={
          <>
            <a href={exportReportUrl(r.id, "csv")}>
              <Button variant="outline" className="border-white/10"><Download className="h-4 w-4 mr-2" /> CSV</Button>
            </a>
            <a href={exportReportUrl(r.id, "json")}>
              <Button variant="outline" className="border-white/10"><Download className="h-4 w-4 mr-2" /> JSON</Button>
            </a>
            <a href={exportReportUrl(r.id, "pdf")}>
              <Button className="gradient-primary text-white glow-primary"><Download className="h-4 w-4 mr-2" /> Export PDF</Button>
            </a>
          </>
        }
      />

      <GlassCard className="mb-6">
        <div className="flex flex-wrap items-center justify-between gap-4">
          <div className="min-w-0">
            <div className="text-xs uppercase tracking-widest text-cyan">{r.id}</div>
            <h2 className="mt-1 text-2xl font-bold">{r.title}</h2>
            <div className="mt-2 flex flex-wrap items-center gap-3 text-xs text-muted-foreground">
              <span><FileText className="h-3.5 w-3.5 inline mr-1" /> {r.createdAt}</span>
              <span><User className="h-3.5 w-3.5 inline mr-1" /> {r.analyst}</span>
              <RiskBadge level={severityToLevel(r.severity)} label={r.severity} />
            </div>
          </div>
        </div>
      </GlassCard>

      <div className="grid gap-6 lg:grid-cols-[1.4fr_1fr]">
        <div className="space-y-6">
          <GlassCard>
            <SectionHeading title="Executive Summary" />
            <p className="text-sm text-muted-foreground leading-relaxed">{r.executiveSummary}</p>
          </GlassCard>

          <GlassCard>
            <SectionHeading title="Threat Overview" />
            <div className="grid sm:grid-cols-3 gap-3">
              {[
                { k: "Vector", v: r.threatOverview.vector },
                { k: "Target", v: r.threatOverview.target },
                { k: "Impact", v: r.threatOverview.impact },
              ].map((c) => (
                <div key={c.k} className="rounded-lg glass p-3">
                  <div className="text-[10px] uppercase tracking-widest text-muted-foreground">{c.k}</div>
                  <div className="mt-1 text-sm font-medium">{c.v}</div>
                </div>
              ))}
            </div>
          </GlassCard>

          <GlassCard>
            <SectionHeading title="Indicators of Compromise" />
            <table className="w-full text-sm">
              <thead>
                <tr className="text-left text-[11px] uppercase tracking-widest text-muted-foreground border-b border-white/10">
                  <th className="py-2">Type</th><th className="py-2">Value</th>
                </tr>
              </thead>
              <tbody>
                {r.iocs.map((i) => (
                  <tr key={i.value} className="border-b border-white/5">
                    <td className="py-2.5 text-cyan font-mono text-xs">{i.type}</td>
                    <td className="py-2.5 font-mono text-xs break-all">{i.value}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </GlassCard>

          <GlassCard>
            <SectionHeading title="Timeline" />
            <ol className="relative border-l border-white/10 pl-4 space-y-4">
              {r.timeline.map((t, i) => (
                <li key={i} className="relative">
                  <span className="absolute -left-[21px] top-1 h-2.5 w-2.5 rounded-full bg-cyan glow-cyan" />
                  <div className="text-[11px] text-muted-foreground font-mono">{t.t} UTC</div>
                  <div className="text-sm">{t.event}</div>
                </li>
              ))}
            </ol>
          </GlassCard>

          <GlassCard>
            <SectionHeading title="Analyst Notes" />
            <textarea
              value={notes}
              onChange={(e) => setNotes(e.target.value)}
              onBlur={saveNotes}
              placeholder="Add investigation notes…"
              className="w-full h-24 rounded-lg glass p-3 text-sm outline-none resize-none"
            />
            {savingNotes && <div className="mt-1 text-[10px] text-muted-foreground">Saving…</div>}
          </GlassCard>
        </div>

        <div className="space-y-6">
          <GlassCard>
            <SectionHeading title="Risk Score" />
            <div className="text-5xl font-bold gradient-text">{r.riskScore}</div>
            <div className="text-xs text-muted-foreground mt-1">Confidence {r.confidence}%</div>
          </GlassCard>

          <GlassCard>
            <SectionHeading title="Recommendations" />
            <ul className="space-y-2">
              {r.recommendations.map((rec, i) => (
                <li key={i} className="flex items-start gap-2 text-sm">
                  <span className="mt-1 h-1.5 w-1.5 rounded-full bg-emerald-400 shrink-0" />
                  <span>{rec}</span>
                </li>
              ))}
            </ul>
          </GlassCard>

          <GlassCard>
            <SectionHeading title="Evidence" />
            <ul className="space-y-2 text-sm">
              {r.evidence.map((f) => (
                <li key={f.filename} className="flex items-center justify-between rounded-lg glass px-3 py-2">
                  <span className="font-mono text-xs">{f.filename}</span>
                  <Download className="h-3.5 w-3.5 text-cyan cursor-pointer" />
                </li>
              ))}
            </ul>
          </GlassCard>
        </div>
      </div>
    </AppShell>
  );
}