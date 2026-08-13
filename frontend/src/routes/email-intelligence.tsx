import { createFileRoute } from "@tanstack/react-router";
import { useState, useRef } from "react";
import axios from "axios";
import { motion } from "framer-motion";
import { Mail, Upload, ShieldAlert, Highlighter } from "lucide-react";
import { AppShell, PageHeader } from "@/components/app-shell";
import { GlassCard, RiskBadge, RiskMeter, SectionHeading } from "@/components/cyber-ui";
import { Button } from "@/components/ui/button";
import { getSessionId } from "@/lib/session-id";
import { usePersistedState } from "@/lib/persisted-state";


export const Route = createFileRoute("/email-intelligence")({
  head: () => ({
    meta: [
      { title: "Email Intelligence — EscudoFlow AI" },
      { name: "description", content: "AI-powered analysis of phishing, BEC, impersonation, and header authenticity for inbound emails." },
      { property: "og:title", content: "Email Intelligence — EscudoFlow AI" },
      { property: "og:description", content: "Detect BEC, phishing, and impersonation with per-sentence AI reasoning." },
    ],
  }),
  component: EmailIntel,
});

function EmailIntel() {
  const [loading, setLoading] = useState(false);

  const [analysis, setAnalysis, clearAnalysis] = usePersistedState<any>("escudoflow_email_analysis", null);
  const [analyzed, setAnalyzed, clearAnalyzed] = usePersistedState("escudoflow_email_analyzed", false);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);

  const fileInputRef = useRef<HTMLInputElement>(null);
  const [emailText, setEmailText] = useState(
  `From: ceo@acmee-corp.com
  Reply-To: ceo.finance@protonmail.com
  To: cfo@acme.com
  Subject: URGENT: Wire transfer authorization needed today

  URGENT — do not discuss with anyone else on the team.

  Wire $248,500 today to secure the acquisition.

  I'm in back-to-back board meetings, only reply to this address.

  — John`
  );
  const analyzeEmail = async () => {

    if (!emailText.trim()) return;

    setLoading(true);

    try {

        const response = await axios.post(
    "http://127.0.0.1:8000/email/analyze",
    { email: emailText },
    { headers: { "X-Session-Id": getSessionId() } }
);

        console.log(response.data);

        setAnalysis(response.data);
        setEmailText(
        `From: ${response.data.from_email}
        Reply-To: ${response.data.reply_to}
        Subject: ${response.data.subject}

        ${response.data.body}`
        );

        setAnalyzed(true);

    } catch (err) {

        console.error(err);

    } finally {

        setLoading(false);

    }

};

