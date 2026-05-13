import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./app/**/*.{ts,tsx}", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        ink: "#161616",
        paper: "#f8f7f3",
        civic: "#1b6f68",
        signal: "#d7a21f",
        line: "#d7d3c8"
      }
    }
  },
  plugins: []
};

export default config;

