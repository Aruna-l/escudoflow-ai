import { createFileRoute } from "@tanstack/react-router";
import { useRef, useState } from "react";
import { motion } from "framer-motion";
import { Upload, FileWarning, Copy, ShieldAlert } from "lucide-react";
import { AppShell, PageHeader } from "@/components/app-shell";
import { GlassCard, RiskBadge, RiskMeter, SectionHeading } from "@/components/cyber-ui";
import { Button } from "@/components/ui/button";
import { analyzeAttachment, type AttachmentAnalysis } from "@/lib/attachment-api";

export const Route = createFileRoute("/attachment-intelligence")({
  head: () => ({
    meta: [
      { title: "Attachment Intelligence — EscudoFlow AI" },
      { name: "description", content: "Static and dynamic analysis of PDF, Office, archive, and executable attachments." },
      { property: "og:title", content: "Attachment Intelligence — EscudoFlow AI" },
      { property: "og:description", content: "Detect malicious macros, embedded scripts, and droppers in attachments." },
    ],
  }),
  component: AttachIntel,
});

function AttachIntel() {
  const [d, setD] = useState<AttachmentAnalysis | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [selectedFileName, setSelectedFileName] = useState<string | null>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  async function handleFileSelected(file: File | undefined) {
    if (!file) return;
    setSelectedFileName(file.name);
    setError(null);
    try {
      const analysis = await analyzeAttachment(file);
      setD(analysis);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to analyze file.");
      setD(null);
    }
  }

  return (
    <AppShell>
      <PageHeader
        eyebrow="Attachment Intelligence"
        title="Malicious File Analysis"
        description="Upload any suspicious attachment for static and behavioral analysis, macro detection, and embedded-script inspection."
      />

      <GlassCard className="mb-6">
        <div className="rounded-xl border-2 border-dashed border-white/15 p-10 text-center hover:border-cyan/50 transition">
          <div className="mx-auto grid place-items-center h-14 w-14 rounded-2xl gradient-primary glow-primary">
            <Upload className="h-6 w-6 text-white" />
          </div>
          <div className="mt-4 font-semibold">
            {selectedFileName ? selectedFileName : "Drop a file to analyze"}
          </div>
          <div className="text-xs text-muted-foreground mt-1">Supported: PDF · DOCX · ZIP · RAR · EXE · JS · up to 32 MB</div>
          {error && <div className="text-xs text-red-400 mt-2">{error}</div>}

          <input
            ref={inputRef}
            type="file"
            className="hidden"
            onChange={(e) => handleFileSelected(e.target.files?.[0])}
          />
          <Button className="mt-4 gradient-primary text-white glow-primary" onClick={() => inputRef.current?.click()}>
            {selectedFileName ? "Choose a different file" : "Choose file"}
          </Button>
        </div>
      </GlassCard>

      {d && (
        <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} className="space-y-6">
          <div className="grid gap-4 lg:grid-cols-3">
            <GlassCard className="lg:col-span-1">
              <RiskMeter score={d.riskScore} label="Attachment Risk" />
            </GlassCard>
            <GlassCard className="lg:col-span-2">
              <SectionHeading title="File Metadata" />
              <div className="grid sm:grid-cols-2 gap-3 text-sm">
                <Field label="Filename" value={d.fileName} />
                <Field label="Type" value={d.fileType} />
                <Field label="Size" value={d.size} />
                <Field label="Macros" value={d.macros ? "Detected" : "None"} tone={d.macros ? "red" : "green"} />
                <Field label="Embedded Scripts" value={String(d.embeddedScripts)} tone={d.embeddedScripts ? "red" : "green"} />
                <Field label="Suspicious Executables" value={String(d.suspiciousExecutables)} tone={d.suspiciousExecutables ? "red" : "green"} />
              </div>
              <div className="mt-4 rounded-lg glass p-3">
                <div className="flex items-center justify-between text-xs text-muted-foreground">
                  <span>SHA-256</span>
                  <button
                    className="hover:text-white flex items-center gap-1"
                    onClick={() => navigator.clipboard.writeText(d.sha256)}
                  >
                    <Copy className="h-3 w-3" /> copy
                  </button>
                </div>
                <div className="mt-1 font-mono text-[11px] break-all">{d.sha256}</div>
              </div>
            </GlassCard>
          </div>

          <GlassCard>
            <div className="flex items-center gap-2 mb-3"><FileWarning className="h-4 w-4 text-red-400" />
              <SectionHeading title="Threat Summary" />
            </div>
            {d.threats.length === 0 ? (
              <p className="text-sm text-muted-foreground">No threat indicators found.</p>
            ) : (
              <ul className="space-y-2">
                {d.threats.map((t, i) => (
                  <li key={i} className="flex items-center justify-between rounded-lg glass px-3 py-2.5">
                    <span className="text-sm">{t.name}</span>
                    <RiskBadge level={t.severity as "safe" | "low" | "suspicious" | "high" | "critical"} />
                  </li>
                ))}
              </ul>
            )}
          </GlassCard>

          <GlassCard>
            <div className="flex items-center gap-2 mb-3"><ShieldAlert className="h-4 w-4 text-cyan" />
              <SectionHeading title="Recommendation" />
            </div>
            <p className="text-sm text-muted-foreground leading-relaxed max-w-3xl">{d.recommendation}</p>
          </GlassCard>
        </motion.div>
      )}
    </AppShell>
  );
}

function Field({ label, value, tone }: { label: string; value: string; tone?: "red" | "green" }) {
  const color = tone === "red" ? "text-red-400" : tone === "green" ? "text-emerald-400" : "";
  return (
    <div className="rounded-lg glass p-3">
      <div className="text-[10px] uppercase tracking-widest text-muted-foreground">{label}</div>
      <div className={`mt-1 text-sm font-medium ${color}`}>{value}</div>
    </div>
  );
}