const uploadEmail = async () => {
  if (!selectedFile) return;

  const formData = new FormData();
  formData.append("file", selectedFile);

  setLoading(true);

  try {
    const response = await axios.post(
  "http://127.0.0.1:8000/email/upload",
  formData,
  { headers: { "Content-Type": "multipart/form-data", "X-Session-Id": getSessionId() } }
);

    console.log(response.data);

    setAnalysis(response.data);

    setEmailText(
    `From: ${response.data.from_email}
    Reply-To: ${response.data.reply_to}
    Subject: ${response.data.subject}

    ${response.data.body}`
    );
    setAnalyzed(true);
  } catch (err) {
    console.error(err);
  } finally {
    setLoading(false);
  }
};
const d = analysis ?? {};

  const entityList = [
  ...(d.entities?.person ?? []).map((x: string) => ({
    type: "Person",
    value: x,
  })),
  ...(d.entities?.amount ?? []).map((x: string) => ({
    type: "Amount",
    value: x,
  })),
  ...(d.entities?.bank ?? []).map((x: string) => ({
    type: "Bank",
    value: x,
  })),
  ...(d.entities?.deadline ?? []).map((x: string) => ({
    type: "Deadline",
    value: x,
  })),
];

  return (
    <AppShell>
      <PageHeader
        eyebrow="Email Intelligence"
        title="AI-Powered Email Analysis"
        description="Paste an email or upload a .eml file. EscudoFlow scores phishing, BEC, urgency, and impersonation risk with explainable reasoning."
      />

      <div className="grid gap-6 lg:grid-cols-[1.1fr_1fr]">
        <GlassCard>
          <SectionHeading title="Input" description="Paste headers + body, or drop a .eml file" />
          <textarea
              value={emailText}
              onChange={(e) => setEmailText(e.target.value)}
              className="w-full h-72 rounded-xl glass p-4 font-mono text-xs outline-none resize-none"
          />
          <input
            type="file"
            accept=".eml"
            ref={fileInputRef}
            style={{ display: "none" }}
            onChange={(e) => {
              if (e.target.files?.length) {
                setSelectedFile(e.target.files[0]);
              }
            }}
          />
          <div className="mt-3 flex gap-2">
            <Button
                onClick={() => {
                  if (selectedFile) {
                    uploadEmail();
                  } else {
                    analyzeEmail();
                  }
                }}
                disabled={loading}
                className="gradient-primary text-white glow-primary flex-1"
            >
                {loading ? "Analyzing..." : "Analyze"}
            </Button>
            <Button
              variant="outline"
              className="border-white/10 flex-1"
              onClick={() => fileInputRef.current?.click()}
            >
              <Upload className="h-4 w-4 mr-2" />
              {selectedFile ? selectedFile.name : "Upload .eml"}
            </Button>
          </div>
        </GlassCard>
        
        {analysis && (
        <GlassCard>
          <SectionHeading title="Verdict" />
          <RiskMeter score={d.overallRisk ?? d.riskScore} label="Overall Risk" />
          <div className="mt-5 grid grid-cols-3 gap-2">
           <Metric
              label="Phishing"
              value={`${Math.round(d.phishingProbability * 100)}%`}
              tone="red"
            />

           <Metric
              label="BEC"
              value={d.bec ? "YES" : "NO"}
              tone={d.bec ? "red" : "green"}
            />

            <Metric
              label="Spam"
              value={d.spamScore}
              tone="amber"
            />

            <Metric
                label="Urgency"
                value={`${Math.round(d.urgency * 100)}%`}
                tone="amber"
            />

            <Metric
                label="Impersonation"
                value={`${Math.round(d.impersonation * 100)}%`}
                tone="red"
            />

            <Metric
                label="Reputation"
                value={d.reputation}
                tone="amber"
            />
          </div>
        </GlassCard>
        )}
      </div>

      {analysis && (
        <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} className="mt-6 space-y-6">
          <div className="grid gap-4 lg:grid-cols-3">
            <GlassCard>
              <SectionHeading title="Authentication" />
              <div className="grid grid-cols-3 gap-2">
                {(["spf","dkim","dmarc"] as const).map((k) => {
                  const v = d.authentication?.[k];
                  const pass = v === "PASS";
              
                  return (
                    <div key={k} className={`rounded-lg p-3 border text-center ${pass ? "bg-emerald-500/10 border-emerald-500/30" : "bg-red-500/10 border-red-500/30"}`}>
                      <div className="text-[10px] uppercase tracking-widest text-muted-foreground">{k}</div>
                      <div className={`mt-1 font-bold uppercase text-sm ${pass ? "text-emerald-400" : "text-red-400"}`}>{v}</div>
                    </div>
                  );
                })}
              </div>
              <div className="mt-4 text-xs text-muted-foreground">
                  Authentication Score : {d.authentication?.score}
              </div>
            </GlassCard>

            <GlassCard>
              <SectionHeading title="Entity Recognition" description="NER on email body" />
              <ul className="space-y-2">
                {entityList.map((e: any, i: number) => (
                  <li key={i} className="flex items-center justify-between text-sm rounded-lg glass px-3 py-2">
                    <span className="text-cyan font-mono text-xs">{e.type}</span>
                    <span>{e.value}</span>
                  </li>
                ))}
              </ul>
            </GlassCard>

            <GlassCard>
              <SectionHeading title="Reply-To Analysis" />
              <div className="rounded-lg glass p-3">
                <div className="text-xs text-muted-foreground">From</div>
                <div className="font-mono text-xs">{d.from_email}</div>
                <div className="text-xs text-muted-foreground mt-2">Reply-To</div>
                <div className="font-mono text-xs text-red-400">{d.reply_to}</div>
                <RiskBadge className="mt-3" level="critical" label={d.reply_analysis?.reason} />
              </div>
              <div className="mt-4 text-xs text-muted-foreground">Reply Match : {d.reply_analysis?.match ? "Yes" : "No"}</div>
            </GlassCard>
          </div>

          <div className="grid gap-4 lg:grid-cols-2">
            <GlassCard>
              <SectionHeading title="Suspicious Links" />
              <ul className="space-y-2">
                {d.urls.map((l: any, i: number) => (
                  <li key={i} className="flex items-center justify-between text-sm rounded-lg glass px-3 py-2">
                    <span className="font-mono text-xs truncate">{l.url}</span>
                    <RiskBadge level="critical" label={`${l.risk_score}`} />
                  </li>
                ))}
              </ul>
            </GlassCard>
            <GlassCard>
              <SectionHeading title="Suspicious Attachments" />
              <ul className="space-y-2">
                {d.attachments.map((a: any, i: number) => (
                  <li key={i} className="flex items-center justify-between text-sm rounded-lg glass px-3 py-2">
                    <span className="font-mono text-xs">{a.filename}</span>
                    <RiskBadge level="critical" label={`${a.risk_score}`} />
                  </li>
                ))}
              </ul>
            </GlassCard>
          </div>

          <GlassCard>
            <div className="flex items-center gap-2 mb-3">
              <Highlighter className="h-4 w-4 text-cyan" />
              <SectionHeading title="Highlighted Suspicious Sentences" />
            </div>
            <ul className="space-y-3">
              {d.highlighted.map((h: any, i: number) => (
                <li key={i} className="rounded-lg border-l-2 border-red-400 bg-red-500/5 p-3">
                  <div className="text-sm">"{h.text}"</div>
                  <div className="mt-1 text-[11px] uppercase tracking-widest text-red-300">
                    {h.tag}
                  </div>
                </li>
              ))}
            </ul>
          </GlassCard>

          <GlassCard>
            <div className="flex items-center gap-2 mb-3">
              <ShieldAlert className="h-4 w-4 text-cyan" />
              <SectionHeading title="Plain-English Explanation" />
            </div>
            <p className="text-sm text-muted-foreground leading-relaxed max-w-3xl">{d.aiExplanation.summary}</p>
          </GlassCard>

          <GlassCard>
            <SectionHeading title="Recommendations" />

            <ul className="space-y-2">
              {d.aiExplanation.recommendations.map((r: string, i: number) => (
              <li key={i} className="rounded-lg glass p-3 text-sm">
               • {r}
              </li>
              ))}
            </ul>
          </GlassCard>
        </motion.div>
      )}
    </AppShell>
  );
}

function Metric({ label, value, tone }: { label: string; value: string; tone: "red" | "green" | "amber" }) {
  const toneMap = {
    red: "bg-red-500/10 border-red-500/30 text-red-300",
    green: "bg-emerald-500/10 border-emerald-500/30 text-emerald-300",
    amber: "bg-amber-500/10 border-amber-500/30 text-amber-300",
  };
  return (
    <div className={`rounded-lg p-3 border text-center ${toneMap[tone]}`}>
      <div className="text-[10px] uppercase tracking-widest text-muted-foreground">{label}</div>
      <div className="mt-1 font-bold">{value}</div>
    </div>
  );
}
