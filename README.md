# Utilization Review using Generative AI

Demonstrates use of Generative AI to streamline Utilization Review process in Healthcare. 

![Reference Architecture](app/images/ref_architecture.png "Reference Architecture")

## Prerequisite
You should complete the following three steps before you start deploying the App.

1. You need a few PDF documents in a Google Cloud Storage (GCS) Bucket in your GCP Project.

2. Import sample prior authorization requests into a firestore.  
[Create a database in GCP Firestore](https://firebase.google.com/docs/firestore/manage-databases#create_a_database), and import the [sample data](firestore_data_pa_requests) into the database. You can refer to [this guide](https://firebase.google.com/docs/firestore/manage-data/export-import#import_all_documents_from_an_export) for importing the provided [sample data](firestore_data_pa_requests) to your Firestore database.
 
3. Create a Cloud Storage Data Store in the Vertex AI Agent Builder to ingest PDF documents from the GCS Bucket. [Here are the instructions](https://cloud.google.com/generative-ai-app-builder/docs/create-data-store-es#cloud-storage) to create a Cloud Storage Data Store in the Vertex AI Agent Builder.

4. Create a Search App in the Vertex AI Agent Builder to implement Search and Summarization over the PDF documents. [Here are the instructions](https://cloud.google.com/generative-ai-app-builder/docs/create-engine-es) to create a Search App in your GCP Project.

## Deploy Locally
Set environment variables:
```commandline
export GOOGLE_CLOUD_PROJECT=[your-project-id]
export SEARCH_DATASTORE_ID=[your-search-datastore-id]
export FIRESTORE_DATABASE=[your-firestore-database]
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
streamlit run src/Home.py
```

## Deploy to Cloud Run
Set environment variables
```commandline
export AR_REPO=[your-ar-repo-name]
export AR_REPO_LOCATION=[your-ar-repo-region]
export SERVICE_NAME=[your-app-name]
```

If this is the first time you are trying to deploy the App in your GCP Project, 
you must enable APIs and Create an Artifact repository in your new GCP Project. 
<span style="color:red">**You can skip this if a repository already exist!**</span>
```commandline
gcloud config set project $GOOGLE_CLOUD_PROJECT

gcloud artifacts repositories create "$AR_REPO" --location="$AR_REPO_LOCATION" --repository-format=Docker

gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com

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