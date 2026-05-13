import { z } from "zod";

const healthSchema = z.object({
  status: z.enum(["ok", "degraded"]),
  service: z.string(),
  environment: z.string(),
  database: z.object({ status: z.enum(["ok", "error"]), detail: z.string().nullable().optional() }),
  redis: z.object({ status: z.enum(["ok", "error"]), detail: z.string().nullable().optional() })
});

export type Health = z.infer<typeof healthSchema>;

export async function getHealth(): Promise<Health | null> {
  const baseUrl = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

  try {
    const response = await fetch(`${baseUrl}/v1/health`, { cache: "no-store" });
    if (!response.ok) {
      return null;
    }
    return healthSchema.parse(await response.json());
  } catch {
    return null;
  }
}

