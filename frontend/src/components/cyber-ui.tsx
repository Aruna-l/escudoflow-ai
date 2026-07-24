import { cn } from "@/lib/utils";
import type { ReactNode } from "react";
import { motion } from "framer-motion";

export function GlassCard({
  className, children, hover = true, glow = false,
}: { className?: string; children: ReactNode; hover?: boolean; glow?: boolean }) {
  return (
    <div
      className={cn(
        "relative rounded-2xl glass p-5 overflow-hidden",
        hover && "transition-all duration-300 hover:border-white/20 hover:-translate-y-0.5",
        glow && "glow-primary",
        className,
      )}
    >
      <div className="absolute inset-x-0 -top-px h-px bg-gradient-to-r from-transparent via-white/20 to-transparent" />
      {children}
    </div>
  );
}

const riskColorMap = {
  safe: "text-emerald-400 bg-emerald-500/10 border-emerald-500/30",
  low: "text-emerald-400 bg-emerald-500/10 border-emerald-500/30",
  suspicious: "text-amber-400 bg-amber-500/10 border-amber-500/30",
  high: "text-orange-400 bg-orange-500/10 border-orange-500/30",
  critical: "text-red-400 bg-red-500/10 border-red-500/30",
} as const;

export function RiskBadge({
  level, label, className,
}: { level: keyof typeof riskColorMap; label?: string; className?: string }) {
  return (
    <span
      className={cn(
        "inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md text-xs font-medium border uppercase tracking-wide",
        riskColorMap[level],
        className,
      )}
    >
      <span className="h-1.5 w-1.5 rounded-full bg-current" />
      {label ?? level}
    </span>
  );
}

export function scoreToLevel(score: number): keyof typeof riskColorMap {
  if (score >= 85) return "critical";
  if (score >= 65) return "high";
  if (score >= 40) return "suspicious";
  if (score >= 20) return "low";
  return "safe";
}

export function RiskMeter({ score, label = "Risk Score" }: { score: number; label?: string }) {
  const level = scoreToLevel(score);
  const color =
    level === "critical" ? "oklch(0.65 0.24 25)" :
    level === "high" ? "oklch(0.75 0.19 45)" :
    level === "suspicious" ? "oklch(0.80 0.17 75)" :
    level === "low" ? "oklch(0.75 0.19 145)" :
    "oklch(0.78 0.14 210)";
  const r = 52;
  const c = 2 * Math.PI * r;
  const offset = c - (score / 100) * c;
  return (
    <div className="flex items-center gap-5">
      <div className="relative h-32 w-32 shrink-0">
        <svg viewBox="0 0 120 120" className="h-full w-full -rotate-90">
          <circle cx="60" cy="60" r={r} fill="none" stroke="oklch(1 0 0 / 0.08)" strokeWidth="10" />
          <motion.circle
            cx="60" cy="60" r={r} fill="none" stroke={color} strokeWidth="10" strokeLinecap="round"
            strokeDasharray={c}
            initial={{ strokeDashoffset: c }}
            animate={{ strokeDashoffset: offset }}
            transition={{ duration: 1.2, ease: "easeOut" }}
            style={{ filter: `drop-shadow(0 0 12px ${color})` }}
          />
        </svg>
        <div className="absolute inset-0 grid place-items-center">
          <div className="text-center">
            <div className="text-3xl font-bold">{score}</div>
            <div className="text-[10px] uppercase tracking-widest text-muted-foreground">/ 100</div>
          </div>
        </div>
      </div>
      <div>
        <div className="text-xs uppercase tracking-widest text-muted-foreground">{label}</div>
        <div className="mt-1"><RiskBadge level={level} /></div>
        <div className="mt-2 text-xs text-muted-foreground max-w-[180px]">
          Model confidence based on 42 signals across URL, header, and behavior analysis.
        </div>
      </div>
    </div>
  );
}

export function StatCard({
  label, value, delta, tone = "primary", icon: Icon,
}: {
  label: string; value: string | number; delta?: string;
  tone?: "primary" | "cyan" | "success" | "warning" | "danger";
  icon?: React.ComponentType<{ className?: string }>;
}) {
  const toneMap = {
    primary: "text-primary bg-primary/10",
    cyan: "text-cyan bg-cyan/10",
    success: "text-emerald-400 bg-emerald-500/10",
    warning: "text-amber-400 bg-amber-500/10",
    danger: "text-red-400 bg-red-500/10",
  };
  return (
    <GlassCard>
      <div className="flex items-start justify-between gap-3">
        <div className="min-w-0">
          <div className="text-xs uppercase tracking-widest text-muted-foreground truncate">{label}</div>
          <div className="mt-2 text-2xl font-bold">{value}</div>
          {delta && <div className="mt-1 text-xs text-muted-foreground">{delta}</div>}
        </div>
        {Icon && (
          <div className={cn("grid place-items-center h-9 w-9 rounded-lg shrink-0", toneMap[tone])}>
            <Icon className="h-4 w-4" />
          </div>
        )}
      </div>
    </GlassCard>
  );
}

export function SectionHeading({ title, description, action }: { title: string; description?: string; action?: ReactNode }) {
  return (
    <div className="flex items-end justify-between gap-4 mb-4">
      <div>
        <h2 className="text-lg font-semibold">{title}</h2>
        {description && <p className="text-sm text-muted-foreground">{description}</p>}
      </div>
      {action}
    </div>
  );
}
