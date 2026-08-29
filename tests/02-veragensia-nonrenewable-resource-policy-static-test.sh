#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

required=(
  "AUTHENTICATION HARD STOP"
  "NEVER automate with a nonrenewable resource"
  "NO recovery code automation"
  "existing \`gh\` CLI/API session"
  "private ephemeral Veragensia"
  "email OTP"
  "GitHub App"
  "SSH/deploy key"
  "device OAuth"
  "One failed route is not exhaustion"
  "Mandatory provider-auth preflight"
)

for file in AGENTS.md docs/183-veragensia-public-agent-computer-security-and-lifecycle.md; do
  for needle in "${required[@]}"; do
    grep -Fq "$needle" "$file" || {
      printf 'missing required authentication warning in %s: %s\n' "$file" "$needle" >&2
      exit 1
    }
  done
done

forbidden_regex='--method[[:space:]]+8|bw-recovery-code|RecoveryCode=8|working headless path.*recovery|broker-bound recovery-code challenge resolution'
if grep -RniE -- "$forbidden_regex" AGENTS.md docs overlay scripts README.md 2>/dev/null; then
  echo 'forbidden automated recovery-code instruction found' >&2
  exit 1
fi

echo 'veragensia nonrenewable-resource policy static test: PASS'
