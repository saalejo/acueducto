#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [ -f "$SCRIPT_DIR/.env" ]; then
  set -o allexport
  source "$SCRIPT_DIR/.env"
  set +o allexport
fi

IMAGE="saalejo/acueducto:latest"
NAMESPACE="acueducto-sonadora"
DEPLOYMENT="acueducto-deployment"
SSH_KEY="$DEPLOY_SSH_KEY"
SERVER="$DEPLOY_SERVER"

echo "==> Checking Docker Hub login..."
if ! podman login --get-login docker.io &>/dev/null; then
  if [ -n "${DOCKERHUB_USER:-}" ] && [ -n "${DOCKERHUB_TOKEN:-}" ]; then
    echo "$DOCKERHUB_TOKEN" | podman login docker.io -u "$DOCKERHUB_USER" --password-stdin
  else
    echo "    Not logged in. Please enter your Docker Hub credentials:"
    podman login docker.io
  fi
fi

echo "==> Building image with podman..."
podman build --platform linux/arm64 -t "$IMAGE" .

echo "==> Pushing image to registry..."
podman push "$IMAGE"

echo "==> Rolling out deployment on server..."
ssh -i "$SSH_KEY" "$SERVER" \
  "kubectl rollout restart deployment/$DEPLOYMENT -n $NAMESPACE && \
   kubectl rollout status deployment/$DEPLOYMENT -n $NAMESPACE"

echo "==> Done."
