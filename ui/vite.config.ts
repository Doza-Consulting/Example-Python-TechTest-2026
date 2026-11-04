import { defineConfig } from "vitest/config";
import react from "@vitejs/plugin-react";

// In dev, /api/* is proxied to the local API (port 3000) with the prefix
// stripped. When deployed, CloudFront does the same routing (see /terraform),
// so the UI always calls relative /api/... URLs and needs no CORS.
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      "/api": {
        target: "http://localhost:3000",
        rewrite: (path) => path.replace(/^\/api/, ""),
      },
    },
  },
  test: {
    environment: "jsdom",
    setupFiles: ["./src/test/setup.ts"],
    globals: true,
  },
});
