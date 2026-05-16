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

const publicIdentitySchema = z.object({
  id: z.string(),
  handle: z.string(),
  display_name: z.string().nullable()
});

const memberSchema = z.object({
  id: z.string(),
  display_locale: z.string(),
  assurance_level: z.string(),
  status: z.string(),
  public_identity: publicIdentitySchema,
  created_at: z.string()
});

const proposalSchema = z.object({
  id: z.string(),
  submitter_member_id: z.string(),
  arena_id: z.string(),
  title: z.string(),
  body_markdown: z.string(),
  country_code: z.string(),
  region_code: z.string().nullable(),
  district_code: z.string().nullable(),
  community_code: z.string().nullable(),
  status: z.string(),
  tags: z.array(z.string()),
  created_at: z.string()
});

const publicProposalCollectionSchema = z.object({
  resource: z.literal("proposals"),
  status: z.literal("live"),
  items: z.array(proposalSchema)
});

const resolutionSchema = z.object({
  id: z.string(),
  panel_id: z.string(),
  proposal_id: z.string(),
  title: z.string(),
  body_markdown: z.string(),
  status: z.string(),
  decision_method: z.string(),
  published_at: z.string().nullable(),
  created_at: z.string()
});

const publicResolutionCollectionSchema = z.object({
  resource: z.literal("resolutions"),
  status: z.literal("live"),
  items: z.array(resolutionSchema)
});

export type SystemOverview = z.infer<typeof systemOverviewSchema>;
export type FederationNode = z.infer<typeof federationNodeSchema>;
export type Member = z.infer<typeof memberSchema>;
export type Proposal = z.infer<typeof proposalSchema>;
export type Resolution = z.infer<typeof resolutionSchema>;

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

export async function getPublicProposals(): Promise<Proposal[]> {
  const collection = await getJson("/v1/public/proposals", publicProposalCollectionSchema);
  return collection?.items ?? [];
}

export async function getPublicResolutions(): Promise<Resolution[]> {
  const collection = await getJson("/v1/public/resolutions", publicResolutionCollectionSchema);
  return collection?.items ?? [];
}

export function getBrowserApiBaseUrl(): string {
  return process.env.NEXT_PUBLIC_BROWSER_API_URL ?? "http://localhost:8000";
}
