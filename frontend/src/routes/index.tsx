import { createFileRoute, Link } from "@tanstack/react-router";
import { motion } from "framer-motion";
import {
  Shield, ArrowRight, Mail, Link2, Eye, Paperclip, Globe2, Brain,
  Building2, FileText, Activity, Layers, ShieldAlert, GitBranch,
  Sparkles, Zap, Lock, CheckCircle2, X as XIcon,
} from "lucide-react";
import { AppShell, PageHeader } from "@/components/app-shell";
import { GlassCard, SectionHeading } from "@/components/cyber-ui";
import { AnimatedNumber } from "@/hooks/use-animated-number";
import { HOMEPAGE_STATS } from "@/lib/mock-data";
import { Button } from "@/components/ui/button";

export const Route = createFileRoute("/")({
  head: () => ({
    meta: [
      { title: "EscudoFlow AI — Intelligent Phishing Detection & Threat Intelligence" },
      { name: "description", content: "Enterprise AI platform to detect, analyze, and explain phishing across email, URLs, brand clones, and attachments." },
      { property: "og:title", content: "EscudoFlow AI" },
      { property: "og:description", content: "AI-powered phishing detection & explainable threat intelligence for security teams." },
    ],
  }),
  component: Home,
});

const FEATURES = [
  { icon: Mail, title: "AI Email Intelligence", desc: "Transformer-based classification of BEC, phishing, and impersonation with per-sentence attribution." },
  { icon: Link2, title: "URL Intelligence Engine", desc: "WHOIS, DNS, SSL, redirect chains, and behavioral URL scoring in under 2 seconds." },
  { icon: Eye, title: "Visual Brand Detection", desc: "CLIP-powered clone recognition — spot fake login pages of Microsoft, Google, and 400+ brands." },
  { icon: Activity, title: "Behavioral URL Sandbox", desc: "Headless Playwright execution reveals credential forms, exfil hops, and JS obfuscation." },
  { icon: Globe2, title: "Threat Intel Correlation", desc: "Enrich every IOC against VirusTotal, PhishTank, AbuseIPDB, and internal feeds." },
  { icon: Brain, title: "Explainable AI Reports", desc: "SHAP + LIME reasoning surfaces the exact features that drove every verdict." },
  { icon: Building2, title: "BEC Detection", desc: "Detect CEO-fraud, wire-fraud, and payroll-diversion using linguistic and header fingerprints." },
  { icon: Paperclip, title: "Attachment Risk Analysis", desc: "Macro, embedded-script, and executable inspection for PDFs, Office docs, and archives." },
  { icon: Layers, title: "Risk Scoring Engine", desc: "Unified 0-100 score fusing URL, header, content, visual, and IOC signals." },
  { icon: ShieldAlert, title: "Organization Threat Modeling", desc: "Map campaigns to your org — who was targeted, who clicked, and what's at risk." },
  { icon: GitBranch, title: "Incident Timeline", desc: "Automatic chronological reconstruction of every step of an attack." },
  { icon: FileText, title: "Interactive Reports", desc: "One-click executive & analyst reports exportable as PDF, CSV, or JSON." },
];

const WORKFLOW = [
  { icon: Mail, label: "Email" },
  { icon: Link2, label: "URL" },
  { icon: Brain, label: "AI Agents" },
  { icon: Activity, label: "Behavior Analysis" },
  { icon: Globe2, label: "Threat Intelligence" },
  { icon: Layers, label: "Risk Engine" },
  { icon: Sparkles, label: "Explainable AI" },
  { icon: FileText, label: "Incident Report" },
];

