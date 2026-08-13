import { createFileRoute } from "@tanstack/react-router";
import { useEffect, useState } from "react";
import {
  User,
  Building2,
  Bell,
  Palette,
  Globe,
  KeyRound,
  Lock,
  ShieldCheck,
  Copy,
} from "lucide-react";
import { AppShell, PageHeader } from "@/components/app-shell";
import { GlassCard, SectionHeading } from "@/components/cyber-ui";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Switch } from "@/components/ui/switch";
import api from "@/services/api";

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

type TabId = (typeof TABS)[number]["id"];

/* =====================================================
   TYPES (mirror backend Pydantic schemas)
   ===================================================== */

interface Profile {
  full_name: string;
  email: string;
  role: string | null;
  time_zone: string | null;
  two_factor_enabled: boolean;
}

interface Organization {
  name: string;
  domain: string;
  tenant_id: string;
  region: string;
}

interface Notifications {
  critical_incidents: boolean;
  weekly_summary: boolean;
  new_ai_findings: boolean;
  product_updates: boolean;
}

interface Preferences {
  theme: string;
  language: string;
}

interface ApiKey {
  name: string;
  key_preview: string;
  created_at: string;
}

const THEME_OPTIONS = ["Deep Navy", "Midnight", "Contrast"];
const LANGUAGE_OPTIONS = ["English (US)", "English (UK)", "Spanish", "French", "German", "Japanese"];

function Settings() {
  const [tab, setTab] = useState<TabId>("profile");

  return (
    <AppShell>
      <PageHeader
        eyebrow="Settings"
        title="Account & Organization"
        description="Manage your workspace, security posture, and integrations."
      />
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
          {tab === "profile" && <ProfileTab />}
          {tab === "org" && <OrganizationTab />}
          {tab === "notif" && <NotificationsTab />}
          {tab === "theme" && <ThemeTab />}
          {tab === "lang" && <LanguageTab />}
          {tab === "api" && <ApiKeysTab />}
          {tab === "security" && <SecurityTab />}
        </div>
      </div>
    </AppShell>
  );
}

/* =====================================================
   PROFILE
   ===================================================== */

function ProfileTab() {
  const [data, setData] = useState<Profile | null>(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    api
      .get<Profile>("/settings/profile")
      .then((res) => setData(res.data))
      .catch((err) => {
        console.error(err);
        alert(err?.response?.data?.detail || "Failed to load profile");
      })
      .finally(() => setLoading(false));
  }, []);

  const handleSave = async () => {
    if (!data) return;
    setSaving(true);
    try {
      const res = await api.put<Profile>("/settings/profile", {
        full_name: data.full_name,
        role: data.role,
        time_zone: data.time_zone,
      });
      setData(res.data);
      alert("Profile updated");
    } catch (err: any) {
      console.error(err);
      alert(err?.response?.data?.detail || "Failed to update profile");
    } finally {
      setSaving(false);
    }
  };

  if (loading) return <LoadingCard />;
  if (!data) return <ErrorCard />;

  return (
    <GlassCard>
      <SectionHeading title="Profile" description="Your personal information" />
      <div className="grid sm:grid-cols-2 gap-4">
        <Field
          label="Full Name"
          value={data.full_name}
          onChange={(v) => setData({ ...data, full_name: v })}
        />
        <Field label="Email" value={data.email} disabled />
        <Field
          label="Role"
          value={data.role ?? ""}
          onChange={(v) => setData({ ...data, role: v })}
        />
        <Field
          label="Time Zone"
          value={data.time_zone ?? ""}
          onChange={(v) => setData({ ...data, time_zone: v })}
        />
      </div>
      <div className="mt-4">
        <Button onClick={handleSave} disabled={saving} className="gradient-primary text-white glow-primary">
          {saving ? "Saving..." : "Save changes"}
        </Button>
      </div>
    </GlassCard>
  );
}

/* =====================================================
   ORGANIZATION
   ===================================================== */

function OrganizationTab() {
  const [data, setData] = useState<Organization | null>(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    api
      .get<Organization>("/settings/organization")
      .then((res) => setData(res.data))
      .catch((err) => {
        console.error(err);
        alert(err?.response?.data?.detail || "Failed to load organization");
      })
      .finally(() => setLoading(false));
  }, []);

  const handleSave = async () => {
    if (!data) return;
    setSaving(true);
    try {
      const res = await api.put<Organization>("/settings/organization", {
        name: data.name,
        domain: data.domain,
        region: data.region,
      });
      setData(res.data);
      alert("Organization updated");
    } catch (err: any) {
      console.error(err);
      alert(err?.response?.data?.detail || "Failed to update organization");
    } finally {
      setSaving(false);
    }
  };

  if (loading) return <LoadingCard />;
  if (!data) return <ErrorCard />;

  return (
    <GlassCard>
      <SectionHeading title="Organization" />
      <div className="grid sm:grid-cols-2 gap-4">
        <Field
          label="Organization"
          value={data.name}
          onChange={(v) => setData({ ...data, name: v })}
        />
        <Field
          label="Domain"
          value={data.domain}
          onChange={(v) => setData({ ...data, domain: v })}
        />
        <Field label="Tenant ID" value={data.tenant_id} disabled />
        <Field
          label="Region"
          value={data.region}
          onChange={(v) => setData({ ...data, region: v })}
        />
      </div>
      <div className="mt-4">
        <Button onClick={handleSave} disabled={saving} className="gradient-primary text-white glow-primary">
          {saving ? "Saving..." : "Save changes"}
        </Button>
      </div>
    </GlassCard>
  );
}

