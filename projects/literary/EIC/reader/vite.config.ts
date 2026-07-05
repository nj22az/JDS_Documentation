import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// Relative base so the built app works when served from any sub-path
// (e.g. https://nj22az.github.io/the-front-row-seat/). Combined with
// HashRouter, deep links and refreshes work on GitHub Pages with no server.
export default defineConfig({
  base: "./",
  plugins: [react()],
  build: { outDir: "dist", assetsDir: "app", sourcemap: false },
});
