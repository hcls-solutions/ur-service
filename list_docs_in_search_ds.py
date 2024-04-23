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

from __future__ import annotations

import logging
logging.basicConfig(level=logging.ERROR)

import streamlit as st # type: ignore
from google.protobuf.json_format import MessageToDict # type: ignore
from google.cloud import discoveryengine
from google.cloud.discoveryengine_v1.services.document_service.pagers import ListDocumentsPager # type: ignore
import utils

def fetch_docs_from_search_ds(
        project_id: str,
        search_engine_id: str,
        location: str = 'global',
) -> ListDocumentsPager:
    """List Enterprise Search Corpus"""
    client = discoveryengine.DocumentServiceClient()
    parent = "projects/" + project_id + "/locations/" + location + \
        "/collections/default_collection/dataStores/" + search_engine_id + "/branches/default_branch"
    request = discoveryengine.ListDocumentsRequest(parent=parent)
    return client.list_documents(request=request)

@st.cache_data
def list_docs() -> list[dict]:
    corpus = []
    docs = fetch_docs_from_search_ds(
        project_id=utils.PROJECT_ID,
        search_engine_id=utils.SEARCH_DATASTORE_ID,
        location=utils.LOCATION)
    for doc in docs: 
        logging.info("--------Document ------")   
        logging.info(doc) 
        logging.info("--------Document Type ------")   
        logging.info(type(doc))
        logging.info("--------Struct Data------")   
        logging.info(type(doc.struct_data))
        metadata = {}
        metadata['id'] = doc.id
        metadata['gcs_uri'] = doc.content.uri
        corpus.append(metadata)
    logging.info(corpus)
    return corpus
