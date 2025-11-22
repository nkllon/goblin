#!/usr/bin/env bash
set -euo pipefail

# Preconditions
if ! command -v docker >/dev/null 2>&1; then
  echo "docker is required" >&2
  exit 1
fi
if ! command -v gh >/dev/null 2>&1; then
  echo "gh (GitHub CLI) is required. Install via: brew install gh" >&2
  exit 1
fi

# Resolve username and token via gh, allow env overrides
GH_USER="${GITHUB_USER:-}"
if [[ -z "${GH_USER}" ]]; then
  GH_USER="$(gh api user -q .login)"
fi

TOKEN="${GITHUB_TOKEN:-}"
if [[ -z "${TOKEN}" ]]; then
  TOKEN="$(gh auth token)"
fi

if [[ -z "${GH_USER}" || -z "${TOKEN}" ]]; then
  echo "Missing GH creds. Ensure gh is logged in (gh auth status) or export GITHUB_USER/GITHUB_TOKEN." >&2
  exit 1
fi

# Login to GHCR
printf '%s' "${TOKEN}" | docker login ghcr.io -u "${GH_USER}" --password-stdin 1>/dev/null
echo "Logged in to ghcr.io as ${GH_USER}"
