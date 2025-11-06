#!/usr/bin/env bash
set -euo pipefail

PROJECT_ID="$(gcloud config get-value project)"
REGION="${REGION:-northamerica-northeast1}"
REPO="${REPO:-engdrill-repo}"
IMAGE_TAG="${IMAGE_TAG:-engdrill-api:1}"
SERVICE_NAME="${SERVICE_NAME:-engdrill-api}"

echo "[i] Project: $PROJECT_ID"
echo "[i] Region : $REGION"
echo "[i] Repo   : $REPO"
echo "[i] Image  : $IMAGE_TAG"

gcloud artifacts repositories create "$REPO" --repository-format=docker --location="$REGION" || true

gcloud builds submit --tag "$REGION-docker.pkg.dev/$PROJECT_ID/$REPO/$IMAGE_TAG"

gcloud run deploy "$SERVICE_NAME"   --image="$REGION-docker.pkg.dev/$PROJECT_ID/$REPO/$IMAGE_TAG"   --region="$REGION" --platform=managed   --memory=1Gi --cpu=1 --concurrency=1 --timeout=60   --min-instances=0 --max-instances=2   --allow-unauthenticated