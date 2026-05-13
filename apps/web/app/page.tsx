import { getHealth } from "@/lib/api";

const workstreams = [
  "Membership and identity separation",
  "Proposal graph and moderation",
  "Reproducible sortition",
  "Mandates and panel lifecycle",
  "Resolutions and official follow-up",
  "Tamper-evident journal"
];

export default async function Home() {
  const health = await getHealth();

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
            Skeleton workspace for the Viche public portal, member cabinet, operator console,
            backend API, policy rules, and journal verifier.
          </p>
        </div>
      </section>

      <section className="mx-auto grid max-w-6xl gap-4 px-6 py-8 md:grid-cols-2 lg:grid-cols-3">
        {workstreams.map((item) => (
          <div key={item} className="border border-line bg-white p-5">
            <h2 className="text-base font-semibold">{item}</h2>
            <p className="mt-3 text-sm leading-6 text-neutral-600">
              Planned implementation track from Plan_1.md.
            </p>
          </div>
        ))}
      </section>
    </main>
  );
}

