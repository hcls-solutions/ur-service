# Utilization Review using Generative AI

Demonstrates use of Generative AI to streamline Utilization Review process in Healthcare. 

![Reference Architecture](app/images/ref_architecture.png "Reference Architecture")

## Prerequisite
### You need a Data Store and a Search App in the Vertex AI Agent Builder in your Google Cloud Platform (GCP) Project.

#### 1. Follow [these instructions](https://cloud.google.com/generative-ai-app-builder/docs/create-data-store-es) to create a Data Store in your GCP Project.

#### 2. Follow [these instructions](https://cloud.google.com/generative-ai-app-builder/docs/create-engine-es) to create a Search App in your GCP Project.

## Deploy Locally
Set environment variables
```commandline
export GOOGLE_CLOUD_PROJECT=[your-project-id]
export SEARCH_DATASTORE_ID=[your-search-datastore-id]
export LOCATION=[your-search-datastore-region]
export SEARCH_APP_ID=[your-search-app-id]
export LLM_LOCATION=[your-LLM-region]
export LLM=[your-LLM]
```

Install dependencies
```commandline
pip install -r requirements.txt
```

Authenticate to your GCP Project
```commandline
gcloud auth application-default login 
```

Launch
```commandline
streamlit run Home.py
```

## Deploy to Cloud Run
Update following ENV attributes in the [Dockerfile](./Dockerfile)  
```
ENV LOCATION=[your-region]
ENV GOOGLE_CLOUD_PROJECT=[your-project-id]
ENV SEARCH_DATASTORE_ID=[your-search-datastore-id]
ENV SEARCH_APP_ID=[your-search-app-id]
ENV LLM_LOCATION=[your-LLM_LOCATION]
ENV LLM=[your-LLM]
```

Set environment variables
```commandline
export AR_REPO=[your-ar-repo-name]
export AR_REPO_LOCATION=[your-ar-repo-region]
export SERVICE_NAME=[your-app-name]
```

Create Artifact repository in your GCP Project. 
<span style="color:red">**You can skip this if a repository already exist!**</span>
```commandline
gcloud artifacts repositories create "$AR_REPO" --location="$AR_REPO_LOCATION" --repository-format=Docker
```

Build the app and save it in the Artifact repository
```commandline
./build.sh
```

Deploy the app from the Artifact repository to Cloud Run
```commandline
./deploy.sh
```

Test locally using Cloud Run proxy
```
./run_proxy.sh
```