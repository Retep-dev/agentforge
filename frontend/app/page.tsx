export default async function Home() {
  let api = "unavailable";
  try {
    const response = await fetch(`${process.env.API_URL ?? "http://localhost:8000"}/health`, { cache: "no-store" });
    api = response.ok ? "healthy" : "unavailable";
  } catch { /* API may be starting. */ }
  return <main className="mx-auto max-w-5xl p-8 md:p-16">
    <p className="text-sm font-bold uppercase tracking-widest text-blue-700">AgentForge</p>
    <h1 className="mt-6 text-5xl font-bold tracking-tight">90 days of AI engineering, one small task at a time.</h1>
    <p className="mt-6 max-w-2xl text-lg text-slate-600">A public build log for planning agents, coding workflows, evaluation, and production reliability.</p>
    <div className="mt-12 grid gap-4 md:grid-cols-3">
      {[ ["01", "Foundation", "API, dashboard, database, and planning"], ["02", "Agent workflows", "Coding, review, evaluation, and integrations"], ["03", "Production", "Monitoring, security, and deployment"] ].map(([n,title,desc]) => <section key={n} className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm"><span className="text-blue-700">{n}</span><h2 className="mt-4 text-xl font-semibold">{title}</h2><p className="mt-2 text-slate-600">{desc}</p></section>)}
    </div>
    <p className="mt-10 text-sm text-slate-500">API status: {api}</p>
  </main>;
}
