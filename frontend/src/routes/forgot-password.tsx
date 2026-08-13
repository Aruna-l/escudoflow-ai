import { createFileRoute, Link } from "@tanstack/react-router";
import { motion } from "framer-motion";
import { Shield, Mail } from "lucide-react";
import { useState, type FormEvent } from "react";
import { Button } from "@/components/ui/button";
import { BrandMark } from "@/components/app-shell";
import api from "@/services/api";

export const Route = createFileRoute("/forgot-password")({
  head: () => ({
    meta: [
      { title: "Forgot Password — EscudoFlow AI" },
      { name: "description", content: "Reset your EscudoFlow AI account password." },
    ],
  }),
  component: ForgotPassword,
});

function ForgotPassword() {
  const [email, setEmail] = useState("");
  const [loading, setLoading] = useState(false);
  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setLoading(true);
    try {
      await api.post("/auth/forgot-password", { email });
      setSubmitted(true);
    } catch (err: any) {
      console.error(err);
      alert(err?.response?.data?.detail || "Something went wrong. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="relative min-h-screen grid lg:grid-cols-2 hero-bg">
      <div className="relative hidden lg:flex flex-col justify-between p-10">
        <BrandMark />
        <div className="text-xs text-muted-foreground">© EscudoFlow AI · Secure by design</div>
      </div>

      <div className="flex items-center justify-center p-6 sm:p-10">
        <motion.div
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          className="w-full max-w-md rounded-2xl glass-strong p-8 shadow-elevated"
        >
          <div className="flex flex-col items-center text-center">
            <div className="grid place-items-center h-12 w-12 rounded-xl gradient-primary glow-primary">
              <Shield className="h-6 w-6 text-white" />
            </div>
            <h1 className="mt-4 text-2xl font-bold">Reset your password</h1>
            <p className="mt-1 text-sm text-muted-foreground">
              Enter your email and we'll generate a reset link.
            </p>
          </div>

          {submitted ? (
            <div className="mt-6 rounded-lg glass border border-cyan/30 p-4 text-sm text-center">
              If that email is registered, a reset link has been generated.
              <div className="mt-2 text-xs text-muted-foreground">
                (Dev mode: check the backend server terminal for the link.)
              </div>
            </div>
          ) : (
            <form onSubmit={handleSubmit} className="mt-6 space-y-3">
              <label className="block">
                <div className="text-[11px] uppercase tracking-widest text-muted-foreground mb-1">
                  Email
                </div>
                <div className="flex items-center gap-2 rounded-lg glass px-3 h-11 border border-white/10 focus-within:border-cyan/50 transition">
                  <Mail className="h-4 w-4 text-muted-foreground" />
                  <input
                    type="email"
                    required
                    placeholder="you@company.com"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    className="bg-transparent flex-1 outline-none text-sm"
                  />
                </div>
              </label>

              <Button
                type="submit"
                disabled={loading}
                className="w-full gradient-primary text-white glow-primary h-11 mt-2"
              >
                {loading ? "Sending..." : "Send reset link"}
              </Button>
            </form>
          )}

          <div className="mt-6 text-center text-sm text-muted-foreground">
            <Link to="/login" className="text-cyan hover:underline">
              Back to sign in
            </Link>
          </div>
        </motion.div>
      </div>
    </div>
  );
}
