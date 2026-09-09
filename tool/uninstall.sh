#!/bin/sh
# Convenience shim for macOS/Linux. All logic lives in uninstall.py.
#   ./uninstall.sh [--only a,b]
DIR="$(CDPATH='' cd -- "$(dirname -- "$0")" && pwd)"
for PY in python3 python; do
  if command -v "$PY" >/dev/null 2>&1; then
    exec "$PY" "$DIR/uninstall.py" "$@"
  fi
done
echo "python3 is required but was not found" >&2
exit 1
