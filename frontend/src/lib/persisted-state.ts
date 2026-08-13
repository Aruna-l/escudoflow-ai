import { useEffect, useState } from "react";

/**
 * Like useState, but backed by sessionStorage under `key`. Survives
 * navigating away and back within the same tab; cleared automatically
 * when the tab closes, or manually via the returned `clear()` function.
 */
export function usePersistedState<T>(key: string, initial: T) {
  const [value, setValue] = useState<T>(() => {
    try {
      const raw = sessionStorage.getItem(key);
      return raw !== null ? (JSON.parse(raw) as T) : initial;
    } catch {
      return initial;
    }
  });

  useEffect(() => {
    try {
      sessionStorage.setItem(key, JSON.stringify(value));
    } catch {
      // storage full or unavailable — fail silently, in-memory state still works
    }
  }, [key, value]);

  const clear = () => {
    sessionStorage.removeItem(key);
    setValue(initial);
  };

  return [value, setValue, clear] as const;
}