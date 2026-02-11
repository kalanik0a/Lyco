from __future__ import annotations

import json
import os
from datetime import datetime, timedelta, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "build" / "ci" / "last_run.json"


def main() -> int:
    if os.environ.get("CI_GUARD_ALLOW") == "1":
        print("CI guard bypassed via CI_GUARD_ALLOW=1.")
        return 0

    days = int(os.environ.get("CI_GUARD_DAYS", "1"))
    if not ARTIFACT.exists():
        print("No prior CI artifact found. Proceeding.")
        return 0

    data = json.loads(ARTIFACT.read_text(encoding="utf-8"))
    last = data.get("timestamp")
    if not last:
        return 0
    last_dt = datetime.fromisoformat(last)
    if last_dt.tzinfo is None:
        last_dt = last_dt.replace(tzinfo=timezone.utc)
    now = datetime.now(timezone.utc)
    if now - last_dt < timedelta(days=days):
        print(
            "CI guard: last full run is recent. "
            f"Set CI_GUARD_ALLOW=1 to proceed. (last={last_dt.isoformat()})"
        )
        return 3
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
