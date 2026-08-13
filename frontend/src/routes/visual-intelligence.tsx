import { createFileRoute } from "@tanstack/react-router";
import { useState, useRef } from "react";
import { motion } from "framer-motion";
import { Camera, Eye } from "lucide-react";
import { AppShell, PageHeader } from "@/components/app-shell";
import { GlassCard, RiskBadge, SectionHeading } from "@/components/cyber-ui";
import { Button } from "@/components/ui/button";
import axios from "axios";
import { getSessionId } from "@/lib/session-id";
import { usePersistedState } from "@/lib/persisted-state";


export const Route = createFileRoute("/visual-intelligence")({
  head: () => ({
    meta: [
      { title: "Visual Intelligence — EscudoFlow AI" },
      { name: "description", content: "Computer-vision analysis of login pages to detect brand cloning and fake credential forms." },
      { property: "og:title", content: "Visual Intelligence — EscudoFlow AI" },
      { property: "og:description", content: "Detect fake login pages with CLIP-based visual similarity." },
    ],
  }),
  component: VisualIntel,
});

const shot = (label: string, tone: "clone" | "brand") =>
  `data:image/svg+xml;utf8,${encodeURIComponent(
    `<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 600 380'>
      <defs><linearGradient id='g' x1='0' x2='1' y1='0' y2='1'>
        <stop offset='0' stop-color='${tone === "brand" ? "#0f172a" : "#1a0f0f"}'/>
        <stop offset='1' stop-color='${tone === "brand" ? "#1e293b" : "#2a1010"}'/>
      </linearGradient></defs>
      <rect width='600' height='380' fill='url(#g)'/>
      <rect x='40' y='36' width='140' height='18' rx='4' fill='${tone === "brand" ? "#2563EB" : "#EF4444"}'/>
      <rect x='200' y='36' width='60' height='14' rx='3' fill='#334155'/>
      <rect x='280' y='36' width='60' height='14' rx='3' fill='#334155'/>
      <rect x='170' y='120' width='260' height='34' rx='6' fill='#0f172a' stroke='#334155'/>
      <rect x='170' y='170' width='260' height='34' rx='6' fill='#0f172a' stroke='#334155'/>
      <rect x='170' y='222' width='260' height='38' rx='6' fill='${tone === "brand" ? "#2563EB" : "#EF4444"}'/>
      <text x='300' y='247' font-family='Inter' font-size='14' fill='#fff' text-anchor='middle'>Sign in</text>
      <text x='300' y='320' font-family='Inter' font-size='11' fill='#64748b' text-anchor='middle'>${label}</text>
    </svg>`
  )}`;

