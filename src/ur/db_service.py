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

import streamlit as st # type: ignore
import google.cloud.firestore as firestore # type: ignore
import google.auth as auth # type: ignore
from google.cloud.firestore import Client # type: ignore
import json
from ur.utils import PROJECT_ID, FIRESTORE_DATABASE


import logging
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

# cred = auth.default()[0]

def get_pa_request_docs():
    db = Client(project=PROJECT_ID, database=FIRESTORE_DATABASE)
    docs = db.collection('pa_requests').stream()
    return docs

@st.cache_data
def get_pa_requests():
    docs = get_pa_request_docs()
    pa_requests = []
    for doc in docs:
        pa_requests.append(doc.to_dict())
    return pa_requests    

@st.cache_data
def get_pa_request(pa_request_id):
    db = Client(project=PROJECT_ID, database=FIRESTORE_DATABASE)
    doc_ref = db.collection("pa_requests").document(pa_request_id)
    doc_ref.update({"prompt": firestore.DELETE_FIELD})
    doc = doc_ref.get()
    pa_request = json.dumps(doc.to_dict())
    return pa_request

@st.cache_data
def get_pa_request_ids() -> list:
    docs = get_pa_request_docs()
    pa_request_ids = []
    for doc in docs:
        pa_request_ids.append(doc.id)
    return pa_request_ids