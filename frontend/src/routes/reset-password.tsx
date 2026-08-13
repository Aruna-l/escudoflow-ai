import { createFileRoute, Link, useNavigate, useSearch } from "@tanstack/react-router";
import { motion } from "framer-motion";
import { Shield, Lock, Eye, EyeOff } from "lucide-react";
import { useState, type FormEvent } from "react";
import { Button } from "@/components/ui/button";
import { BrandMark } from "@/components/app-shell";
import api from "@/services/api";

type ResetSearch = { token?: string };

export const Route = createFileRoute("/reset-password")({
  validateSearch: (search: Record<string, unknown>): ResetSearch => ({
    token: typeof search.token === "string" ? search.token : undefined,
  }),
  head: () => ({
    meta: [
      { title: "Reset Password — EscudoFlow AI" },
      { name: "description", content: "Set a new password for your EscudoFlow AI account." },
    ],
  }),
  component: ResetPassword,
});

function ResetPassword() {
  const navigate = useNavigate();
  const { token } = useSearch({ from: "/reset-password" });

  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    if (!token) {
      alert("Missing or invalid reset link.");
      return;
    }

    if (newPassword !== confirmPassword) {
      alert("Passwords do not match");
      return;
    }

    setLoading(true);
    try {
      await api.post("/auth/reset-password", { token, new_password: newPassword });
      alert("Password has been reset. Please sign in.");
      navigate({ to: "/login" });
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
            <h1 className="mt-4 text-2xl font-bold">Set a new password</h1>
            <p className="mt-1 text-sm text-muted-foreground">
              {token ? "Choose a new password below." : "This reset link is missing a token."}
            </p>
          </div>

          {token && (
            <form onSubmit={handleSubmit} className="mt-6 space-y-3">
              <label className="block">
                <div className="text-[11px] uppercase tracking-widest text-muted-foreground mb-1">
                  New password
                </div>
                <div className="flex items-center gap-2 rounded-lg glass px-3 h-11 border border-white/10 focus-within:border-cyan/50 transition">
                  <Lock className="h-4 w-4 text-muted-foreground" />
                  <input
                    type={showPassword ? "text" : "password"}
                    required
                    placeholder="••••••••"
                    value={newPassword}
                    onChange={(e) => setNewPassword(e.target.value)}
                    className="bg-transparent flex-1 outline-none text-sm"
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword((v) => !v)}
                    className="text-muted-foreground hover:text-white transition"
                    tabIndex={-1}
                  >
                    {showPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                  </button>
                </div>
              </label>

              <label className="block">
                <div className="text-[11px] uppercase tracking-widest text-muted-foreground mb-1">
                  Confirm new password
                </div>
                <div className="flex items-center gap-2 rounded-lg glass px-3 h-11 border border-white/10 focus-within:border-cyan/50 transition">
                  <Lock className="h-4 w-4 text-muted-foreground" />
                  <input
                    type={showPassword ? "text" : "password"}
                    required
                    placeholder="••••••••"
                    value={confirmPassword}
                    onChange={(e) => setConfirmPassword(e.target.value)}
                    className="bg-transparent flex-1 outline-none text-sm"
                  />
                </div>
              </label>

              <Button
                type="submit"
                disabled={loading}
                className="w-full gradient-primary text-white glow-primary h-11 mt-2"
              >
                {loading ? "Resetting..." : "Reset password"}
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
