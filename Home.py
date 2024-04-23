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

st.set_page_config(
    page_title="Utilization Review",
    page_icon='app/images/logo.png',
    layout="wide",
)

cols = st.columns([10, 90])
with cols[0]:
    st.write('')
    st.image('app/images/logo.png', '', 64)
with cols[1]:
    st.header(':green[Utilization Review Application]')

st.markdown('''   ''')

cols = st.columns([55, 45])
with cols[0]:
    st.markdown('''
        ### About
        This demo app illustrates the use of GCP services like Agent Builder to perform utilization review. 
        It also supports retrieval and question answering with citation on 
        policies and clinical guidelines documents. 
        It allows UR specialists to quickly process 
        the prior authorization requests using AI generated recommendations.
    ''')
    st.markdown('''
        ### Enterprise Search
        The use of Enterprise Search provides powerful functionality out of the box:
        1. It not only fetches the most relevant documents, it also identifies the most relevant snippets within each 
        document.
        2. It feeds the relevant snippets into an LLM and generates a summary answer. In effect it is combining 
        both extractive document retrieval with generative summarization. 
        
        ### Dataset
        This prototype uses [Internet-Only Manuals (IOMs) from CMS.gov](https://www.cms.gov/medicare/regulations-guidance/manuals/internet-only-manuals-ioms) 
    ''')
with cols[1]:
    st.image('app/images/ur_app_architecture.png', 'Reference Architecture Diagram', 380)

st.divider()
