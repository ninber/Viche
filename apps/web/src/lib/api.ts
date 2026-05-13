import { z } from "zod";

const healthSchema = z.object({
  status: z.enum(["ok", "degraded"]),
  service: z.string(),
  environment: z.string(),
  database: z.object({ status: z.enum(["ok", "error"]), detail: z.string().nullable().optional() }),
  redis: z.object({ status: z.enum(["ok", "error"]), detail: z.string().nullable().optional() })
});

export type Health = z.infer<typeof healthSchema>;

const systemModuleSchema = z.object({
  key: z.string(),
  name: z.string(),
  layer: z.enum(["trust", "civic", "interaction", "federation"]),
  status: z.enum(["planned", "skeleton", "pilot", "production"]),
  purpose: z.string(),
  plan_reference: z.string()
});

const systemOverviewSchema = z.object({
  name: z.string(),
  canonical_language: z.string(),
  modules: z.array(systemModuleSchema)
});

const federationNodeSchema = z.object({
  node_id: z.string(),
  name: z.string(),
  scope: z.string(),
  protocol_versions: z.array(z.string()),
  supported_languages: z.array(z.string()),
  public_api_base: z.string(),
  transparency_log_url: z.string().nullable()
});

export type SystemOverview = z.infer<typeof systemOverviewSchema>;
export type FederationNode = z.infer<typeof federationNodeSchema>;

async function getJson<T>(path: string, schema: z.ZodSchema<T>): Promise<T | null> {
  const baseUrl = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

  try {
    const response = await fetch(`${baseUrl}${path}`, { cache: "no-store" });
    if (!response.ok) {
      return null;
    }
    return schema.parse(await response.json());
  } catch {
    return null;
  }
}

export async function getHealth(): Promise<Health | null> {
  return getJson("/v1/health", healthSchema);
}

export async function getSystemOverview(): Promise<SystemOverview | null> {
  return getJson("/v1/system", systemOverviewSchema);
}

export async function getFederationNode(): Promise<FederationNode | null> {
  return getJson("/v1/federation/node", federationNodeSchema);
}
