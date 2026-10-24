#!/usr/bin/env bash
set -euo pipefail
repo_root=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)
if [[ $# != 1 ]]; then echo "usage: $0 /path/to/original/th06.exe" >&2; exit 2; fi
python3 "$repo_root/scripts/verify-target.py" "$1"
mkdir -p "$repo_root/resources"
cp -- "$1" "$repo_root/resources/th06.exe"
