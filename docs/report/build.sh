#!/usr/bin/env bash
set -euo pipefail

SITE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BASE_URL="${HUGO_BASEURL:-https://herijooj.github.io/redes2/}"

mkdir -p "${SITE_DIR}/content"
cp "${SITE_DIR}/report.md" "${SITE_DIR}/content/_index.md"

hugo \
  --source "${SITE_DIR}" \
  --destination "${SITE_DIR}/public" \
  --cleanDestinationDir \
  --minify \
  --baseURL "${BASE_URL}"
