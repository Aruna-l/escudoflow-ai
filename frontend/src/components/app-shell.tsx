import { Link, useRouterState } from "@tanstack/react-router";
import { motion } from "framer-motion";
import {
  Shield,
  LayoutDashboard,
  Link2,
  Mail,
  Eye,
  Paperclip,
  Globe2,
  FileText,
  Settings as SettingsIcon,
  Home,
  Bell,
  Search,
  Menu,
  X,
  LogOut,
} from "lucide-react";
import { useEffect, useState, type ReactNode } from "react";
import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

const NAV = [
  { to: "/", label: "Home", icon: Home },
  { to: "/dashboard", label: "Dashboard", icon: LayoutDashboard },
  { to: "/url-intelligence", label: "URL Intelligence", icon: Link2 },
  { to: "/email-intelligence", label: "Email Intelligence", icon: Mail },
  { to: "/visual-intelligence", label: "Visual Intelligence", icon: Eye },
  { to: "/attachment-intelligence", label: "Attachment Intelligence", icon: Paperclip },
  { to: "/threat-intelligence", label: "Threat Intelligence", icon: Globe2 },
  { to: "/reports", label: "Reports", icon: FileText },
  { to: "/settings", label: "Settings", icon: SettingsIcon },
] as const;

export function BrandMark({ className }: { className?: string }) {
  return (
    <Link to="/" className={cn("flex items-center gap-2 group", className)}>
      <span className="relative grid place-items-center h-9 w-9 rounded-xl gradient-primary glow-primary">
        <Shield className="h-5 w-5 text-white" strokeWidth={2.4} />
        <span className="absolute inset-0 rounded-xl pulse-ring" />
      </span>
      <span className="flex flex-col leading-none">
        <span className="font-display text-[15px] font-bold tracking-tight">
          EscudoFlow <span className="gradient-text">AI</span>
        </span>
        <span className="text-[10px] uppercase tracking-[0.18em] text-muted-foreground">
          Threat Intelligence
        </span>
      </span>
    </Link>
  );
}

export function TopNav() {
  const pathname = useRouterState({ select: (s) => s.location.pathname });
  const [open, setOpen] = useState(false);
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [userName, setUserName] = useState("");

  useEffect(() => {
    const token =
      localStorage.getItem("access_token") ||
      sessionStorage.getItem("access_token");

    const name =
      localStorage.getItem("user_name") ||
      sessionStorage.getItem("user_name") ||
      "";

    setIsLoggedIn(!!token);
    setUserName(name);
  }, [pathname]);

  const handleLogout = () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("token_type");
    localStorage.removeItem("user_email");
    localStorage.removeItem("user_name");

    sessionStorage.removeItem("access_token");
    sessionStorage.removeItem("token_type");
    sessionStorage.removeItem("user_email");
    sessionStorage.removeItem("user_name");

    window.location.href = "/login";
  };

  return (
    <header className="sticky top-0 z-40 w-full">
      <div className="glass-strong border-b border-white/5">
        <div className="mx-auto flex h-16 max-w-[1400px] items-center gap-4 px-4 sm:px-6">
          <BrandMark />
          <nav className="hidden lg:flex items-center gap-1 ml-4">
            {NAV.slice(0, 8).map((item) => {
              const active = pathname === item.to || (item.to !== "/" && pathname.startsWith(item.to));
              return (
                <Link
                  key={item.to}
                  to={item.to}
                  className={cn(
                    "relative px-3 py-2 text-sm rounded-lg transition-colors",
                    active ? "text-white" : "text-muted-foreground hover:text-white",
                  )}
                >
                  {active && (
                    <motion.span
                      layoutId="nav-active"
                      className="absolute inset-0 rounded-lg bg-white/5 border border-white/10"
                      transition={{ type: "spring", stiffness: 380, damping: 30 }}
                    />
                  )}
                  <span className="relative">{item.label}</span>
                </Link>
              );
            })}
          </nav>
          <div className="ml-auto flex items-center gap-2">
            <div className="hidden md:flex items-center gap-2 rounded-lg glass px-3 py-1.5 w-72">
              <Search className="h-4 w-4 text-muted-foreground" />
              <input
                className="bg-transparent text-sm outline-none flex-1 placeholder:text-muted-foreground"
                placeholder="Search IOCs, URLs, emails…"
              />
              <kbd className="text-[10px] text-muted-foreground border border-white/10 rounded px-1.5 py-0.5">⌘K</kbd>
            </div>
            <Button variant="ghost" size="icon" className="relative">
              <Bell className="h-4 w-4" />
              <span className="absolute top-2 right-2 h-1.5 w-1.5 rounded-full bg-destructive" />
            </Button>
            {isLoggedIn ? (
  <>
    <span className="hidden sm:inline-flex text-sm text-muted-foreground px-3 py-1.5">
      {userName || "Account"}
    </span>

    <button
      type="button"
      onClick={handleLogout}
      className="hidden sm:inline-flex items-center gap-2 text-sm text-muted-foreground hover:text-white px-3 py-1.5 transition"
    >
      <LogOut className="h-4 w-4" />
      Logout
    </button>
  </>
) : (
  <>
    <Link
      to="/login"
      className="hidden sm:inline-flex text-sm text-muted-foreground hover:text-white px-3 py-1.5"
    >
      Login
    </Link>

    <Link
      to="/signup"
      className="hidden sm:inline-flex text-sm text-white gradient-primary px-3.5 py-1.5 rounded-lg glow-primary hover:opacity-90 transition"
    >
      Sign Up
    </Link>
  </>
)}
            <Button variant="ghost" size="icon" className="lg:hidden" onClick={() => setOpen(true)}>
              <Menu className="h-5 w-5" />
            </Button>
          </div>
        </div>
      </div>

      {open && (
        <div className="fixed inset-0 z-50 lg:hidden">
          <div className="absolute inset-0 bg-background/80 backdrop-blur-md" onClick={() => setOpen(false)} />
          <div className="absolute right-0 top-0 h-full w-80 glass-strong border-l border-white/10 p-5">
            <div className="flex items-center justify-between">
              <BrandMark />
              <Button variant="ghost" size="icon" onClick={() => setOpen(false)}><X className="h-5 w-5" /></Button>
            </div>
            <div className="mt-6 flex flex-col gap-1">
              {NAV.map((it) => (
                <Link
                  key={it.to}
                  to={it.to}
                  onClick={() => setOpen(false)}
                  className="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm hover:bg-white/5"
                >
                  <it.icon className="h-4 w-4" /> {it.label}
                </Link>
              ))}
              <div className="mt-3 flex flex-col gap-2">
  {isLoggedIn ? (
    <>
      <div className="text-center py-2 text-sm text-muted-foreground">
        {userName || "Account"}
      </div>

      <button
        type="button"
        onClick={() => {
          setOpen(false);
          handleLogout();
        }}
        className="flex items-center justify-center gap-2 py-2 rounded-lg border border-white/10"
      >
        <LogOut className="h-4 w-4" />
        Logout
      </button>
    </>
  ) : (
    <>
      <Link
        to="/login"
        onClick={() => setOpen(false)}
        className="text-center py-2 rounded-lg border border-white/10"
      >
        Login
      </Link>

      <Link
        to="/signup"
        onClick={() => setOpen(false)}
        className="text-center py-2 rounded-lg gradient-primary text-white"
      >
        Sign Up
      </Link>
    </>
  )}
</div>
            </div>
          </div>
        </div>
      )}
    </header>
  );
}

