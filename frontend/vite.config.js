import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    host: true,        // listen on 0.0.0.0 so the Docker port mapping works
    port: 3000,
    strictPort: true,
    watch: { usePolling: true }, // reliable hot reload on Windows bind mounts
  },
});
