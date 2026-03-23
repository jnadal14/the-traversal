#!/usr/bin/env bash
# Resize & recompress gallery JPEGs for web (macOS built-in sips).
# Max edge 2200px, JPEG ~78% quality — good for full-width ~1200px layouts.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

optimize_jpg() {
  local f="$1"
  [[ -f "$f" ]] || return 0
  [[ "$f" == *README* ]] && return 0
  local tmp="${f}.tmp.jpg"
  sips -Z 2200 -s format jpeg -s formatOptions 78 "$f" --out "$tmp" >/dev/null
  mv "$tmp" "$f"
  echo "OK $f"
}

echo "Optimizing IMAGES/*.jpg and IMAGES/new/*.jpg …"
shopt -s nullglob
for f in IMAGES/*.jpg IMAGES/new/*.jpg; do
  optimize_jpg "$f"
done
echo "Done."
