import { useEffect, useState } from "react";
import { createFileRoute, Link } from "@tanstack/react-router";
import { motion } from "framer-motion";
import {
  Activity, ShieldAlert, ShieldCheck, Ban, Mail, Gauge, ThermometerSun, Timer,
  MoreHorizontal, ArrowUpRight,
} from "lucide-react";
import {
  Area, AreaChart, Bar, BarChart, CartesianGrid, Cell, Pie, PieChart,
  ResponsiveContainer, Tooltip, XAxis, YAxis,
} from "recharts";
import { AppShell, PageHeader } from "@/components/app-shell";
import { GlassCard, RiskBadge, SectionHeading, StatCard, scoreToLevel } from "@/components/cyber-ui";
import { Button } from "@/components/ui/button";
import {
  getDashboardSummary, getDashboardFeed, getDashboardInsights,
  formatKpiCards, DashboardApiError,
  type DashboardSummary, type DashboardFeed, type DashboardInsights,
} from "@/lib/dashboard-api";

export const Route = createFileRoute("/dashboard")({
  head: () => ({
    meta: [
      { title: "SOC Dashboard — EscudoFlow AI" },
      { name: "description", content: "Live security operations center dashboard with threat trends, alerts, and AI findings." },
      { property: "og:title", content: "SOC Dashboard — EscudoFlow AI" },
      { property: "og:description", content: "Live SOC dashboard: threats, investigations, alerts." },
    ],
  }),
  component: Dashboard,
});

const KPI_ICONS = [ShieldAlert, Activity, Ban, ShieldCheck, Mail, Gauge, ThermometerSun, Timer];
const CHART_COLORS = ["#2563EB", "#06B6D4", "#22C55E", "#F59E0B", "#EF4444", "#A855F7"];

