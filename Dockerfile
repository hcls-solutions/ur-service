
# Initialize a new build stage and set the 
FROM python:3.10

# Expose port you want your app on
EXPOSE 8080

# Copy app code and set working directory
WORKDIR /app
COPY . ./

# Upgrade pip, install requirements and install curl
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

# TODO - Implement Sign On in the App and use the service account to access the GCP APIs
ENV GOOGLE_APPLICATION_CREDENTIALS=./adc.json
ENTRYPOINT ["streamlit", "run", "Home.py", "--server.port=8080", "--server.address=0.0.0.0"]