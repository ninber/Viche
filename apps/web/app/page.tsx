import { getFederationNode, getHealth, getSystemOverview } from "@/lib/api";

export default async function Home() {
  const [health, system, federationNode] = await Promise.all([
    getHealth(),
    getSystemOverview(),
    getFederationNode()
  ]);

  const modules = system?.modules ?? [];
  const planOneModules = modules.filter((module) => module.layer !== "federation");
  const federationModules = modules.filter((module) => module.layer === "federation");

  return (
    <main className="min-h-screen">
      <section className="border-b border-line bg-paper">
        <div className="mx-auto flex max-w-6xl flex-col gap-8 px-6 py-10 md:py-14">
          <div className="flex flex-wrap items-center justify-between gap-4">
            <div>
              <p className="text-sm font-semibold uppercase tracking-wide text-civic">Віче</p>
              <h1 className="mt-2 max-w-3xl text-4xl font-semibold leading-tight md:text-6xl">
                Civic deliberation infrastructure
              </h1>
            </div>
            <div className="border border-line bg-white px-4 py-3 text-sm">
              API:{" "}
              <span className={health?.status === "ok" ? "text-civic" : "text-red-700"}>
                {health?.status ?? "unreachable"}
              </span>
            </div>
          </div>
          <p className="max-w-3xl text-lg leading-8 text-neutral-700">
            Skeleton workspace for the Viche civic operating system: public portal, member
            cabinet, operator console, backend API, policy rules, journal verifier, and
            hierarchical federation layer.
          </p>
        </div>
      </section>

      <section className="mx-auto max-w-6xl px-6 py-8">
        <div className="mb-4 flex items-end justify-between gap-4">
          <div>
            <h2 className="text-2xl font-semibold">Plan 1 Core Skeleton</h2>
            <p className="mt-2 max-w-3xl text-sm leading-6 text-neutral-600">
              Local civic workflow modules exposed by the API as typed skeleton contracts.
            </p>
          </div>
          <span className="border border-line bg-white px-3 py-2 text-sm">
            {system?.canonical_language ?? "uk-UA"}
          </span>
        </div>
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {planOneModules.map((module) => (
            <div key={module.key} className="border border-line bg-white p-5">
              <div className="flex items-start justify-between gap-3">
                <h3 className="text-base font-semibold">{module.name}</h3>
                <span className="bg-paper px-2 py-1 text-xs">{module.status}</span>
              </div>
              <p className="mt-3 text-sm leading-6 text-neutral-600">{module.purpose}</p>
              <p className="mt-4 text-xs text-neutral-500">{module.plan_reference}</p>
            </div>
          ))}
        </div>
      </section>

      <section className="border-t border-line bg-white">
        <div className="mx-auto max-w-6xl px-6 py-8">
          <h2 className="text-2xl font-semibold">Plan 2 Federation Skeleton</h2>
          <p className="mt-2 max-w-3xl text-sm leading-6 text-neutral-600">
            Node discovery and bidirectional artifact flow are represented as API contracts for
            future town, regional, national, peer, partner, and mirror interoperability.
          </p>
          <div className="mt-6 grid gap-4 md:grid-cols-2">
            <div className="border border-line bg-paper p-5">
              <h3 className="text-base font-semibold">Local Node</h3>
              <dl className="mt-4 space-y-2 text-sm">
                <div className="flex justify-between gap-4">
                  <dt className="text-neutral-600">ID</dt>
                  <dd>{federationNode?.node_id ?? "unreachable"}</dd>
                </div>
                <div className="flex justify-between gap-4">
                  <dt className="text-neutral-600">Scope</dt>
                  <dd>{federationNode?.scope ?? "unknown"}</dd>
                </div>
                <div className="flex justify-between gap-4">
                  <dt className="text-neutral-600">Protocol</dt>
                  <dd>{federationNode?.protocol_versions.join(", ") ?? "none"}</dd>
                </div>
              </dl>
            </div>
            {federationModules.map((module) => (
              <div key={module.key} className="border border-line bg-paper p-5">
                <div className="flex items-start justify-between gap-3">
                  <h3 className="text-base font-semibold">{module.name}</h3>
                  <span className="bg-white px-2 py-1 text-xs">{module.status}</span>
                </div>
                <p className="mt-3 text-sm leading-6 text-neutral-600">{module.purpose}</p>
                <p className="mt-4 text-xs text-neutral-500">{module.plan_reference}</p>
              </div>
            ))}
          </div>
        </div>
      </section>
    </main>
  );
}

