#!/usr/bin/env bash
set -euo pipefail

mkdir -p ssl/local

command -v mkcert >/dev/null || { echo "mkcert missing. Install: brew install mkcert"; exit 1; }
mkcert -install

mkcert -cert-file ssl/local/dev.local.crt -key-file ssl/local/dev.local.key "*.dev.local" dev.local

for ns in client-wp client-pts; do
  kubectl get ns "$ns" >/dev/null 2>&1 || kubectl create ns "$ns"
  kubectl -n "$ns" create secret tls dev-local-tls \
    --cert=ssl/local/dev.local.crt \
    --key=ssl/local/dev.local.key \
    --dry-run=client -o yaml | kubectl apply -f -
done

echo "TLS secrets created in client-wp and client-pts"
