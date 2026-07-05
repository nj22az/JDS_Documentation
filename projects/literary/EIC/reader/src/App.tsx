import { useState } from "react";
import { Routes, Route, Navigate } from "react-router-dom";
import { useSettings } from "./hooks/useSettings";
import TopBar from "./components/TopBar";
import SettingsPanel from "./components/SettingsPanel";
import Contents from "./components/Contents";
import Reader from "./components/Reader";
import Credits from "./components/Credits";

export default function App() {
  const settings = useSettings();
  const [settingsOpen, setSettingsOpen] = useState(false);

  return (
    <>
      <TopBar onOpenSettings={() => setSettingsOpen(true)} />
      <Routes>
        <Route path="/" element={<Contents />} />
        <Route path="/read/:id" element={<Reader />} />
        <Route path="/credits" element={<Credits />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
      <SettingsPanel
        open={settingsOpen}
        onClose={() => setSettingsOpen(false)}
        settings={settings}
      />
    </>
  );
}
