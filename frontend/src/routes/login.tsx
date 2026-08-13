import {
  createFileRoute,
  Link,
  useNavigate,
} from "@tanstack/react-router";

import { motion } from "framer-motion";

import {
  Shield,
  Mail,
  Lock,
  Github,
  Eye,
  EyeOff,
} from "lucide-react";

import { Button } from "@/components/ui/button";
import { Checkbox } from "@/components/ui/checkbox";
import { BrandMark } from "@/components/app-shell";

import {
  useState,
  type FormEvent,
  type ChangeEvent,
} from "react";

import api from "@/services/api";


export const Route = createFileRoute("/login")({
  head: () => ({
    meta: [
      {
        title: "Login — EscudoFlow AI",
      },
      {
        name: "description",
        content:
          "Sign in to EscudoFlow AI to access your SOC dashboard and investigations.",
      },
      {
        property: "og:title",
        content: "Login — EscudoFlow AI",
      },
      {
        property: "og:description",
        content: "Sign in to EscudoFlow AI.",
      },
    ],
  }),

  component: Login,
});


function Login() {
  return <AuthShell mode="login" />;
}


export function AuthShell({
  mode,
}: {
  mode: "login" | "signup";
}) {

  const navigate = useNavigate();

  const [loading, setLoading] = useState(false);

  const [rememberMe, setRememberMe] = useState(false);

  const [showPassword, setShowPassword] = useState(false);

  const [showConfirmPassword, setShowConfirmPassword] = useState(false);

  const [formData, setFormData] = useState({
    full_name: "",
    organization: "",
    email: "",
    password: "",
    confirmPassword: "",
  });


  const handleChange = (
    field: string,
    value: string
  ) => {

    setFormData((prev) => ({
      ...prev,
      [field]: value,
    }));

  };


  const handleSubmit = async (
    e: FormEvent<HTMLFormElement>
  ) => {

    e.preventDefault();

    setLoading(true);


    try {

      /*
       * ==========================
       * SIGNUP
       * ==========================
       */

      if (mode === "signup") {

        // Check password confirmation
        if (
          formData.password !==
          formData.confirmPassword
        ) {

          alert("Passwords do not match");

          setLoading(false);

          return;
        }


        // Send signup request to FastAPI
        await api.post("/auth/signup", {

          full_name:
            formData.full_name,

          organization:
            formData.organization,

          email:
            formData.email,

          password:
            formData.password,

        });


        alert(
          "Account created successfully"
        );


        // Go to login page
        navigate({
          to: "/login",
        });


        return;
      }


      /*
       * ==========================
       * LOGIN
       * ==========================
       */


      const response =
        await api.post(
          "/auth/login",
          {
            email:
              formData.email,

            password:
              formData.password,
          }
        );


      /*
       * Backend response:
       *
       * {
       *   message: "Login successful",
       *   access_token: "...",
       *   token_type: "bearer",
       *   email: "...",
       *   name: "..."
       * }
       */


      const {
        access_token,
        token_type,
        email,
        name,
      } = response.data;


      /*
       * Store authentication information.
       *
       * Remember me checked:
       *     localStorage
       *
       * Remember me unchecked:
       *     sessionStorage
       */

if (rememberMe) {
  localStorage.setItem("access_token", access_token);
  localStorage.setItem("token_type", token_type);
  localStorage.setItem("user_email", email);
  localStorage.setItem("user_name", name);

  sessionStorage.removeItem("access_token");
  sessionStorage.removeItem("token_type");
  sessionStorage.removeItem("user_email");
  sessionStorage.removeItem("user_name");

} else {
  sessionStorage.setItem("access_token", access_token);
  sessionStorage.setItem("token_type", token_type);
  sessionStorage.setItem("user_email", email);
  sessionStorage.setItem("user_name", name);

  localStorage.removeItem("access_token");
  localStorage.removeItem("token_type");
  localStorage.removeItem("user_email");
  localStorage.removeItem("user_name");
}


      alert("Login successful");


      /*
       * Go to dashboard
       */

      await navigate({
        to: "/dashboard",
      });


    } catch (error: any) {

      console.error(
        "Authentication error:",
        error
      );


      /*
       * FastAPI returns errors like:
       *
       * {
       *   "detail": "Invalid credentials"
       * }
       */

      const message =
        error?.response?.data?.detail ||
        error?.response?.data?.message ||
        "Something went wrong. Please try again.";


      alert(message);


    } finally {

      setLoading(false);

    }

  };


  return (
    <div className="relative min-h-screen grid lg:grid-cols-2 hero-bg">

      {/* =========================
          LEFT SIDE
          ========================= */}

      <div className="relative hidden lg:flex flex-col justify-between p-10">

        <BrandMark />


        <div className="max-w-md">

          <div className="text-xs uppercase tracking-[0.2em] text-cyan mb-3">
            Trusted by security teams
          </div>


          <h2 className="text-3xl font-bold">
            Detect and explain phishing attacks with AI.
          </h2>


          <p className="mt-3 text-muted-foreground">
            EscudoFlow analyzes emails, URLs, and attachments in under 2 seconds with explainable reasoning your SOC can act on.
          </p>


          <div className="mt-8 flex items-center gap-3 text-xs text-muted-foreground">

            {[
              "SOC 2",
              "ISO 27001",
              "GDPR",
              "HIPAA",
            ].map((b) => (

              <span
                key={b}
                className="px-2 py-1 rounded-md glass"
              >
                {b}
              </span>

            ))}

          </div>

        </div>


        <div className="text-xs text-muted-foreground">
          © EscudoFlow AI · Secure by design
        </div>

      </div>


      {/* =========================
          RIGHT SIDE
          ========================= */}

      <div className="flex items-center justify-center p-6 sm:p-10">

        <motion.div
          initial={{
            opacity: 0,
            y: 12,
          }}
          animate={{
            opacity: 1,
            y: 0,
          }}
          className="w-full max-w-md rounded-2xl glass-strong p-8 shadow-elevated"
        >

          {/* =========================
              HEADER
              ========================= */}

          <div className="flex flex-col items-center text-center">

            <div className="grid place-items-center h-12 w-12 rounded-xl gradient-primary glow-primary">

              <Shield className="h-6 w-6 text-white" />

            </div>


            <h1 className="mt-4 text-2xl font-bold">

              {mode === "login"
                ? "Welcome back"
                : "Create your account"}

            </h1>


            <p className="mt-1 text-sm text-muted-foreground">

              {mode === "login"
                ? "Sign in to continue to EscudoFlow AI"
                : "Start protecting your organization in minutes"}

            </p>

          </div>


          {/* =========================
              FORM
              ========================= */}

          <form
            onSubmit={handleSubmit}
            className="mt-6 space-y-3"
          >

            {/* SIGNUP FIELDS */}

            {mode === "signup" && (
              <>

                <Field
                  label="Full Name"
                  placeholder="Jane Doe"
                  value={formData.full_name}
                  onChange={(e) =>
                    handleChange(
                      "full_name",
                      e.target.value
                    )
                  }
                />


                <Field
                  label="Organization"
                  placeholder="Acme Corp"
                  value={formData.organization}
                  onChange={(e) =>
                    handleChange(
                      "organization",
                      e.target.value
                    )
                  }
                />

              </>
            )}


            {/* EMAIL */}

            <Field
              label="Email"
              placeholder="you@company.com"
              icon={Mail}
              value={formData.email}
              onChange={(e) =>
                handleChange(
                  "email",
                  e.target.value
                )
              }
            />


            {/* PASSWORD */}

            <Field
              label="Password"
              placeholder="••••••••"
              type={showPassword ? "text" : "password"}
              icon={Lock}
              value={formData.password}
              onChange={(e) =>
                handleChange(
                  "password",
                  e.target.value
                )
              }
              endIcon={showPassword ? EyeOff : Eye}
              onEndIconClick={() => setShowPassword((v) => !v)}
            />


            {/* CONFIRM PASSWORD */}

            {mode === "signup" && (

              <Field
                label="Confirm Password"
                placeholder="••••••••"
                type={showConfirmPassword ? "text" : "password"}
                icon={Lock}
                value={
                  formData.confirmPassword
                }
                onChange={(e) =>
                  handleChange(
                    "confirmPassword",
                    e.target.value
                  )
                }
                endIcon={showConfirmPassword ? EyeOff : Eye}
                onEndIconClick={() => setShowConfirmPassword((v) => !v)}
              />

            )}


            {/* =========================
                REMEMBER ME
                ========================= */}

            {mode === "login" && (

              <div className="flex items-center justify-between text-xs">

                <label className="flex items-center gap-2 text-muted-foreground">

                  <Checkbox
                    className="border-white/20"
                    checked={rememberMe}
                    onCheckedChange={(checked) =>
                      setRememberMe(
                        checked === true
                      )
                    }
                  />

                  Remember me

                </label>


                <Link
                  className="text-cyan hover:underline"
                  to="/forgot-password"
                >
                  Forgot password?
                </Link>

              </div>

            )}


            {/* =========================
                SUBMIT BUTTON
                ========================= */}

            <Button
              type="submit"
              disabled={loading}
              className="w-full gradient-primary text-white glow-primary h-11 mt-2"
            >

              {loading
                ? "Please wait..."
                : mode === "login"
                ? "Sign in"
                : "Create account"}

            </Button>

          </form>


          {/* =========================
              SOCIAL LOGIN
              ========================= */}

          <div className="my-5 flex items-center gap-3 text-xs text-muted-foreground">

            <span className="h-px flex-1 bg-white/10" />

            or continue with

            <span className="h-px flex-1 bg-white/10" />

          </div>


          <div className="grid grid-cols-2 gap-2">

            <Button
              type="button"
              variant="outline"
              className="border-white/10 h-11"
              onClick={() => alert("Google sign-in is coming soon.")}
            >
              <GoogleIcon />
              Google
            </Button>


            <Button
              type="button"
              variant="outline"
              className="border-white/10 h-11"
              onClick={() => alert("GitHub sign-in is coming soon.")}
            >
              <Github className="h-4 w-4 mr-2" />
              GitHub
            </Button>

          </div>


          {/* =========================
              LOGIN / SIGNUP LINK
              ========================= */}

          <div className="mt-6 text-center text-sm text-muted-foreground">

            {mode === "login" ? (

              <>
                New to EscudoFlow?{" "}

                <Link
                  to="/signup"
                  className="text-cyan hover:underline"
                >
                  Create account
                </Link>
              </>

            ) : (

              <>
                Already have an account?{" "}

                <Link
                  to="/login"
                  className="text-cyan hover:underline"
                >
                  Sign in
                </Link>
              </>

            )}

          </div>

        </motion.div>

      </div>

    </div>
  );
}


