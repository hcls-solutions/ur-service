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
import pandas as pd
from st_aggrid import GridOptionsBuilder, AgGrid, ColumnsAutoSizeMode

from search_service import get_corpus
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
    st.title('Browse Policies And Care Guidelines')
st.divider()
st.markdown('''-Below are all the documents uploaded to Enterprise Search for this demo.''')  

col1, col2 = st.columns(2)

with col1:
    df = pd.DataFrame(get_corpus())
    gb = GridOptionsBuilder.from_dataframe(df[['gcs_uri']])
    # gb.configure_column('id', header_name="Document ID")
    gb.configure_selection()
    gb.configure_column('gcs_uri', header_name="Select a document to browse")

    gb.configure_pagination()
    gridOptions = gb.build()

    data = AgGrid(
        df,
        gridOptions=gridOptions,
        columns_auto_size_mode=ColumnsAutoSizeMode.FIT_ALL_COLUMNS_TO_VIEW)

with col2:
    selected_rows = data["selected_rows"]

    if len(selected_rows) != 0:
        st.write(selected_rows[0]['gcs_uri'])
        st.write(utils.show_pdf(selected_rows[0]['gcs_uri']), unsafe_allow_html=True)
        

    
