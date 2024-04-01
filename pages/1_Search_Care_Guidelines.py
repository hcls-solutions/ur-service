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

import pandas as pd
import streamlit as st
from st_aggrid import GridOptionsBuilder, AgGrid, ColumnsAutoSizeMode

from search_service import generate_answer
import utils

st.set_page_config(
    page_title="Utilization Review Application",
    page_icon='app/images/logo.png',
    layout="wide",
)

cols = st.columns([10, 90])
with cols[0]:
    st.write('')
    st.image('app/images/logo.png', '', 64)
with cols[1]:
    st.title('Search Policies and Care Guidelines')
st.divider()

st.markdown('''Given a query, Enterprise Search will generate answer with citations and identify which text snippets are most relevant.''')

answer = ''
sources = []

question = st.text_input("Question: (E.g. Will Medicare require prior authorization for prescribing CGM to Type 1 diabetic patient?)", value="Ask your own question?")

if question != "Ask your own question?":
    result = generate_answer(question)
    answer = result["answer"]
    sources = result["sources"]

st.text_area("Summary Response: ", value=answer,)

st.divider()

df = pd.DataFrame(sources, columns=['title', 'gcs_uri', 'content'])
gb = GridOptionsBuilder.from_dataframe(df[['title']])
gb.configure_selection()
gb.configure_column('title', header_name="Citations: (click to expand)")
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
        st.markdown(f"**Title:** {selected_rows[0]['title']}")
        with st.expander(label=f"{st.session_state.value} Manual", expanded=False):
            st.session_state.value = "Hide"
            st.markdown(utils.show_pdf(selected_rows[0]['gcs_uri']), unsafe_allow_html=True)

        st.markdown('**Relevant Snippets**')
        for snippet in selected_rows[0]['content']:
            st.markdown(f'- {snippet}', unsafe_allow_html=True)

else:
    st.caption('No Citations')
