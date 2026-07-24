import { useEffect, useRef, useState } from "react";

/** Animated counter that eases from 0 → target when it enters view. */
export function useAnimatedNumber(target: number, duration = 1400) {
  const [value, setValue] = useState(0);
  const ref = useRef<HTMLSpanElement | null>(null);
  const started = useRef(false);

  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    const io = new IntersectionObserver((entries) => {
      entries.forEach((e) => {
        if (e.isIntersecting && !started.current) {
          started.current = true;
          const start = performance.now();
          const tick = (t: number) => {
            const p = Math.min(1, (t - start) / duration);
            const eased = 1 - Math.pow(1 - p, 3);
            setValue(target * eased);
            if (p < 1) requestAnimationFrame(tick);
          };
          requestAnimationFrame(tick);
        }
      });
    }, { threshold: 0.2 });
    io.observe(el);
    return () => io.disconnect();
  }, [target, duration]);

  return { ref, value };
}

export function AnimatedNumber({ value, decimals = 0, suffix = "" }: { value: number; decimals?: number; suffix?: string }) {
  const { ref, value: v } = useAnimatedNumber(value);
  const formatted = v >= 1000
    ? Math.floor(v).toLocaleString()
    : v.toFixed(decimals);
  return <span ref={ref}>{formatted}{suffix}</span>;
}
