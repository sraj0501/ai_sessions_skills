#!/usr/bin/env python3
"""Read a dotted key out of config.json, with a fallback default.

    cfg.py distill.timeout_seconds 900
    cfg.py model swe-1-7-medium
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main() -> int:
    key, default = sys.argv[1], (sys.argv[2] if len(sys.argv) > 2 else "")
    try:
        node = json.loads((ROOT / "config.json").read_text(encoding="utf-8"))
        for part in key.split("."):
            node = node[part]
    except Exception:
        print(default)
        return 0
    if isinstance(node, bool):
        print("true" if node else "false")
    elif isinstance(node, (list, dict)):
        print(json.dumps(node))
    else:
        print(node)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
