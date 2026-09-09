import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// Build into aphanis/dashboard_static so the Python server can ship it.
export default defineConfig({
  plugins: [react()],
  build: {
    outDir: "../aphanis/dashboard_static",
    emptyOutDir: true,
  },
});