function Dashboard() {
  const [summary, setSummary] = useState<DashboardSummary | null>(null);
  const [feed, setFeed] = useState<DashboardFeed | null>(null);
  const [insights, setInsights] = useState<DashboardInsights | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    // Summary and feed load in parallel; insights is intentionally
    // separate so a slow LLM-backed call never blocks KPIs/charts/table
    // from rendering.
    getDashboardSummary().then(setSummary).catch((e) => setError(e instanceof DashboardApiError ? e.message : "Failed to load dashboard summary"));
    getDashboardFeed().then(setFeed).catch((e) => setError(e instanceof DashboardApiError ? e.message : "Failed to load dashboard feed"));
    getDashboardInsights().then(setInsights).catch(() => {
      // Non-fatal — insights panel just stays empty if this fails.
    });
  }, []);

  if (error) {
    return (
      <AppShell>
        <div className="p-6 text-sm text-red-400">{error}</div>
      </AppShell>
    );
  }

  const kpiCards = summary ? formatKpiCards(summary.kpis) : [];

  return (
    <AppShell>
      <PageHeader
        eyebrow="Security Operations"
        title="SOC Command Center"
        description="Real-time view of every phishing signal, investigation, and AI verdict across your organization."
        actions={
          <>
            <Button variant="outline" className="border-white/10">Last 24 hours</Button>
            <Button className="gradient-primary text-white glow-primary">Export Report</Button>
          </>
        }
      />

      {/* KPI grid */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
        {kpiCards.length === 0
          ? Array.from({ length: 8 }).map((_, i) => (
              <GlassCard key={i} className="h-[104px]">
                <div className="h-full w-full animate-pulse rounded-lg bg-white/5" />
              </GlassCard>
            ))
          : kpiCards.map((k, i) => (
              <StatCard key={k.label} label={k.label} value={k.value} delta={k.delta} tone={k.tone} icon={KPI_ICONS[i]} />
            ))}
      </div>

      {/* Charts row 1 */}
      <div className="mt-6 grid gap-4 lg:grid-cols-3">
        <GlassCard className="lg:col-span-2 min-h-[320px]">
          <SectionHeading
            title="Threat Trends"
            description="Detected vs. blocked, last 14 days"
            action={summary && <RiskBadge level={riskLevelToBadge(summary.kpis.riskLevel)} label={summary.kpis.riskLevel} />}
          />
          <div className="h-64">
            {summary && (
              <ResponsiveContainer>
                <AreaChart data={summary.threatTrend}>
                  <defs>
                    <linearGradient id="g1" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="0%" stopColor="#2563EB" stopOpacity={0.5} />
                      <stop offset="100%" stopColor="#2563EB" stopOpacity={0} />
                    </linearGradient>
                    <linearGradient id="g2" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="0%" stopColor="#06B6D4" stopOpacity={0.4} />
                      <stop offset="100%" stopColor="#06B6D4" stopOpacity={0} />
                    </linearGradient>
                  </defs>
                  <CartesianGrid stroke="rgba(255,255,255,0.06)" vertical={false} />
                  <XAxis dataKey="day" stroke="rgba(255,255,255,0.4)" fontSize={11} />
                  <YAxis stroke="rgba(255,255,255,0.4)" fontSize={11} />
                  <Tooltip contentStyle={{ background: "#0B1120", border: "1px solid rgba(255,255,255,0.1)", borderRadius: 8 }} />
                  <Area type="monotone" dataKey="threats" stroke="#2563EB" fill="url(#g1)" strokeWidth={2} />
                  <Area type="monotone" dataKey="blocked" stroke="#06B6D4" fill="url(#g2)" strokeWidth={2} />
                </AreaChart>
              </ResponsiveContainer>
            )}
          </div>
        </GlassCard>

        <GlassCard className="min-h-[320px]">
          <SectionHeading title="Attack Categories" description="Share of detected threats" />
          <div className="h-64">
            {summary && (
              <ResponsiveContainer>
                <PieChart>
                  <Pie data={summary.attackCategories} dataKey="value" nameKey="name" innerRadius={45} outerRadius={80} paddingAngle={3}>
                    {summary.attackCategories.map((_, i) => <Cell key={i} fill={CHART_COLORS[i % CHART_COLORS.length]} />)}
                  </Pie>
                  <Tooltip contentStyle={{ background: "#0B1120", border: "1px solid rgba(255,255,255,0.1)", borderRadius: 8 }} />
                </PieChart>
              </ResponsiveContainer>
            )}
          </div>
          <div className="grid grid-cols-2 gap-2 mt-2">
            {summary?.attackCategories.map((c, i) => (
              <div key={c.name} className="flex items-center gap-2 text-xs">
                <span className="h-2 w-2 rounded-full" style={{ background: CHART_COLORS[i % CHART_COLORS.length] }} />
                <span className="text-muted-foreground flex-1 truncate">{c.name}</span>
                <span className="font-medium">{c.value}%</span>
              </div>
            ))}
          </div>
        </GlassCard>
      </div>

      {/* Charts row 2 */}
      <div className="mt-4 grid gap-4 lg:grid-cols-3">
        <GlassCard className="min-h-[280px]">
          <SectionHeading title="Daily Investigations" description="This week" />
          <div className="h-56">
            {summary && (
              <ResponsiveContainer>
                <BarChart data={summary.dailyInvestigations}>
                  <CartesianGrid stroke="rgba(255,255,255,0.06)" vertical={false} />
                  <XAxis dataKey="day" stroke="rgba(255,255,255,0.4)" fontSize={11} />
                  <YAxis stroke="rgba(255,255,255,0.4)" fontSize={11} />
                  <Tooltip contentStyle={{ background: "#0B1120", border: "1px solid rgba(255,255,255,0.1)", borderRadius: 8 }} />
                  <Bar dataKey="investigations" fill="#2563EB" radius={[6, 6, 0, 0]} />
                  <Bar dataKey="resolved" fill="#22C55E" radius={[6, 6, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            )}
          </div>
        </GlassCard>

        <GlassCard className="min-h-[280px]">
          <SectionHeading title="Risk Distribution" description="All investigations, 30d" />
          <div className="space-y-3 mt-2">
            {summary?.riskDistribution.map((r, i) => (
              <div key={r.name}>
                <div className="flex items-center justify-between text-xs mb-1">
                  <span className="text-muted-foreground">{r.name}</span>
                  <span className="font-medium">{r.value}%</span>
                </div>
                <div className="h-2 rounded-full bg-white/5 overflow-hidden">
                  <motion.div
                    initial={{ width: 0 }} whileInView={{ width: `${r.value}%` }} viewport={{ once: true }}
                    transition={{ duration: 0.9, delay: i * 0.05 }}
                    className="h-full rounded-full"
                    style={{ background: CHART_COLORS[i % CHART_COLORS.length] }}
                  />
                </div>
              </div>
            ))}
          </div>
        </GlassCard>

        <GlassCard className="min-h-[280px]">
          <SectionHeading title="Threat Sources" description="Top originating countries" />
          <div className="h-56">
            {summary && summary.threatSources.length > 0 ? (
              <ResponsiveContainer>
                <BarChart data={summary.threatSources} layout="vertical">
                  <CartesianGrid stroke="rgba(255,255,255,0.06)" horizontal={false} />
                  <XAxis type="number" stroke="rgba(255,255,255,0.4)" fontSize={11} />
                  <YAxis type="category" dataKey="country" stroke="rgba(255,255,255,0.4)" fontSize={11} width={70} />
                  <Tooltip contentStyle={{ background: "#0B1120", border: "1px solid rgba(255,255,255,0.1)", borderRadius: 8 }} />
                  <Bar dataKey="value" fill="#06B6D4" radius={[0, 6, 6, 0]} />
                </BarChart>
              </ResponsiveContainer>
            ) : (
              summary && <div className="h-full grid place-items-center text-xs text-muted-foreground">No geo data yet</div>
            )}
          </div>
        </GlassCard>
      </div>

      {/* Table + alerts */}
      <div className="mt-6 grid gap-4 lg:grid-cols-[1.6fr_1fr]">
        <GlassCard>
          <SectionHeading
            title="Recent Investigations"
            description="Latest AI-driven verdicts"
            action={
              <Link to="/reports" className="text-xs text-cyan flex items-center gap-1 hover:underline">
                View all <ArrowUpRight className="h-3 w-3" />
              </Link>
            }
          />
          <div className="overflow-x-auto -mx-2">
            <table className="w-full text-sm">
              <thead>
                <tr className="text-left text-[11px] uppercase tracking-widest text-muted-foreground">
                  <th className="px-2 py-2">Date</th>
                  <th className="px-2 py-2">Source</th>
                  <th className="px-2 py-2">Target</th>
                  <th className="px-2 py-2">Threat</th>
                  <th className="px-2 py-2">Risk</th>
                  <th className="px-2 py-2">Status</th>
                  <th className="px-2 py-2"></th>
                </tr>
              </thead>
              <tbody>
                {feed?.recentInvestigations.map((i) => (
                  <tr key={i.id} className="border-t border-white/5 hover:bg-white/[0.03]">
                    <td className="px-2 py-3 text-muted-foreground text-xs">{i.date}</td>
                    <td className="px-2 py-3 font-mono text-xs truncate max-w-[200px]">{i.source}</td>
                    <td className="px-2 py-3 font-mono text-xs truncate max-w-[180px]">{i.target}</td>
                    <td className="px-2 py-3">{i.threatType}</td>
                    <td className="px-2 py-3">
                      <div className="flex items-center gap-2">
                        <span className="font-semibold">{i.riskScore}</span>
                        <RiskBadge level={scoreToLevel(i.riskScore)} />
                      </div>
                    </td>
                    <td className="px-2 py-3">
                      <span className="text-xs capitalize px-2 py-0.5 rounded-md bg-white/5 border border-white/10">{i.status}</span>
                    </td>
                    <td className="px-2 py-3">
                      <Button variant="ghost" size="icon" className="h-7 w-7"><MoreHorizontal className="h-4 w-4" /></Button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </GlassCard>

        <div className="space-y-4">
          <GlassCard>
            <SectionHeading title="Alert Feed" description="Live" action={<span className="h-2 w-2 rounded-full bg-red-500 animate-pulse" />} />
            <ul className="space-y-2">
              {feed?.alerts.map((a) => (
                <li key={a.id} className="rounded-lg border border-white/5 p-3 hover:border-white/15 transition">
                  <div className="flex items-center justify-between gap-2">
                    <RiskBadge level={a.severity as any} />
                    <span className="text-[10px] text-muted-foreground">{a.time}</span>
                  </div>
                  <div className="mt-2 text-sm">{a.title}</div>
                  <div className="mt-1 text-[11px] text-muted-foreground">{a.source} · {a.id}</div>
                </li>
              ))}
            </ul>
          </GlassCard>

          <GlassCard>
            <SectionHeading title="Security Recommendations" />
            <ul className="space-y-2">
              {insights?.recommendations.map((r, i) => (
                <li key={i} className="flex items-start gap-2 text-sm">
                  <span className="mt-1 h-1.5 w-1.5 rounded-full bg-cyan shrink-0" />
                  <span className="text-muted-foreground">{r}</span>
                </li>
              )) ?? <li className="text-xs text-muted-foreground">Loading…</li>}
            </ul>
          </GlassCard>

          <GlassCard>
            <SectionHeading title="Latest AI Findings" />
            <ul className="space-y-3">
              {insights?.findings.map((f) => (
                <li key={f.title} className="rounded-lg glass p-3">
                  <div className="flex items-center justify-between">
                    <div className="text-sm font-medium">{f.title}</div>
                    <span className="text-xs font-bold gradient-text">{f.score}</span>
                  </div>
                  <div className="text-xs text-muted-foreground mt-1">{f.detail}</div>
                </li>
              )) ?? <li className="text-xs text-muted-foreground">Loading…</li>}
              {insights && insights.findings.length === 0 && (
                <li className="text-xs text-muted-foreground">No clustered patterns in the last 48h.</li>
              )}
            </ul>
          </GlassCard>
        </div>
      </div>
    </AppShell>
  );
}

function riskLevelToBadge(level: string): "safe" | "low" | "suspicious" | "high" | "critical" {
  if (level === "Critical") return "critical";
  if (level === "Elevated") return "suspicious";
  return "low";
}