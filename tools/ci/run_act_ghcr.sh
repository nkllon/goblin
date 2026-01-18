#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/../.." && pwd)"

# Login to GHCR using gh (for private registries if needed)
"${SCRIPT_DIR}/ghcr_login.sh" || true

# Prefer local act binary; require it for reliability
if ! command -v act >/dev/null 2>&1; then
  echo "act not found. Please install: brew install act" >&2
  exit 1
fi

# Pull runner image (ubuntu)
docker pull catthehacker/ubuntu:act-latest 1>/dev/null

PARAMS=(-P "ubuntu-latest=catthehacker/ubuntu:act-latest")

# Allow override: ACT_JOBS="job1 job2"
JOBS="${ACT_JOBS:-validate-and-build js python-validate dot-check docs-link}"
for job in ${JOBS}; do
  echo "=== ${job} ==="
  act pull_request -j "${job}" "${PARAMS[@]}"
  echo "=== done: ${job} ==="
done
