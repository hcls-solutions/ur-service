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
logger = logging.getLogger(__name__)

from google.protobuf.json_format import MessageToDict # type: ignore
import streamlit as st # type: ignore
from google.cloud import discoveryengine
from google.cloud.discoveryengine_v1.services.document_service.pagers import ListDocumentsPager # type: ignore
from ur.utils import to_proto, PROJECT_ID, SEARCH_DATASTORE_ID, LOCATION

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
        project_id=PROJECT_ID,
        search_engine_id=SEARCH_DATASTORE_ID,
        location=LOCATION)
    for doc in docs:
        if type(doc.struct_data).__name__ == 'MapComposite':
            doc_info = MessageToDict(to_proto(doc.struct_data.pb))
        else:
            doc_info = MessageToDict(doc.struct_data)
        url = doc_info.get('url')
        if url == None:
            url = "None"      
        logger.info("########## url #############")
        logger.info(url)
        logger.info("############################")
        id = doc.id
        name =  doc.name
        gcs_uri = doc.content.uri
        metadata = {}
        metadata['id'] = id
        metadata['url'] = url
        metadata['name'] = name
        metadata['gcs_uri'] = gcs_uri
        corpus.append(metadata)

    return corpus