/* =====================================================
   NOTIFICATIONS
   ===================================================== */

const NOTIF_LABELS: { key: keyof Notifications; label: string }[] = [
  { key: "critical_incidents", label: "Critical incidents" },
  { key: "weekly_summary", label: "Weekly summary" },
  { key: "new_ai_findings", label: "New AI findings" },
  { key: "product_updates", label: "Product updates" },
];

function NotificationsTab() {
  const [data, setData] = useState<Notifications | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api
      .get<Notifications>("/settings/notifications")
      .then((res) => setData(res.data))
      .catch((err) => {
        console.error(err);
        alert(err?.response?.data?.detail || "Failed to load notifications");
      })
      .finally(() => setLoading(false));
  }, []);

  const handleToggle = async (key: keyof Notifications, checked: boolean) => {
    if (!data) return;
    const updated = { ...data, [key]: checked };
    setData(updated); // optimistic update

    try {
      await api.put<Notifications>("/settings/notifications", updated);
    } catch (err: any) {
      console.error(err);
      alert(err?.response?.data?.detail || "Failed to update notification");
      setData(data); // revert on failure
    }
  };

  if (loading) return <LoadingCard />;
  if (!data) return <ErrorCard />;

  return (
    <GlassCard>
      <SectionHeading title="Notifications" />
      <div className="space-y-3">
        {NOTIF_LABELS.map(({ key, label }) => (
          <div key={key} className="flex items-center justify-between rounded-lg glass px-3 py-2.5">
            <span className="text-sm">{label}</span>
            <Switch checked={data[key]} onCheckedChange={(checked) => handleToggle(key, checked)} />
          </div>
        ))}
      </div>
    </GlassCard>
  );
}

/* =====================================================
   THEME
   ===================================================== */

function ThemeTab() {
  const [data, setData] = useState<Preferences | null>(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    api
      .get<Preferences>("/settings/preferences")
      .then((res) => setData(res.data))
      .catch((err) => {
        console.error(err);
        alert(err?.response?.data?.detail || "Failed to load preferences");
      })
      .finally(() => setLoading(false));
  }, []);

  const handleSelect = async (theme: string) => {
    if (!data || saving) return;
    const updated = { ...data, theme };
    setData(updated);
    setSaving(true);
    try {
      await api.put<Preferences>("/settings/preferences", updated);
    } catch (err: any) {
      console.error(err);
      alert(err?.response?.data?.detail || "Failed to update theme");
    } finally {
      setSaving(false);
    }
  };

  if (loading) return <LoadingCard />;
  if (!data) return <ErrorCard />;

  return (
    <GlassCard>
      <SectionHeading
        title="Theme"
        description="EscudoFlow ships with a dark-first enterprise theme optimized for 24/7 SOC use."
      />
      <div className="grid sm:grid-cols-3 gap-3">
        {THEME_OPTIONS.map((t, i) => {
          const selected = data.theme === t;
          return (
            <button
              key={t}
              onClick={() => handleSelect(t)}
              className={`text-left rounded-xl p-4 border transition ${
                selected ? "border-cyan/40 gradient-primary/10" : "border-white/10 glass"
              }`}
            >
              <div
                className="h-16 rounded-lg"
                style={{
                  background:
                    i === 0
                      ? "linear-gradient(135deg,#0B1120,#2563EB)"
                      : i === 1
                      ? "linear-gradient(135deg,#020617,#0f172a)"
                      : "linear-gradient(135deg,#000,#334155)",
                }}
              />
              <div className="mt-2 text-sm font-medium">{t}</div>
            </button>
          );
        })}
      </div>
    </GlassCard>
  );
}

/* =====================================================
   LANGUAGE
   ===================================================== */

