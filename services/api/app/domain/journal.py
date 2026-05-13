import hashlib
import json
from datetime import UTC, datetime
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import JournalEntry


def canonical_json(data: dict[str, Any]) -> str:
    return json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def sha256_digest(value: str) -> str:
    return f"sha256:{hashlib.sha256(value.encode('utf-8')).hexdigest()}"


async def append_journal_entry(
    session: AsyncSession,
    *,
    event_type: str,
    actor_type: str,
    actor_id: str | None,
    subject_type: str,
    subject_id: str,
    payload: dict[str, Any],
) -> JournalEntry:
    previous_hash = await session.scalar(
        select(JournalEntry.entry_hash).order_by(JournalEntry.sequence.desc()).limit(1)
    )
    occurred_at = datetime.now(UTC)
    payload_hash = sha256_digest(canonical_json(payload))
    entry_material = {
        "event_type": event_type,
        "actor_type": actor_type,
        "actor_id": actor_id,
        "subject_type": subject_type,
        "subject_id": subject_id,
        "payload_hash": payload_hash,
        "previous_hash": previous_hash,
        "occurred_at": occurred_at.isoformat(),
    }
    entry = JournalEntry(
        event_type=event_type,
        actor_type=actor_type,
        actor_id=actor_id,
        subject_type=subject_type,
        subject_id=subject_id,
        payload=payload,
        payload_hash=payload_hash,
        previous_hash=previous_hash,
        entry_hash=sha256_digest(canonical_json(entry_material)),
        occurred_at=occurred_at,
    )
    session.add(entry)
    await session.flush()
    return entry

