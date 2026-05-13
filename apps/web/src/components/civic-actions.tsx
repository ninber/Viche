"use client";

import { FormEvent, useState } from "react";

import { getBrowserApiBaseUrl, Member, Proposal } from "@/lib/api";

type RegisterResponse = {
  member: Member;
  journal_entry_id: string;
  journal_entry_hash: string;
};

type SubmitProposalResponse = {
  proposal: Proposal;
  journal_entry_id: string;
  journal_entry_hash: string;
};

async function postJson<T>(path: string, body: unknown): Promise<T> {
  const response = await fetch(`${getBrowserApiBaseUrl()}${path}`, {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify(body)
  });

  if (!response.ok) {
    const text = await response.text();
    throw new Error(text || `Request failed with ${response.status}`);
  }

  return response.json() as Promise<T>;
}

export function CivicActions() {
  const [member, setMember] = useState<Member | null>(null);
  const [proposal, setProposal] = useState<Proposal | null>(null);
  const [journalHash, setJournalHash] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isBusy, setIsBusy] = useState(false);

  async function registerMember(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setIsBusy(true);
    setError(null);

    const form = new FormData(event.currentTarget);
    try {
      const result = await postJson<RegisterResponse>("/v1/members/register", {
        display_locale: "uk-UA",
        assurance_method: "self_declared",
        public_display_name: form.get("public_display_name")?.toString() || null,
        consents: {
          privacy_notice_version: "draft-2026-05-13",
          terms_version: "draft-2026-05-13",
          public_profile_opt_in: Boolean(form.get("public_profile_opt_in"))
        }
      });
      setMember(result.member);
      setJournalHash(result.journal_entry_hash);
    } catch (requestError) {
      setError(requestError instanceof Error ? requestError.message : "Unknown registration error");
    } finally {
      setIsBusy(false);
    }
  }

  async function submitProposal(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!member) {
      setError("Register a member first.");
      return;
    }

    setIsBusy(true);
    setError(null);
    const form = new FormData(event.currentTarget);
    const tags = form
      .get("tags")
      ?.toString()
      .split(",")
      .map((tag) => tag.trim())
      .filter(Boolean);

    try {
      const result = await postJson<SubmitProposalResponse>("/v1/proposals", {
        submitter_member_id: member.id,
        arena_id: "00000000-0000-4000-8000-000000000001",
        title: form.get("title")?.toString(),
        body_markdown: form.get("body_markdown")?.toString(),
        jurisdiction: {
          country_code: "UA",
          region_code: form.get("region_code")?.toString() || null,
          district_code: null,
          community_code: form.get("community_code")?.toString() || null
        },
        tags
      });
      setProposal(result.proposal);
      setJournalHash(result.journal_entry_hash);
    } catch (requestError) {
      setError(requestError instanceof Error ? requestError.message : "Unknown proposal error");
    } finally {
      setIsBusy(false);
    }
  }

  return (
    <section className="border-t border-line bg-paper">
      <div className="mx-auto grid max-w-6xl gap-6 px-6 py-8 lg:grid-cols-2">
        <form className="border border-line bg-white p-5" onSubmit={registerMember}>
          <h2 className="text-2xl font-semibold">Register Pilot Member</h2>
          <label className="mt-5 block text-sm font-medium" htmlFor="public_display_name">
            Public display name
          </label>
          <input
            className="mt-2 w-full border border-line px-3 py-2"
            id="public_display_name"
            name="public_display_name"
            placeholder="Олена"
          />
          <label className="mt-4 flex items-center gap-2 text-sm">
            <input name="public_profile_opt_in" type="checkbox" />
            Public profile opt-in
          </label>
          <button
            className="mt-5 border border-civic bg-civic px-4 py-2 text-sm font-semibold text-white disabled:opacity-50"
            disabled={isBusy}
            type="submit"
          >
            Register
          </button>
          {member ? (
            <p className="mt-4 text-sm text-neutral-700">
              Registered {member.public_identity.handle} ({member.id})
            </p>
          ) : null}
        </form>

        <form className="border border-line bg-white p-5" onSubmit={submitProposal}>
          <h2 className="text-2xl font-semibold">Submit Proposal</h2>
          <label className="mt-5 block text-sm font-medium" htmlFor="title">
            Title
          </label>
          <input
            className="mt-2 w-full border border-line px-3 py-2"
            id="title"
            name="title"
            placeholder="Improve pedestrian crossing safety"
            required
          />
          <label className="mt-4 block text-sm font-medium" htmlFor="body_markdown">
            Body
          </label>
          <textarea
            className="mt-2 min-h-28 w-full border border-line px-3 py-2"
            id="body_markdown"
            name="body_markdown"
            placeholder="Describe the civic problem, evidence, and requested action."
            required
          />
          <div className="mt-4 grid gap-3 md:grid-cols-3">
            <input className="border border-line px-3 py-2" name="region_code" placeholder="Region" />
            <input
              className="border border-line px-3 py-2"
              name="community_code"
              placeholder="Community"
            />
            <input className="border border-line px-3 py-2" name="tags" placeholder="tags,civic" />
          </div>
          <button
            className="mt-5 border border-civic bg-civic px-4 py-2 text-sm font-semibold text-white disabled:opacity-50"
            disabled={isBusy || !member}
            type="submit"
          >
            Submit
          </button>
          {proposal ? (
            <p className="mt-4 text-sm text-neutral-700">
              Submitted proposal {proposal.id}: {proposal.title}
            </p>
          ) : null}
        </form>

        <div className="lg:col-span-2">
          {journalHash ? <p className="text-sm text-neutral-700">Last journal hash: {journalHash}</p> : null}
          {error ? <p className="mt-2 text-sm text-red-700">{error}</p> : null}
        </div>
      </div>
    </section>
  );
}