/* =====================================================
   FIELD COMPONENT
   ===================================================== */

function Field({
  label,
  placeholder,
  type = "text",
  icon: Icon,
  endIcon: EndIcon,
  onEndIconClick,
  value,
  onChange,
}: {
  label: string;
  placeholder?: string;
  type?: string;
  icon?: any;
  endIcon?: any;
  onEndIconClick?: () => void;
  value?: string;
  onChange?: (
    e: ChangeEvent<HTMLInputElement>
  ) => void;
}) {

  return (

    <label className="block">

      <div className="text-[11px] uppercase tracking-widest text-muted-foreground mb-1">
        {label}
      </div>


      <div className="flex items-center gap-2 rounded-lg glass px-3 h-11 border border-white/10 focus-within:border-cyan/50 transition">

        {Icon && (
          <Icon className="h-4 w-4 text-muted-foreground" />
        )}


        <input
          type={type}
          placeholder={placeholder}
          value={value}
          onChange={onChange}
          className="bg-transparent flex-1 outline-none text-sm"
        />

        {EndIcon && (
          <button
            type="button"
            onClick={onEndIconClick}
            className="text-muted-foreground hover:text-white transition"
            tabIndex={-1}
          >
            <EndIcon className="h-4 w-4" />
          </button>
        )}

      </div>

    </label>

  );
}


/* =====================================================
   GOOGLE ICON
   ===================================================== */

function GoogleIcon() {

  return (

    <svg
      className="h-4 w-4 mr-2"
      viewBox="0 0 24 24"
    >

      <path
        fill="#EA4335"
        d="M12 10.8v3.6h5.1c-.2 1.4-1.6 4-5.1 4-3.1 0-5.6-2.6-5.6-5.7S8.9 7 12 7c1.7 0 2.9.7 3.6 1.3l2.5-2.4C16.5 4.4 14.5 3.5 12 3.5 6.9 3.5 3 7.4 3 12.5s3.9 9 9 9c5.2 0 8.7-3.7 8.7-8.8 0-.6-.1-1.1-.2-1.6H12z"
      />

    </svg>

  );
}