function LanguageTab() {
  const [data, setData] = useState<Preferences | null>(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    api
      .get<Preferences>("/settings/preferences")
      .then((res) => setData(res.data))
      .catch((err) => {
        console.error(err);
        alert(err?.response?.data?.detail || "Failed to load preferences");
      })
      .finally(() => setLoading(false));
  }, []);

  const handleSave = async () => {
    if (!data) return;
    setSaving(true);
    try {
      await api.put<Preferences>("/settings/preferences", data);
      alert("Language updated");
    } catch (err: any) {
      console.error(err);
      alert(err?.response?.data?.detail || "Failed to update language");
    } finally {
      setSaving(false);
    }
  };

  if (loading) return <LoadingCard />;
  if (!data) return <ErrorCard />;

  return (
    <GlassCard>
      <SectionHeading title="Language" />
      <div className="max-w-sm space-y-4">
        <label className="block">
          <div className="text-xs uppercase tracking-widest text-muted-foreground mb-1.5">
            Preferred Language
          </div>
          <select
            value={data.language}
            onChange={(e) => setData({ ...data, language: e.target.value })}
            className="w-full glass border border-white/10 rounded-md h-11 px-3 text-sm bg-transparent outline-none"
          >
            {LANGUAGE_OPTIONS.map((l) => (
              <option key={l} value={l} className="bg-[#0B1120]">
                {l}
              </option>
            ))}
          </select>
        </label>
        <Button onClick={handleSave} disabled={saving} className="gradient-primary text-white glow-primary">
          {saving ? "Saving..." : "Save changes"}
        </Button>
      </div>
    </GlassCard>
  );
}

/* =====================================================
   API KEYS
   ===================================================== */

function ApiKeysTab() {
  const [keys, setKeys] = useState<ApiKey[] | null>(null);
  const [loading, setLoading] = useState(true);
  const [creating, setCreating] = useState(false);
  const [revealedKey, setRevealedKey] = useState<{ name: string; key: string } | null>(null);

  const loadKeys = () => {
    setLoading(true);
    api
      .get<ApiKey[]>("/settings/api-keys")
      .then((res) => setKeys(res.data))
      .catch((err) => {
        console.error(err);
        alert(err?.response?.data?.detail || "Failed to load API keys");
      })
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    loadKeys();
  }, []);

  const handleGenerate = async () => {
    const name = window.prompt("Name this API key (e.g. Production, Staging):");
    if (!name) return;

    setCreating(true);
    try {
      const res = await api.post("/settings/api-keys", { name });
      setRevealedKey({ name: res.data.name, key: res.data.key });
      loadKeys();
    } catch (err: any) {
      console.error(err);
      alert(err?.response?.data?.detail || "Failed to create API key");
    } finally {
      setCreating(false);
    }
  };

  const handleCopy = (key: string) => {
    navigator.clipboard.writeText(key);
    alert("Copied to clipboard");
  };

  if (loading) return <LoadingCard />;

  return (
    <GlassCard>
      <SectionHeading
        title="API Keys"
        description="For FastAPI backend integration"
        action={
          <Button onClick={handleGenerate} disabled={creating} className="gradient-primary text-white">
            {creating ? "Generating..." : "Generate key"}
          </Button>
        }
      />

      {revealedKey && (
        <div className="mb-4 rounded-lg border border-cyan/40 bg-cyan/5 p-3">
          <div className="text-xs text-cyan mb-1">
            Copy "{revealedKey.name}" now — it will not be shown again.
          </div>
          <div className="flex items-center gap-2">
            <code className="flex-1 text-xs font-mono break-all">{revealedKey.key}</code>
            <button
              onClick={() => handleCopy(revealedKey.key)}
              className="text-muted-foreground hover:text-white"
            >
              <Copy className="h-4 w-4" />
            </button>
          </div>
        </div>
      )}

      <div className="space-y-2">
        {keys && keys.length === 0 && (
          <div className="text-sm text-muted-foreground">No API keys yet.</div>
        )}
        {keys?.map((k) => (
          <div key={k.key_preview} className="flex items-center justify-between rounded-lg glass px-3 py-3">
            <div>
              <div className="text-sm font-medium">{k.name}</div>
              <div className="text-xs font-mono text-muted-foreground">{k.key_preview}</div>
            </div>
            <div className="text-xs text-muted-foreground">
              Created {new Date(k.created_at).toLocaleDateString()}
            </div>
          </div>
        ))}
      </div>
    </GlassCard>
  );
}

/* =====================================================
   SECURITY
   ===================================================== */

