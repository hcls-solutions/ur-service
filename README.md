# Utilization Review using Generative AI

Demonstrates use of Generative AI to streamline Utilization Review process in Healthcare. 

![Reference Architecture](app/images/ref_architecture.png "Reference Architecture")

## Prerequisite
You should complete the following steps before you start deploying the App.

  1. Create a [Google Cloud Project](https://cloud.google.com/resource-manager/docs/creating-managing-projects#creating_a_project) with billing enabled.

  2. You need a few PDF documents in a Google Cloud Storage (GCS) Bucket in your GCP Project. You can dowload [Internet-Only Manuals (IOMs) from CMS.gov](https://www.cms.gov/medicare/regulations-guidance/manuals/internet-only-manuals-ioms) and upload into a bucket in your GCP Project.

  3. Import sample prior authorization requests into a firestore. [Create a database in GCP Firestore](https://firebase.google.com/docs/firestore/manage-databases#create_a_database), and import the [sample data](firestore_data_pa_requests) into the database. You can refer to [this guide](https://firebase.google.com/docs/firestore/manage-data/export-import#import_all_documents_from_an_export) for importing the provided [sample data](firestore_data_pa_requests) to your Firestore database.
 
  4. Create a Cloud Storage Data Store in the Vertex AI Agent Builder to ingest PDF documents from the GCS Bucket you created earlier in step 2 above. [Here are the instructions](https://cloud.google.com/generative-ai-app-builder/docs/create-data-store-es#cloud-storage) to create a Cloud Storage Data Store in the Vertex AI Agent Builder.

  5. Create a Search App in the Vertex AI Agent Builder to implement Search and Summarization over the PDF documents. [Here are the instructions](https://cloud.google.com/generative-ai-app-builder/docs/create-engine-es) to create a Search App in your GCP Project.

## Deploy and run the App Locally
  1. Set environment variables:
```commandline
export GOOGLE_CLOUD_PROJECT=[your-project-id]

export BUCKET_NAME=[Bucket name where the PDF documents are stored]

export FIRESTORE_DATABASE=[your-firestore-database]

export SEARCH_APP_ID=[your-search-app-id]
export SEARCH_DATASTORE_ID=[your-search-datastore-id]
export LOCATION=[your-search-datastore-region]
export LLM_LOCATION=[your-LLM-region]
export LLM=[your-LLM]

gcloud config set project $GOOGLE_CLOUD_PROJECT
```

  2. Install dependencies
```commandline
pip install -r requirements.txt
```

  3. Authenticate to your GCP Project
```commandline
gcloud auth application-default login 
```

  4. Launch
```commandline
streamlit run src/Home.py
```

## Deploy and run the App on Cloud Run
  1. Set environment variables:   
```commandline
export GOOGLE_CLOUD_PROJECT=[your-project-id]

export BUCKET_NAME=[Bucket name where the PDF documents are stored]

export FIRESTORE_DATABASE=[your-firestore-database]

export SEARCH_APP_ID=[your-search-app-id]
export SEARCH_DATASTORE_ID=[your-search-datastore-id]
export LOCATION=[your-search-datastore-region]
export LLM_LOCATION=[your-LLM-region]
export LLM=[your-LLM]

export AR_REPO=[your-ar-repo-name]
export AR_REPO_LOCATION=[your-ar-repo-region]
export SERVICE_NAME=[your-app-name]
export SERVICE_ACCOUNT_NAME=[your-service-account-name]
<!-- export GROUP_EMAIL=[Gogole group containing users who need access to the Serice/UI] -->

gcloud config set project $GOOGLE_CLOUD_PROJECT
```  

  2. Initialize the project:  
    If this is the first time you are trying to deploy the App in your GCP Project, 
    you must enable APIs, Create an Artifact Registry, Create a Service Account and 
    configure IAM policies in your new GCP Project.  
    <span style="color:red">**You can skip this if a repository already exist!**</span>
```
./init.sh
```  

  3. Build the app and save it in the Artifact repository
```commandline
./build.sh
```

  4. Deploy the app from the Artifact repository to Cloud Run
```commandline
./deploy.sh
```