function Home() {
  return (
    <AppShell sidebar={false}>
      {/* Hero */}
      <section className="relative -mx-4 sm:-mx-6 -mt-8 px-4 sm:px-6 pt-10 pb-24 hero-bg overflow-hidden">
        <div className="grid lg:grid-cols-[1.15fr_1fr] gap-10 items-center max-w-[1280px] mx-auto">
          <div>
            <motion.div
              initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}
              className="inline-flex items-center gap-2 rounded-full glass px-3 py-1 text-xs text-muted-foreground"
            >
              <span className="h-1.5 w-1.5 rounded-full bg-emerald-400 animate-pulse" />
              Live threat models · v4.2 released
            </motion.div>
            <motion.h1
              initial={{ opacity: 0, y: 14 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.05 }}
              className="mt-5 text-5xl md:text-6xl font-bold tracking-tight leading-[1.05]"
            >
              EscudoFlow <span className="gradient-text">AI</span>
            </motion.h1>
            <motion.p
              initial={{ opacity: 0, y: 14 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.1 }}
              className="mt-3 text-lg md:text-xl font-medium text-cyan"
            >
              Intelligent Phishing Detection & Threat Intelligence Platform
            </motion.p>
            <motion.p
              initial={{ opacity: 0, y: 14 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.15 }}
              className="mt-5 max-w-xl text-muted-foreground leading-relaxed"
            >
              Detect, analyze, and explain phishing attacks using Artificial Intelligence,
              Machine Learning, Explainable AI, Behavioral URL Analysis, Threat Intelligence,
              and Multi-Modal Intelligence — in a single enterprise-grade platform.
            </motion.p>
            <motion.div
              initial={{ opacity: 0, y: 14 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.2 }}
              className="mt-8 flex flex-wrap gap-3"
            >
              <Link to="/url-intelligence" className="inline-flex items-center gap-2 gradient-primary text-white px-5 py-3 rounded-xl glow-primary hover:opacity-95 transition font-medium">
                Start Investigation <ArrowRight className="h-4 w-4" />
              </Link>
              <Link to="/dashboard" className="inline-flex items-center gap-2 glass px-5 py-3 rounded-xl hover:border-white/20 border border-white/10 transition">
                View Dashboard
              </Link>
            </motion.div>
            <div className="mt-8 flex flex-wrap items-center gap-4 text-xs text-muted-foreground">
              {["SOC 2 Type II","ISO 27001","GDPR","HIPAA-ready"].map((b) => (
                <div key={b} className="flex items-center gap-1.5"><CheckCircle2 className="h-3.5 w-3.5 text-emerald-400" /> {b}</div>
              ))}
            </div>
          </div>

          <HeroIllustration />
        </div>
      </section>

      {/* Stats */}
      <section className="mt-4">
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
          {HOMEPAGE_STATS.map((s) => (
            <GlassCard key={s.label} className="text-center">
              <div className="text-2xl md:text-3xl font-bold gradient-text">
                <AnimatedNumber value={s.value} decimals={s.suffix === "s" || s.suffix === "%" ? 1 : 0} suffix={s.suffix} />
              </div>
              <div className="mt-1 text-[11px] uppercase tracking-widest text-muted-foreground">{s.label}</div>
            </GlassCard>
          ))}
        </div>
      </section>

      {/* Features */}
      <section className="mt-24">
        <PageHeader
          eyebrow="Platform Capabilities"
          title="Twelve intelligence engines. One platform."
          description="Every EscudoFlow module is production-ready, API-first, and fuses into a single risk score your team can act on."
        />
        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {FEATURES.map((f, i) => (
            <motion.div
              key={f.title}
              initial={{ opacity: 0, y: 12 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: i * 0.04 }}
            >
              <GlassCard className="h-full">
                <div className="grid place-items-center h-10 w-10 rounded-xl gradient-primary glow-primary">
                  <f.icon className="h-5 w-5 text-white" />
                </div>
                <h3 className="mt-4 text-base font-semibold">{f.title}</h3>
                <p className="mt-1.5 text-sm text-muted-foreground leading-relaxed">{f.desc}</p>
              </GlassCard>
            </motion.div>
          ))}
        </div>
      </section>

      {/* How it works */}
      <section className="mt-24">
        <PageHeader
          eyebrow="How it works"
          title="From inbound message to explainable verdict."
          description="EscudoFlow orchestrates specialized AI agents through a deterministic pipeline — every step logged, every decision explained."
        />
        <GlassCard className="p-8">
          <div className="flex flex-wrap items-center justify-between gap-4">
            {WORKFLOW.map((step, i) => (
              <div key={step.label} className="flex items-center gap-3">
                <motion.div
                  initial={{ opacity: 0, scale: 0.85 }}
                  whileInView={{ opacity: 1, scale: 1 }}
                  viewport={{ once: true }}
                  transition={{ delay: i * 0.07 }}
                  className="flex flex-col items-center gap-2"
                >
                  <div className="relative grid place-items-center h-14 w-14 rounded-2xl glass border border-white/10">
                    <step.icon className="h-5 w-5 text-cyan" />
                    <span className="absolute inset-0 rounded-2xl border border-cyan/30 animate-pulse" />
                  </div>
                  <div className="text-xs font-medium text-center max-w-[100px]">{step.label}</div>
                </motion.div>
                {i < WORKFLOW.length - 1 && (
                  <div className="hidden md:block h-px w-8 bg-gradient-to-r from-white/30 to-transparent" />
                )}
              </div>
            ))}
          </div>
        </GlassCard>
      </section>

      {/* Why EscudoFlow */}
      <section className="mt-24">
        <PageHeader
          eyebrow="Why EscudoFlow AI"
          title="Beyond blocklists. Beyond binary verdicts."
          description="Traditional phishing detectors stop at a yes/no answer. EscudoFlow fuses multi-modal AI, behavior, and threat intelligence into one explainable risk score."
        />
        <GlassCard className="overflow-hidden p-0">
          <div className="grid grid-cols-1 md:grid-cols-2 divide-y md:divide-y-0 md:divide-x divide-white/5">
            <div className="p-6">
              <div className="flex items-center gap-2 text-xs uppercase tracking-widest text-muted-foreground">
                <span className="h-2 w-2 rounded-full bg-red-400" /> Traditional Phishing Detector
              </div>
              <ul className="mt-5 space-y-3">
                {["Binary prediction","Blocklist only","No explanation","URL only","Static detection","Reactive"].map((t) => (
                  <li key={t} className="flex items-start gap-3 text-sm text-muted-foreground">
                    <XIcon className="h-4 w-4 mt-0.5 text-red-400 shrink-0" /> {t}
                  </li>
                ))}
              </ul>
            </div>
            <div className="p-6 relative">
              <div className="absolute inset-0 bg-gradient-to-br from-cyan/5 via-transparent to-primary/5 pointer-events-none" />
              <div className="relative">
                <div className="flex items-center gap-2 text-xs uppercase tracking-widest text-cyan">
                  <span className="h-2 w-2 rounded-full bg-emerald-400 glow-cyan" /> EscudoFlow AI
                </div>
                <ul className="mt-5 space-y-3">
                  {["Multi-modal analysis (email, URL, visual, attachment)","Explainable AI with SHAP + LIME reasoning","Live threat intelligence correlation","Behavioral URL sandbox execution","Visual brand-clone detection","Unified 0–100 risk score"].map((t) => (
                    <li key={t} className="flex items-start gap-3 text-sm">
                      <CheckCircle2 className="h-4 w-4 mt-0.5 text-emerald-400 shrink-0" /> {t}
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          </div>
        </GlassCard>
      </section>

      {/* CTA */}
      <section className="mt-24">
        <GlassCard className="p-10 relative overflow-hidden">
          <div className="absolute inset-0 hero-bg opacity-70" />
          <div className="relative grid md:grid-cols-[1.4fr_1fr] gap-8 items-center">
            <div>
              <div className="inline-flex items-center gap-2 text-xs text-cyan uppercase tracking-widest"><Zap className="h-3.5 w-3.5" /> Deploy in minutes</div>
              <h2 className="mt-3 text-3xl md:text-4xl font-bold">Give your SOC AI-grade visibility.</h2>
              <p className="mt-3 text-muted-foreground max-w-xl">Start a free investigation now — no install required. Connect your mail gateway when you're ready.</p>
              <div className="mt-6 flex flex-wrap gap-3">
                <Link to="/signup" className="inline-flex items-center gap-2 gradient-primary text-white px-5 py-3 rounded-xl glow-primary">Get started free <ArrowRight className="h-4 w-4" /></Link>
                <Link to="/dashboard" className="inline-flex items-center gap-2 glass px-5 py-3 rounded-xl border border-white/10">Explore dashboard</Link>
              </div>
            </div>
            <div className="grid grid-cols-2 gap-3">
              {[
                { icon: Lock, k: "Encryption", v: "AES-256 at rest" },
                { icon: Shield, k: "Detection", v: "99.4% accuracy" },
                { icon: Zap, k: "Latency", v: "<2s per verdict" },
                { icon: Brain, k: "Explainable", v: "SHAP + LIME" },
              ].map((c) => (
                <div key={c.k} className="rounded-xl glass p-4">
                  <c.icon className="h-4 w-4 text-cyan" />
                  <div className="mt-3 text-xs uppercase tracking-widest text-muted-foreground">{c.k}</div>
                  <div className="font-semibold">{c.v}</div>
                </div>
              ))}
            </div>
          </div>
        </GlassCard>
      </section>
    </AppShell>
  );
}

function HeroIllustration() {
  const nodes = [
    { icon: Mail, x: "10%", y: "20%", delay: 0 },
    { icon: Link2, x: "80%", y: "15%", delay: 0.4 },
    { icon: Globe2, x: "88%", y: "70%", delay: 0.8 },
    { icon: Paperclip, x: "12%", y: "78%", delay: 1.2 },
    { icon: Eye, x: "50%", y: "8%", delay: 1.6 },
    { icon: Brain, x: "50%", y: "92%", delay: 2.0 },
  ];
  return (
    <div className="relative aspect-square w-full max-w-[520px] mx-auto">
      {/* Rings */}
      {[280, 220, 160].map((s, i) => (
        <motion.div
          key={s}
          className="absolute left-1/2 top-1/2 rounded-full border border-white/10"
          style={{ width: s, height: s, transform: "translate(-50%, -50%)" }}
          animate={{ rotate: 360 }}
          transition={{ duration: 30 + i * 10, repeat: Infinity, ease: "linear" }}
        >
          <span className="absolute -top-1 left-1/2 h-2 w-2 -translate-x-1/2 rounded-full bg-cyan glow-cyan" />
        </motion.div>
      ))}
      {/* Center shield */}
      <motion.div
        initial={{ scale: 0.9, opacity: 0 }} animate={{ scale: 1, opacity: 1 }} transition={{ duration: 0.6 }}
        className="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2"
      >
        <div className="relative grid place-items-center h-32 w-32 rounded-3xl gradient-primary glow-primary float-slow">
          <Shield className="h-14 w-14 text-white" strokeWidth={2.2} />
          <span className="absolute inset-0 rounded-3xl pulse-ring" />
        </div>
      </motion.div>
      {/* Nodes */}
      {nodes.map((n, i) => (
        <motion.div
          key={i}
          className="absolute grid place-items-center h-12 w-12 rounded-xl glass border border-white/10"
          style={{ left: n.x, top: n.y, transform: "translate(-50%, -50%)" }}
          initial={{ opacity: 0, scale: 0.6 }}
          animate={{ opacity: 1, scale: 1, y: [0, -6, 0] }}
          transition={{ delay: n.delay, duration: 4, repeat: Infinity, repeatType: "reverse" }}
        >
          <n.icon className="h-5 w-5 text-cyan" />
        </motion.div>
      ))}
      {/* Particles */}
      {Array.from({ length: 24 }).map((_, i) => (
        <motion.span
          key={i}
          className="absolute h-1 w-1 rounded-full bg-white/60"
          style={{ left: `${Math.random() * 100}%`, top: `${Math.random() * 100}%` }}
          animate={{ opacity: [0, 1, 0], scale: [0.5, 1.2, 0.5] }}
          transition={{ duration: 2 + Math.random() * 3, repeat: Infinity, delay: Math.random() * 3 }}
        />
      ))}
    </div>
  );
}
