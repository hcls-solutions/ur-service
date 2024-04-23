
# Initialize a new build stage and set the 
FROM python:3.9-slim

# Copy app code and set working directory
WORKDIR /app
COPY . /app/

#Set Environment variables
ENV LOCATION=us-central1
ENV GOOGLE_CLOUD_PROJECT=dp-workspace
ENV SEARCH_DATASTORE_ID=policies-and-guidelines-ds_1708548278784
ENV SEARCH_APP_ID=ur-search-app_1708548208198
ENV GOOGLE_APPLICATION_CREDENTIALS=adc.json

# Upgrade pip, install requirements and install curl
RUN pip install -U pip
RUN pip3 install -r requirements.txt
RUN apt-get -y update; apt-get -y install curl

# Expose port you want your app on
EXPOSE 8080

ENTRYPOINT ["streamlit", "run", "Home.py", "--server.port=8080", "--server.address=0.0.0.0"]

# Healthcheck
HEALTHCHECK CMD curl --fail http://localhost:8080/