function SecurityTab() {
  // Password change
  const [currentPassword, setCurrentPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [changingPassword, setChangingPassword] = useState(false);

  // 2FA
  const [twoFactorEnabled, setTwoFactorEnabled] = useState<boolean | null>(null);
  const [setupData, setSetupData] = useState<{ secret: string; otpauth_url: string } | null>(null);
  const [verifyCode, setVerifyCode] = useState("");
  const [busy2fa, setBusy2fa] = useState(false);

  useEffect(() => {
    api
      .get<Profile>("/settings/profile")
      .then((res) => setTwoFactorEnabled(res.data.two_factor_enabled))
      .catch((err) => console.error(err));
  }, []);

  const handleChangePassword = async () => {
    if (newPassword !== confirmPassword) {
      alert("New passwords do not match");
      return;
    }
    setChangingPassword(true);
    try {
      await api.put("/settings/security/password", {
        current_password: currentPassword,
        new_password: newPassword,
      });
      alert("Password updated");
      setCurrentPassword("");
      setNewPassword("");
      setConfirmPassword("");
    } catch (err: any) {
      console.error(err);
      alert(err?.response?.data?.detail || "Failed to update password");
    } finally {
      setChangingPassword(false);
    }
  };

  const handleToggle2FA = async (checked: boolean) => {
    if (checked) {
      // Start setup flow — don't flip the switch until verified
      setBusy2fa(true);
      try {
        const res = await api.post("/settings/security/2fa/setup");
        setSetupData(res.data);
      } catch (err: any) {
        console.error(err);
        alert(err?.response?.data?.detail || "Failed to start 2FA setup");
      } finally {
        setBusy2fa(false);
      }
    } else {
      setBusy2fa(true);
      try {
        await api.post("/settings/security/2fa/disable");
        setTwoFactorEnabled(false);
        setSetupData(null);
      } catch (err: any) {
        console.error(err);
        alert(err?.response?.data?.detail || "Failed to disable 2FA");
      } finally {
        setBusy2fa(false);
      }
    }
  };

  const handleVerify2FA = async () => {
    setBusy2fa(true);
    try {
      const res = await api.post("/settings/security/2fa/verify", { code: verifyCode });
      setTwoFactorEnabled(res.data.two_factor_enabled);
      setSetupData(null);
      setVerifyCode("");
      alert("Two-factor authentication enabled");
    } catch (err: any) {
      console.error(err);
      alert(err?.response?.data?.detail || "Invalid code");
    } finally {
      setBusy2fa(false);
    }
  };

  return (
    <div className="space-y-6">
      <GlassCard>
        <SectionHeading title="Password" />
        <div className="grid sm:grid-cols-2 gap-4">
          <Field
            label="Current password"
            type="password"
            value={currentPassword}
            onChange={setCurrentPassword}
          />
          <div />
          <Field label="New password" type="password" value={newPassword} onChange={setNewPassword} />
          <Field
            label="Confirm new password"
            type="password"
            value={confirmPassword}
            onChange={setConfirmPassword}
          />
        </div>
        <div className="mt-4">
          <Button
            onClick={handleChangePassword}
            disabled={changingPassword || !currentPassword || !newPassword}
            className="gradient-primary text-white glow-primary"
          >
            {changingPassword ? "Updating..." : "Update password"}
          </Button>
        </div>
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
          <Switch
            checked={twoFactorEnabled ?? false}
            disabled={busy2fa || twoFactorEnabled === null}
            onCheckedChange={handleToggle2FA}
          />
        </div>

        {setupData && (
          <div className="mt-4 rounded-lg border border-cyan/40 bg-cyan/5 p-4 space-y-3">
            <div className="text-sm">
              Scan this secret with your authenticator app, then enter the 6-digit code to confirm:
            </div>
            <code className="block text-xs font-mono break-all text-cyan">{setupData.secret}</code>
            <div className="flex gap-2">
              <Input
                value={verifyCode}
                onChange={(e) => setVerifyCode(e.target.value)}
                placeholder="123456"
                className="glass border-white/10 h-11 max-w-[160px]"
              />
              <Button
                onClick={handleVerify2FA}
                disabled={busy2fa || verifyCode.length === 0}
                className="gradient-primary text-white glow-primary"
              >
                Verify
              </Button>
            </div>
          </div>
        )}
      </GlassCard>
    </div>
  );
}

/* =====================================================
   SHARED HELPERS
   ===================================================== */

function Field({
  label,
  value,
  onChange,
  type = "text",
  disabled = false,
}: {
  label: string;
  value?: string;
  onChange?: (value: string) => void;
  type?: string;
  disabled?: boolean;
}) {
  return (
    <label className="block">
      <div className="text-xs uppercase tracking-widest text-muted-foreground mb-1.5">{label}</div>
      <Input
        value={value ?? ""}
        onChange={(e) => onChange?.(e.target.value)}
        type={type}
        disabled={disabled}
        className="glass border-white/10 h-11 disabled:opacity-60"
      />
    </label>
  );
}

function LoadingCard() {
  return (
    <GlassCard>
      <div className="text-sm text-muted-foreground">Loading...</div>
    </GlassCard>
  );
}

function ErrorCard() {
  return (
    <GlassCard>
      <div className="text-sm text-red-400">Failed to load. Please refresh the page.</div>
    </GlassCard>
  );
}
