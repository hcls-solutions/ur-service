# Utilization Review using Generative AI

Demonstrates use of Generative AI to streamline Utilization Review process in Healthcare. 

![Reference Architecture](genai-demos/ur_service/app/images/ref_architecture.png "Reference Architecture")

## Deploy Locally
Set environment variables
```commandline
export LOCATION=[your-region]
export GOOGLE_CLOUD_PROJECT=[your-project-id]
export SEARCH_DATASTORE_ID=[your-search-datastore-id]
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

## Deploy to App Engine

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

Deploy
```commandline
gcloud app deploy
```

Browse
```commandline
gcloud app browse
```