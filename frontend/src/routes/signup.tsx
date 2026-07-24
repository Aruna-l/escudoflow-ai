import { createFileRoute } from "@tanstack/react-router";
import { AuthShell } from "./login";

export const Route = createFileRoute("/signup")({
  head: () => ({
    meta: [
      { title: "Sign up — EscudoFlow AI" },
      { name: "description", content: "Create your EscudoFlow AI workspace and start detecting phishing in minutes." },
      { property: "og:title", content: "Sign up — EscudoFlow AI" },
      { property: "og:description", content: "Create your EscudoFlow AI account." },
    ],
  }),
  component: () => <AuthShell mode="signup" />,
});
