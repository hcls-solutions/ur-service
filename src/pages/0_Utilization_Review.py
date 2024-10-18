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
import re
from st_aggrid import GridOptionsBuilder, AgGrid, ColumnsAutoSizeMode # type: ignore
import pandas as pd  # type: ignore
from ur.db_service import get_pa_requests, get_pa_request
from ur.llm_service import generate_ur_prompt, generate_recommendation

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

st.set_page_config(
    page_title = "Utilization Review",
    page_icon = 'app/images/logo.png',
    layout = "wide",
)

cols = st.columns([10, 90])
with cols[0]:
    st.write('')
    st.image('app/images/logo.png', '', 64)
with cols[1]:
    st.header(":green[Simplify Utilization Review: 3 Easy Steps]")

st.markdown(
    """
    <style>
    textarea {
        font-family: 'Google Sans'; font-size: 16px !important;
    }
    input {
        font-family: 'Google Sans'; font-size: 16px !important;
    }
    select {
        font-size: 14px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)
PROMPT_ALERT = "Select a PA request (a row from the table above) and press the button: 'Generate Prompt'."
REC_ALERT = "Generate or type a prompt in the text area above and press the button: 'Generate Recommendation'."
def init_prompt():
    st.session_state.prompt = PROMPT_ALERT

def init_recommendation():
    st.session_state.recommendation = REC_ALERT


def set_recommendation():
    prompt = st.session_state.prompt
    if PROMPT_ALERT == prompt or "" == prompt: 
        recommendation = REC_ALERT
    else:    
        recommendation = generate_recommendation(prompt)
    init_recommendation()
    st.session_state.recommendation = recommendation
    logger.info("--------------PROMPT----------------")
    logger.info(prompt)
    logger.info("-----------RECOMMENDATION-----------")
    logger.info(recommendation)

def render_recommendation():
    with st.container():
        if "recommendation" in st.session_state:
            recommendation = st.session_state.recommendation
            if REC_ALERT == recommendation:
                st.write(":red["+REC_ALERT+"]")            
            else:
                logger.info("------------RECOMMENDATION-------------")
                logger.info(recommendation)
                out = recommendation.replace('\\n', '  \n  ')
                st.markdown(out)
                # st.text_area(":blue[Recommendation]", key = 'recommendation', height=230, label_visibility="collapsed")
             

def set_prompt(pa_request_id):
    pa_request = get_pa_request(pa_request_id)
    prompt = generate_ur_prompt(pa_request=pa_request)
    logger.info("--------------PROMPT----------------")
    logger.info(prompt)
    out = prompt.replace('\\n', '  \n  ')
    init_prompt()
    st.session_state.prompt = out

def render_prompt():
    st.markdown(":blue[2. Review and correct the :orange[***system generated prompt***]:]")
    st.text_area(":blue[2. Review and correct the system generated prompt: ]", key = 'prompt', height=130, label_visibility="collapsed")

    st.markdown(":blue[3. Press :orange[Generate Recommendation] button to generate UR recommendation.]")
    st.form_submit_button(":orange[Generate Recommendation]", on_click=set_recommendation, use_container_width=True)   

def render_pa_requests_container():
    pa_requests = get_pa_requests()
    logger.info("------------------ pa_requests ----------------")
    logger.info(pa_requests)
    logger.info("-----------------------------------------------")
    df = pd.json_normalize(pa_requests, max_level=2)
    with st.form("pa_request_form"):
        st.markdown(":blue[1. Select the :orange[***Prior authorization(PA) request***] below and press Generate Prompt button to generate UR Prompt.]")
        gb = GridOptionsBuilder.from_dataframe(df[['request_id', 'patient.patient_name', 'service.description', 'service.code', 'diagnosis.description', 'diagnosis.code','current_condition.name', 'provider.name']])
        gb.configure_selection()
        gb.configure_column('request_id', header_name="Request ID: ")
        gb.configure_column('patient.patient_name', header_name="Patient Name: ")
        gb.configure_column('service.description', header_name="Service: ")
        gb.configure_column('service.code', header_name="CPT Codes: ")
        gb.configure_column('diagnosis.description', header_name="Diagnosis: ") 
        gb.configure_column('diagnosis.code', header_name="Diagnosis Codes: ")       
        gb.configure_column('current_condition.name', header_name="Current conditions: ")
        gb.configure_column('provider.name', header_name="Provider Name: ")        
        gridOptions = gb.build()
        
        if pa_requests:
            data = AgGrid(
                df,
                height=250,
                gridOptions=gridOptions,
                columns_auto_size_mode=ColumnsAutoSizeMode.FIT_ALL_COLUMNS_TO_VIEW)
        
        prompt_button = st.form_submit_button(":orange[Generate Prompt]", use_container_width=True)

        if prompt_button:
            selected_rows = data["selected_rows"]
            # print(selected_rows)
            if selected_rows is not None and len(selected_rows) != 0: 
                selected_row = selected_rows.iloc[0] 
                # print(selected_row)
                if len(selected_row) != 0:
                    pa_request_id = selected_row.request_id
                    logger.info("------------- Request ID ----------")
                    logger.info(pa_request_id)
                    logger.info("-----------------------------------")
                    set_prompt(pa_request_id)
                    init_recommendation()
                else:
                    st.session_state.prompt = PROMPT_ALERT
                    st.session_state.recommendation = REC_ALERT    
            else:
                st.session_state.prompt = PROMPT_ALERT 
        render_prompt()
        render_recommendation()        

render_pa_requests_container()


