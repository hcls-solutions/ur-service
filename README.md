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
export LOCATION=[your-region]
export GOOGLE_CLOUD_PROJECT=[your-project-id]
export SEARCH_DATASTORE_ID=[your-search-datastore-id]
export SEARCH_APP_ID=[your-search-app-id]
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

<!-- ## Deploy to App Engine

Ensure the default App Engine service account has the following IAM permissions:
- Discovery Engine Editor
- Discovery Engine Service Agent

Set the environment variables in `app.yaml`
```yaml
env_variables:
    LOCATION: your-region
    GOOGLE_CLOUD_PROJECT: your-project-id
    SEARCH_DATASTORE_ID: your-search-datastore-id
```

If a default network does not exist in your GCP Project. You can run the following to create a default network. 
Default network is required for the App Engine deployment.
```commandline
gcloud compute networks create default
```

Initialize gcloud with the right GCP project.
```commandline
gcloud init
```

Deploy
```commandline
gcloud app deploy
```

Browse
```commandline
gcloud app browse
``` -->
