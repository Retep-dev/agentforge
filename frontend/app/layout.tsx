import "./globals.css";
export const metadata = { title: "AgentForge", description: "A 90-day autonomous AI engineering project" };
export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return <html lang="en"><body>{children}</body></html>;
}
