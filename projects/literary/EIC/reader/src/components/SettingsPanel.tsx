import { Link } from "react-router-dom";
import type { Theme } from "../hooks/useSettings";
import { Sun, Moon, Auto } from "./icons";

interface Settings {
  theme: Theme;
  setTheme: (t: Theme) => void;
  size: number;
  setSize: (s: any) => void;
}

const THEMES: { id: Theme; label: string; icon: JSX.Element }[] = [
  { id: "auto", label: "Auto", icon: <Auto size={17} /> },
  { id: "light", label: "Light", icon: <Sun size={17} /> },
  { id: "dark", label: "Dark", icon: <Moon size={17} /> },
];

export default function SettingsPanel({
  open,
  onClose,
  settings,
}: {
  open: boolean;
  onClose: () => void;
  settings: Settings;
}) {
  if (!open) return null;
  const { theme, setTheme, size, setSize } = settings;

  return (
    <div className="sheet-backdrop" onClick={onClose}>
      <div className="settings-pop" onClick={(e) => e.stopPropagation()} role="dialog" aria-label="Reading settings">
        <div className="set-row">
          <span className="set-label">Text Size</span>
          <div className="size-stepper">
            <button aria-label="Smaller text" disabled={size <= 0} onClick={() => setSize(size - 1)}>
              <span className="aa-min">A</span>
            </button>
            <div className="size-dots">
              {[0, 1, 2, 3, 4].map((i) => (
                <span key={i} className={"size-dot" + (i <= size ? " on" : "")} />
              ))}
            </div>
            <button aria-label="Larger text" disabled={size >= 4} onClick={() => setSize(size + 1)}>
              <span className="aa-max">A</span>
            </button>
          </div>
        </div>

        <div className="set-divider" />

        <div className="set-row">
          <span className="set-label">Appearance</span>
          <div className="segmented">
            {THEMES.map((t) => (
              <button
                key={t.id}
                className={"seg" + (theme === t.id ? " active" : "")}
                onClick={() => setTheme(t.id)}
              >
                {t.icon}
                <span>{t.label}</span>
              </button>
            ))}
          </div>
        </div>

        <div className="set-divider" />

        <Link to="/credits" className="set-link" onClick={onClose}>
          Visual Credits
        </Link>
      </div>
    </div>
  );
}
