import { createFileRoute } from "@tanstack/react-router";
import { useState } from "react";
import { User, Building2, Bell, Palette, Globe, KeyRound, Lock, ShieldCheck } from "lucide-react";
import { AppShell, PageHeader } from "@/components/app-shell";
import { GlassCard, SectionHeading } from "@/components/cyber-ui";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Switch } from "@/components/ui/switch";

export const Route = createFileRoute("/settings")({
  head: () => ({
    meta: [
      { title: "Settings — EscudoFlow AI" },
      { name: "description", content: "Manage profile, organization, notifications, API keys, and security." },
      { property: "og:title", content: "Settings — EscudoFlow AI" },
      { property: "og:description", content: "Manage your EscudoFlow account and organization." },
    ],
  }),
  component: Settings,
});

const TABS = [
  { id: "profile", label: "Profile", icon: User },
  { id: "org", label: "Organization", icon: Building2 },
  { id: "notif", label: "Notifications", icon: Bell },
  { id: "theme", label: "Theme", icon: Palette },
  { id: "lang", label: "Language", icon: Globe },
  { id: "api", label: "API Keys", icon: KeyRound },
  { id: "security", label: "Security", icon: Lock },
] as const;

function Settings() {
  const [tab, setTab] = useState<(typeof TABS)[number]["id"]>("profile");
  return (
    <AppShell>
      <PageHeader eyebrow="Settings" title="Account & Organization" description="Manage your workspace, security posture, and integrations." />
      <div className="grid gap-6 lg:grid-cols-[240px_1fr]">
        <GlassCard className="h-fit">
          <nav className="space-y-1">
            {TABS.map((t) => (
              <button
                key={t.id}
                onClick={() => setTab(t.id)}
                className={`w-full flex items-center gap-2 px-3 py-2 rounded-lg text-sm transition ${
                  tab === t.id ? "bg-white/5 text-white" : "text-muted-foreground hover:text-white"
                }`}
              >
                <t.icon className="h-4 w-4" /> {t.label}
              </button>
            ))}
          </nav>
        </GlassCard>

        <div className="space-y-6">
          {tab === "profile" && (
            <GlassCard>
              <SectionHeading title="Profile" description="Your personal information" />
              <div className="grid sm:grid-cols-2 gap-4">
                <Field label="Full Name" defaultValue="Priya Ramanathan" />
                <Field label="Email" defaultValue="priya@acme.com" />
                <Field label="Role" defaultValue="Senior SOC Analyst" />
                <Field label="Time Zone" defaultValue="Asia/Kolkata (UTC+5:30)" />
              </div>
              <div className="mt-4"><Button className="gradient-primary text-white glow-primary">Save changes</Button></div>
            </GlassCard>
          )}
          {tab === "org" && (
            <GlassCard>
              <SectionHeading title="Organization" />
              <div className="grid sm:grid-cols-2 gap-4">
                <Field label="Organization" defaultValue="Acme Corp" />
                <Field label="Domain" defaultValue="acme.com" />
                <Field label="Tenant ID" defaultValue="af_ten_9a02d1c0" />
                <Field label="Region" defaultValue="EU-West-1" />
              </div>
            </GlassCard>
          )}
          {tab === "notif" && (
            <GlassCard>
              <SectionHeading title="Notifications" />
              <div className="space-y-3">
                {["Critical incidents","Weekly summary","New AI findings","Product updates"].map((n) => (
                  <div key={n} className="flex items-center justify-between rounded-lg glass px-3 py-2.5">
                    <span className="text-sm">{n}</span>
                    <Switch defaultChecked />
                  </div>
                ))}
              </div>
            </GlassCard>
          )}
          {tab === "theme" && (
            <GlassCard>
              <SectionHeading title="Theme" description="EscudoFlow ships with a dark-first enterprise theme optimized for 24/7 SOC use." />
              <div className="grid sm:grid-cols-3 gap-3">
                {["Deep Navy","Midnight","Contrast"].map((t, i) => (
                  <div key={t} className={`rounded-xl p-4 border ${i === 0 ? "border-cyan/40 gradient-primary/10" : "border-white/10 glass"}`}>
                    <div className="h-16 rounded-lg" style={{ background: i === 0 ? "linear-gradient(135deg,#0B1120,#2563EB)" : i === 1 ? "linear-gradient(135deg,#020617,#0f172a)" : "linear-gradient(135deg,#000,#334155)" }} />
                    <div className="mt-2 text-sm font-medium">{t}</div>
                  </div>
                ))}
              </div>
            </GlassCard>
          )}
          {tab === "lang" && (
            <GlassCard>
              <SectionHeading title="Language" />
              <div className="max-w-sm"><Field label="Preferred Language" defaultValue="English (US)" /></div>
            </GlassCard>
          )}
          {tab === "api" && (
            <GlassCard>
              <SectionHeading title="API Keys" description="For FastAPI backend integration" action={<Button className="gradient-primary text-white">Generate key</Button>} />
              <div className="space-y-2">
                {[
                  { name: "Production", key: "af_prod_9f8a…c421", created: "2026-06-01" },
                  { name: "Staging", key: "af_stg_2a91…d093", created: "2026-06-14" },
                ].map((k) => (
                  <div key={k.key} className="flex items-center justify-between rounded-lg glass px-3 py-3">
                    <div>
                      <div className="text-sm font-medium">{k.name}</div>
                      <div className="text-xs font-mono text-muted-foreground">{k.key}</div>
                    </div>
                    <div className="text-xs text-muted-foreground">Created {k.created}</div>
                  </div>
                ))}
              </div>
            </GlassCard>
          )}
          {tab === "security" && (
            <div className="space-y-6">
              <GlassCard>
                <SectionHeading title="Password" />
                <div className="grid sm:grid-cols-2 gap-4">
                  <Field label="Current password" type="password" />
                  <div />
                  <Field label="New password" type="password" />
                  <Field label="Confirm new password" type="password" />
                </div>
                <div className="mt-4"><Button className="gradient-primary text-white glow-primary">Update password</Button></div>
              </GlassCard>
              <GlassCard>
                <SectionHeading title="Two-Factor Authentication" />
                <div className="flex items-center justify-between rounded-lg glass px-3 py-3">
                  <div className="flex items-center gap-3">
                    <ShieldCheck className="h-5 w-5 text-emerald-400" />
                    <div>
                      <div className="text-sm font-medium">Authenticator App</div>
                      <div className="text-xs text-muted-foreground">Time-based one-time passwords</div>
                    </div>
                  </div>
                  <Switch defaultChecked />
                </div>
              </GlassCard>
            </div>
          )}
        </div>
      </div>
    </AppShell>
  );
}

function Field({ label, defaultValue, type = "text" }: { label: string; defaultValue?: string; type?: string }) {
  return (
    <label className="block">
      <div className="text-xs uppercase tracking-widest text-muted-foreground mb-1.5">{label}</div>
      <Input defaultValue={defaultValue} type={type} className="glass border-white/10 h-11" />
    </label>
  );
}
