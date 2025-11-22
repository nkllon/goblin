#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/../.." && pwd)"

# Login to GHCR using gh
"${SCRIPT_DIR}/ghcr_login.sh"

# Pull required images (act and ubuntu runner)
docker pull ghcr.io/nektos/act:latest 1>/dev/null
docker pull catthehacker/ubuntu:act-latest 1>/dev/null

ACT_IMG="ghcr.io/nektos/act:latest"
PARAMS=(-P "ubuntu-latest=catthehacker/ubuntu:act-latest")

run_job() {
  local job="$1"
  docker run --rm \
    -v /var/run/docker.sock:/var/run/docker.sock \
    -v "${ROOT_DIR}":/github/workspace \
    -v "${HOME}/.act":/root/.act \
    -w /github/workspace \
    "${ACT_IMG}" pull_request -j "${job}" "${PARAMS[@]}"
}

# Allow override: ACT_JOBS="job1 job2"
JOBS="${ACT_JOBS:-validate-and-build js python-validate dot-check docs-link}"
for job in ${JOBS}; do
  echo "=== ${job} ==="
  run_job "${job}"
  echo "=== done: ${job} ==="
done
