import argparse
import json
from pathlib import Path


def verify_jsonl(path: Path) -> int:
    previous_hash: str | None = None
    count = 0

    with path.open("r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            if not line.strip():
                continue
            record = json.loads(line)
            if record.get("previous_hash") != previous_hash:
                print(f"hash-chain mismatch at line {line_number}")
                return 1
            previous_hash = record.get("entry_hash")
            count += 1

    print(f"verified {count} journal entries")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify a Viche journal JSONL export.")
    parser.add_argument("path", type=Path)
    args = parser.parse_args()
    return verify_jsonl(args.path)


if __name__ == "__main__":
    raise SystemExit(main())

