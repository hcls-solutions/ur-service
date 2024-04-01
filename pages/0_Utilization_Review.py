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

import streamlit as st

from db_service import get_pa_request_ids, get_pa_request
from llm_service import generate_ur_prompt, generate_recommendation

st.set_page_config(
    page_title = "Utilization Review Application",
    page_icon = 'app/images/logo.png',
    layout = "wide",
)

cols = st.columns([10, 90])
with cols[0]:
    st.write('')
    st.image('app/images/logo.png', '', 64)
with cols[1]:
    st.title('Utilization Review')
st.divider()

def reset():
    st.session_state.prompt = " "
    st.session_state.recommendation = " "

pa_request_ids = get_pa_request_ids()
cols = st.columns([20, 80])
with cols[0]:
    pa_request_id = st.selectbox("PA Requests", pa_request_ids, on_change=reset)
with cols[1]:
    if pa_request_id:
        pa_request = get_pa_request(pa_request_id)
        st.text_area(":blue[PA Request (JSON): ]", pa_request)

def render_prompt():
    prompt = generate_ur_prompt(pa_request=pa_request)
    st.session_state.prompt = prompt

st.button("Generate Prompt", on_click=render_prompt)
prompt = st.text_area(":blue[Review and Correct Prompt: ]", key = 'prompt')

def render_recommendation():
    prompt = st.session_state.prompt
    recommendation = generate_recommendation(prompt)
    st.session_state.recommendation = recommendation

st.button("Generate Recommendation", on_click=render_recommendation)
with st.container():
   st.write(":blue[Recommendation: ]")
   if 'recommendation' in st.session_state:
        if st.session_state.recommendation != " ":
            st.markdown(st.session_state.recommendation)