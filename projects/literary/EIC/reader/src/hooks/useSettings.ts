import { useCallback, useEffect, useState } from "react";

export type Theme = "auto" | "light" | "dark";
export type TextSize = 0 | 1 | 2 | 3 | 4;

const THEME_KEY = "frs-theme";
const SIZE_KEY = "frs-size";

function read<T>(key: string, fallback: T): T {
  try {
    const v = localStorage.getItem(key);
    return v === null ? fallback : (JSON.parse(v) as T);
  } catch {
    return fallback;
  }
}

export function useSettings() {
  const [theme, setThemeState] = useState<Theme>(() => read<Theme>(THEME_KEY, "auto"));
  const [size, setSizeState] = useState<TextSize>(() => read<TextSize>(SIZE_KEY, 2));

  useEffect(() => {
    const root = document.documentElement;
    root.dataset.theme = theme;
    root.dataset.size = String(size);
  }, [theme, size]);

  const setTheme = useCallback((t: Theme) => {
    setThemeState(t);
    try { localStorage.setItem(THEME_KEY, JSON.stringify(t)); } catch { /* ignore */ }
  }, []);

  const setSize = useCallback((s: TextSize) => {
    const clamped = Math.max(0, Math.min(4, s)) as TextSize;
    setSizeState(clamped);
    try { localStorage.setItem(SIZE_KEY, JSON.stringify(clamped)); } catch { /* ignore */ }
  }, []);

  return { theme, setTheme, size, setSize };
}
