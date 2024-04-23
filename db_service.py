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
import firebase_admin # type: ignore
from firebase_admin import credentials # type: ignore
from firebase_admin import firestore # type: ignore
import json
import utils

cred = credentials.ApplicationDefault()

if not firebase_admin._apps:
    firebase_admin.initialize_app(cred, {
        'projectId': utils.PROJECT_ID,
    })


def get_pa_request_docs():
    db = firestore.client()
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
    db = firestore.client()
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