export function SideRail() {
  const pathname = useRouterState({ select: (s) => s.location.pathname });
  return (
    <aside className="hidden xl:flex sticky top-16 h-[calc(100vh-4rem)] w-16 flex-col items-center gap-1 py-4 border-r border-white/5">
      {NAV.map((it) => {
        const active = pathname === it.to || (it.to !== "/" && pathname.startsWith(it.to));
        return (
          <Link
            key={it.to}
            to={it.to}
            title={it.label}
            className={cn(
              "grid place-items-center h-10 w-10 rounded-xl transition-all",
              active
                ? "gradient-primary text-white glow-primary"
                : "text-muted-foreground hover:text-white hover:bg-white/5",
            )}
          >
            <it.icon className="h-4 w-4" />
          </Link>
        );
      })}
    </aside>
  );
}

export function Footer() {
  return (
    <footer className="mt-24 border-t border-white/5">
      <div className="mx-auto max-w-[1400px] px-6 py-10 grid gap-8 md:grid-cols-4">
        <div>
          <BrandMark />
          <p className="mt-3 text-sm text-muted-foreground max-w-xs">
            AI-powered phishing detection, brand-clone recognition, and explainable threat intelligence for modern security teams.
          </p>
        </div>
        <div>
          <h4 className="text-sm font-semibold mb-3">Platform</h4>
          <ul className="space-y-2 text-sm text-muted-foreground">
            <li><Link to="/dashboard">Dashboard</Link></li>
            <li><Link to="/url-intelligence">URL Intelligence</Link></li>
            <li><Link to="/email-intelligence">Email Intelligence</Link></li>
            <li><Link to="/threat-intelligence">Threat Intelligence</Link></li>
          </ul>
        </div>
        <div>
          <h4 className="text-sm font-semibold mb-3">Company</h4>
          <ul className="space-y-2 text-sm text-muted-foreground">
            <li>About</li><li>Security</li><li>Careers</li><li>Contact</li>
          </ul>
        </div>
        <div>
          <h4 className="text-sm font-semibold mb-3">Compliance</h4>
          <div className="flex flex-wrap gap-2">
            {["SOC 2","ISO 27001","GDPR","HIPAA"].map((b) => (
              <span key={b} className="text-[11px] px-2 py-1 rounded-md glass">{b}</span>
            ))}
          </div>
        </div>
      </div>
      <div className="border-t border-white/5 py-4 text-center text-xs text-muted-foreground">
        © {new Date().getFullYear()} EscudoFlow AI · All rights reserved
      </div>
    </footer>
  );
}

export function AppShell({ children, sidebar = true }: { children: ReactNode; sidebar?: boolean }) {
  return (
    <div className="relative min-h-screen">
      <TopNav />
      <div className="mx-auto max-w-[1400px] flex">
        {sidebar && <SideRail />}
        <main className="relative flex-1 min-w-0 px-4 sm:px-6 py-8">{children}</main>
      </div>
      <Footer />
    </div>
  );
}

export function PageHeader({
  eyebrow, title, description, actions,
}: { eyebrow?: string; title: string; description?: string; actions?: ReactNode }) {
  return (
    <div className="flex flex-col md:flex-row md:items-end md:justify-between gap-4 mb-8">
      <div className="min-w-0">
        {eyebrow && (
          <div className="text-xs uppercase tracking-[0.2em] text-cyan mb-2">{eyebrow}</div>
        )}
        <h1 className="text-3xl md:text-4xl font-bold tracking-tight">{title}</h1>
        {description && <p className="mt-2 text-muted-foreground max-w-2xl">{description}</p>}
      </div>
      {actions && <div className="flex shrink-0 items-center gap-2">{actions}</div>}
    </div>
  );
}

export { Input };
