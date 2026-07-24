import { createFileRoute, Link } from "@tanstack/react-router";
import { motion } from "framer-motion";
import { Shield, Mail, Lock, Github } from "lucide-react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Checkbox } from "@/components/ui/checkbox";
import { BrandMark } from "@/components/app-shell";

export const Route = createFileRoute("/login")({
  head: () => ({
    meta: [
      { title: "Login — EscudoFlow AI" },
      { name: "description", content: "Sign in to EscudoFlow AI to access your SOC dashboard and investigations." },
      { property: "og:title", content: "Login — EscudoFlow AI" },
      { property: "og:description", content: "Sign in to EscudoFlow AI." },
    ],
  }),
  component: Login,
});

function Login() {
  return <AuthShell mode="login" />;
}

export function AuthShell({ mode }: { mode: "login" | "signup" }) {
  return (
    <div className="relative min-h-screen grid lg:grid-cols-2 hero-bg">
      <div className="relative hidden lg:flex flex-col justify-between p-10">
        <BrandMark />
        <div className="max-w-md">
          <div className="text-xs uppercase tracking-[0.2em] text-cyan mb-3">Trusted by security teams</div>
          <h2 className="text-3xl font-bold">Detect and explain phishing attacks with AI.</h2>
          <p className="mt-3 text-muted-foreground">EscudoFlow analyzes emails, URLs, and attachments in under 2 seconds with explainable reasoning your SOC can act on.</p>
          <div className="mt-8 flex items-center gap-3 text-xs text-muted-foreground">
            {["SOC 2","ISO 27001","GDPR","HIPAA"].map((b) => (<span key={b} className="px-2 py-1 rounded-md glass">{b}</span>))}
          </div>
        </div>
        <div className="text-xs text-muted-foreground">© EscudoFlow AI · Secure by design</div>
      </div>
      <div className="flex items-center justify-center p-6 sm:p-10">
        <motion.div
          initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }}
          className="w-full max-w-md rounded-2xl glass-strong p-8 shadow-elevated"
        >
          <div className="flex flex-col items-center text-center">
            <div className="grid place-items-center h-12 w-12 rounded-xl gradient-primary glow-primary">
              <Shield className="h-6 w-6 text-white" />
            </div>
            <h1 className="mt-4 text-2xl font-bold">{mode === "login" ? "Welcome back" : "Create your account"}</h1>
            <p className="mt-1 text-sm text-muted-foreground">{mode === "login" ? "Sign in to continue to EscudoFlow AI" : "Start protecting your organization in minutes"}</p>
          </div>

          <form className="mt-6 space-y-3">
            {mode === "signup" && (
              <>
                <Field label="Full Name" placeholder="Jane Doe" />
                <Field label="Organization" placeholder="Acme Corp" />
              </>
            )}
            <Field label="Email" placeholder="you@company.com" icon={Mail} />
            <Field label="Password" placeholder="••••••••" type="password" icon={Lock} />
            {mode === "signup" && <Field label="Confirm Password" placeholder="••••••••" type="password" icon={Lock} />}

            {mode === "login" && (
              <div className="flex items-center justify-between text-xs">
                <label className="flex items-center gap-2 text-muted-foreground">
                  <Checkbox className="border-white/20" /> Remember me
                </label>
                <a className="text-cyan hover:underline" href="#">Forgot password?</a>
              </div>
            )}

            <Button type="button" className="w-full gradient-primary text-white glow-primary h-11 mt-2">
              {mode === "login" ? "Sign in" : "Create account"}
            </Button>
          </form>

          <div className="my-5 flex items-center gap-3 text-xs text-muted-foreground">
            <span className="h-px flex-1 bg-white/10" /> or continue with <span className="h-px flex-1 bg-white/10" />
          </div>
          <div className="grid grid-cols-2 gap-2">
            <Button variant="outline" className="border-white/10 h-11"><GoogleIcon /> Google</Button>
            <Button variant="outline" className="border-white/10 h-11"><Github className="h-4 w-4 mr-2" /> GitHub</Button>
          </div>

          <div className="mt-6 text-center text-sm text-muted-foreground">
            {mode === "login" ? (<>New to EscudoFlow? <Link to="/signup" className="text-cyan hover:underline">Create account</Link></>) :
              (<>Already have an account? <Link to="/login" className="text-cyan hover:underline">Sign in</Link></>)}
          </div>
        </motion.div>
      </div>
    </div>
  );
}

function Field({ label, placeholder, type = "text", icon: Icon }: { label: string; placeholder?: string; type?: string; icon?: any }) {
  return (
    <label className="block">
      <div className="text-[11px] uppercase tracking-widest text-muted-foreground mb-1">{label}</div>
      <div className="flex items-center gap-2 rounded-lg glass px-3 h-11 border border-white/10 focus-within:border-cyan/50 transition">
        {Icon && <Icon className="h-4 w-4 text-muted-foreground" />}
        <input type={type} placeholder={placeholder} className="bg-transparent flex-1 outline-none text-sm" />
      </div>
    </label>
  );
}

function GoogleIcon() {
  return (
    <svg className="h-4 w-4 mr-2" viewBox="0 0 24 24">
      <path fill="#EA4335" d="M12 10.8v3.6h5.1c-.2 1.4-1.6 4-5.1 4-3.1 0-5.6-2.6-5.6-5.7S8.9 7 12 7c1.7 0 2.9.7 3.6 1.3l2.5-2.4C16.5 4.4 14.5 3.5 12 3.5 6.9 3.5 3 7.4 3 12.5s3.9 9 9 9c5.2 0 8.7-3.7 8.7-8.8 0-.6-.1-1.1-.2-1.6H12z"/>
    </svg>
  );
}
