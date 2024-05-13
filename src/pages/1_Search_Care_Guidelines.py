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

import pandas as pd # type: ignore
import streamlit as st # type: ignore
from st_aggrid import GridOptionsBuilder, AgGrid, ColumnsAutoSizeMode # type: ignore
from ur.utils import show_pdf
from ur.search_service import generate_answer

import logging
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)


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
    st.title(":green[Search Policies and Care Guidelines]")
st.divider()

st.markdown('''### Given a query, Enterprise Search will generate answer with citations and identify which text snippets are most relevant.''')
cols = st.columns([55, 45])
with cols[0]:
    answer = ''
    sources = []

    st.markdown(":blue[Type a :orange[***question***] in the box below:]")
    question = st.text_input("Type a question: (E.g. Will Medicare require prior authorization for prescribing CGM to Type 1 diabetic patient?)", value=" ", label_visibility="collapsed")

    if question != " ":
        result = generate_answer(question)
        answer = result["answer"]
        sources = result["sources"]

    st.text_area("Summary Response: ", value=answer,)

    logger.info("####### ANSWER ######")
    logger.info(answer)
    logger.info("#####################")

    logger.info("####### SOURCES ######")
    logger.info(sources)
    logger.info("#####################")

    st.markdown(f"**Sources:** ")
    df = pd.DataFrame(sources, columns=['title', 'gcs_uri', 'content', 'url'])
    gb = GridOptionsBuilder.from_dataframe(df[['title', 'gcs_uri', 'content', 'url']])
    gb.configure_selection()
    gb.configure_column('title', header_name="Document Title: ")
    gb.configure_column('url', header_name="URL: ")
    gb.configure_column('content', header_name="Content: ")
    gb.configure_column('gcs_uri', header_name="Document URI: ")


    gridOptions = gb.build()


    if sources:
        data = AgGrid(
            df,
            height=150,
            gridOptions=gridOptions,
            columns_auto_size_mode=ColumnsAutoSizeMode.FIT_ALL_COLUMNS_TO_VIEW)

        selected_rows = data["selected_rows"] 

        st.session_state.value = "Display"

        def change_label():
            st.session_state.value = "Hide"

        if len(selected_rows) != 0:
            st.markdown(f"**Content:**")
            with st.container():
                content=selected_rows[0]['content']
                logging.info(content)
                for snippet in content:
                    st.markdown(f'- {snippet}', unsafe_allow_html=True)

            st.markdown(f"**Title:** {selected_rows[0]['title']}")
            with st.expander(label=f"{st.session_state.value} Manual", expanded=False):
                st.session_state.value = "Hide"
                st.markdown(show_pdf(selected_rows[0]['gcs_uri']), unsafe_allow_html=True)

    else:
        st.caption('None')

with cols[1]:
    st.markdown(":orange[***Sample Questions:***]")
    st.markdown('''              
        ``` 
            Will Medicare approve a request for hyperbaric oxygen (HBO) therapy? 
        ```
        ``` 
            Will Medicare approve CGM for patients with Type 2 diabetes? 
        ```
        ``` 
            What are Medicare guidelines for prescribing CGM? 
        ```
        ``` 
            What are Medicare guidelines for prescribing Ozempic? 
        ```
        ``` 
            Do I need prior authorization for deep anesthesia services for dental procedures? 
        ```  
                
        ``` 
            Does Medicare requires prior authorization for insulin pumps prescription? 
        ```  
    
        ``` 
            Does Medicare requires prior authorization for CGM Device? 
        ```  
    
        ``` 
            Does Medicare requires prior authorization for GLP Drugs? 
        ```  
    
        ``` 
            Will Medicare require prior authorization for prescribing CGM to Type 1 diabetic patient? 
        ``` 
                        
    ''')