import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Viche",
  description: "API-first civic deliberation platform"
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="uk">
      <body>{children}</body>
    </html>
  );
}

