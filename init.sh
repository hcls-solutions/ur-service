#!/bin/bash

# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable artifactregistry.googleapis.com

gcloud artifacts repositories create "$AR_REPO" \
  --project="$GOOGLE_CLOUD_PROJECT" \
  --location="$AR_REPO_LOCATION" \
  --repository-format=Docker > /dev/null 2>&1

gcloud iam service-accounts create "$SERVICE_NAME-identity" \
  --description="Service account for $SERVICE_NAME" \
  --display-name="$SERVICE_NAME service identity" \
  --project="$GOOGLE_CLOUD_PROJECT" > /dev/null 2>&1

roles=(
    "roles/datastore.user"
    "roles/datastore.viewer"
    "roles/discoveryengine.viewer"
    "roles/storage.objectViewer"
    "roles/aiplatform.user"
)

for role in "${roles[@]}"; do
  gcloud projects add-iam-policy-binding $GOOGLE_CLOUD_PROJECT \
    --member="serviceAccount:$SERVICE_NAME-identity@$GOOGLE_CLOUD_PROJECT.iam.gserviceaccount.com" \
    --role="$role" \
    --project="$GOOGLE_CLOUD_PROJECT" > /dev/null 2>&1
done

PROJECT_NUMBER=$(gcloud projects list --filter="$GOOGLE_CLOUD_PROJECT" --format="value(projectNumber)")

ce_roles=(
    "roles/storage.objectViewer"
    "roles/logging.logWriter"
    "roles/artifactregistry.writer"
    "roles/artifactregistry.reader"
    "artifactregistry.repositories.uploadArtifacts"
)

for ce_role in "${ce_roles[@]}"; do
  gcloud projects add-iam-policy-binding $GOOGLE_CLOUD_PROJECT \
      --member="serviceAccount:$PROJECT_NUMBER-compute@developer.gserviceaccount.com" \
      --role="$ce_role" \
      --project="$GOOGLE_CLOUD_PROJECT" > /dev/null 2>&1
done