function VisualIntel() {
  const [url, setUrl, clearVisualUrl] = usePersistedState("escudoflow_visual_url", "");
  const [captured, setCaptured, clearCaptured] = usePersistedState("escudoflow_visual_captured", false);
  const [loading, setLoading] = useState(false);
  const [analysis, setAnalysis, clearVisualAnalysis] = usePersistedState<any>("escudoflow_visual_analysis", null);

  const [selectedFile, setSelectedFile] = useState<File | null>(null);

  const fileInputRef = useRef<HTMLInputElement>(null);

  const d = analysis ?? {};

  const analyzeVisual = async () => {
    console.log(selectedFile);
    if (!selectedFile) return;

    const formData = new FormData();

    formData.append("file", selectedFile);

    formData.append("url", url);

    setLoading(true);

    try {
      const response = await axios.post(
  "http://127.0.0.1:8000/visual/analyze",
  formData,
  {
    headers: {
      "Content-Type": "multipart/form-data",
      "X-Session-Id": getSessionId(),
    },
  }
);

      console.log(response.data);

      setAnalysis(response.data);

      setCaptured(true);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <AppShell>
      <PageHeader
        eyebrow="Visual Intelligence"
        title="Brand-Clone Detection"
        description="Capture a live screenshot of any URL and compare it to 400+ known brand login pages with CLIP embeddings."
      />

      <GlassCard className="mb-6">
        <div className="flex flex-col md:flex-row gap-3">
          <div className="flex-1 flex items-center gap-2 rounded-xl glass px-4 h-14">
            <Eye className="h-4 w-4 text-cyan" />
            <input
              className="bg-transparent flex-1 outline-none text-sm font-mono"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
            />
          </div>

          {/* Hidden file input now lives as a real sibling in the JSX tree,
              so fileInputRef actually attaches to a mounted DOM node. */}
          <input
            ref={fileInputRef}
            type="file"
            accept="image/*"
            hidden
            onChange={(e) => {
              if (e.target.files?.length) {
                setSelectedFile(e.target.files[0]);
              }
            }}
          />

          <Button
            onClick={() => {
              if (selectedFile) {
                analyzeVisual();
              } else {
                fileInputRef.current?.click();
              }
            }}
            className="gradient-primary text-white glow-primary h-14 px-6"
          >
            <Camera className="h-4 w-4 mr-2" /> {loading ? "Analyzing..." : "Capture Screenshot"}
          </Button>
        </div>
      </GlassCard>

      {captured && (
        <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} className="space-y-6">
          <div className="grid gap-4 md:grid-cols-2">
            <GlassCard>
              <SectionHeading title="Captured Website" action={<RiskBadge level="critical" label="Fake login" />} />
              <div className="rounded-xl overflow-hidden border border-red-500/30 relative">
                <img src={shot("Suspicious clone", "clone")} alt="Suspicious page" className="w-full" />
                <div className="absolute inset-0 pointer-events-none">
                  <div className="absolute left-0 right-0 h-8 bg-gradient-to-b from-red-500/30 to-transparent scan-line" />
                </div>
              </div>
              <div className="text-xs font-mono text-muted-foreground mt-2 truncate">{url}</div>
            </GlassCard>
            <GlassCard>
              <SectionHeading
                title={`Reference: ${d.brand?.matchedBrand ?? "Unknown"}`}
                action={<RiskBadge level="safe" label="Verified" />}
              />
              <div className="rounded-xl overflow-hidden border border-emerald-500/30">
                <img src={shot("Legitimate brand", "brand")} alt="Brand reference" className="w-full" />
              </div>
              <div className="text-xs font-mono text-muted-foreground mt-2 truncate">{d.clone?.referenceMatched}</div>
            </GlassCard>
          </div>

          <div className="grid gap-4 md:grid-cols-4">
            <SimilarityCard
              label="Visual Similarity"
              value={Math.round((d.similarity?.visualSimilarity ?? 0) * 100)}
            />
            <SimilarityCard label="Logo Match" value={Math.round(d.logo?.confidence ?? 0)} />
            <SimilarityCard
              label="Color Similarity"
              value={Math.round((d.similarity?.colorSimilarity ?? 0) * 100)}
            />
            <SimilarityCard
              label="Layout Similarity"
              value={Math.round((d.similarity?.layoutSimilarity ?? 0) * 100)}
            />
          </div>

          <GlassCard>
            <SectionHeading title="Computer Vision Explanation" />
            <p className="text-sm text-muted-foreground max-w-3xl leading-relaxed">{d.aiExplanation?.summary}</p>
            <div className="mt-4 flex flex-wrap gap-2 text-xs">
              {[
                `CLIP: ${d.similarity?.clipSimilarity}`,
                `SSIM: ${d.similarity?.ssim}`,
                `Hash: ${d.similarity?.perceptualHash}`,
                `Logo: ${d.logo?.confidence}%`,
              ].map((t) => (
                <span key={t} className="px-2 py-1 rounded-md glass border border-white/10 font-mono">
                  {t}
                </span>
              ))}
            </div>
          </GlassCard>
        </motion.div>
      )}
    </AppShell>
  );
}

function SimilarityCard({ label, value }: { label: string; value: number }) {
  return (
    <GlassCard>
      <div className="text-xs uppercase tracking-widest text-muted-foreground">{label}</div>
      <div className="mt-2 text-3xl font-bold gradient-text">{value}%</div>
      <div className="mt-3 h-2 rounded-full bg-white/5 overflow-hidden">
        <motion.div
          initial={{ width: 0 }}
          animate={{ width: `${value}%` }}
          transition={{ duration: 1 }}
          className="h-full gradient-primary"
        />
      </div>
    </GlassCard>
  );
}
