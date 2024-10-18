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
from st_aggrid.shared import JsCode # type: ignore
from ur.utils import show_pdf
from ur.list_docs_in_search_ds import list_docs

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
    st.title(":green[Policies And Care Guidelines]")
st.divider()
st.markdown('''-Below are all the documents uploaded to Enterprise Search for this demo.''')  

cols = st.columns([50, 40])

with cols[0]:
    df = pd.DataFrame(list_docs())
    gb = GridOptionsBuilder.from_dataframe(df[['gcs_uri']], editable=True)
    gb.configure_column('id', header_name="Document ID", width=100)
    # gb.configure_column('name', header_name="Document Name")
    gb.configure_selection()
    gb.configure_column('gcs_uri', header_name="Select a document to browse", width=200)
    gb.configure_selection()
    # gb.configure_column('url', header_name="URL")
    # cell_renderer =  JsCode("""
    #         class UrlCellRenderer {
    #         init(params) {
    #             this.eGui = document.createElement('a');
    #             this.eGui.innerText = 'Open';
    #             this.eGui.setAttribute('href', params.value);
    #             this.eGui.setAttribute('style', "text-decoration:none");
    #             this.eGui.setAttribute('target', "_blank");
    #         }
    #         getGui() {
    #             return this.eGui;
    #         }
    #         }
    #     """)
    gb.configure_column("url",
        headerName="Link",
        # cellRenderer=cell_renderer,
        width=30)
    gb.configure_pagination()
    gridOptions = gb.build()

    data = AgGrid(
        df,
        gridOptions=gridOptions,
        columns_auto_size_mode=ColumnsAutoSizeMode.FIT_ALL_COLUMNS_TO_VIEW, allow_unsafe_jscode=True)

with cols[1]:
    selected_rows = data["selected_rows"]
    # print(selected_rows)
    if selected_rows is not None and len(selected_rows) != 0: 
        selected_row = selected_rows.iloc[0] 
        # print(selected_row)
        url = selected_row.url      
        gcs_uri = selected_row.gcs_uri
        if gcs_uri.endswith('.txt'):
            st.write(url)
        else:    
            st.write(gcs_uri)
            st.write(show_pdf(gcs_uri), unsafe_allow_html=True)
    
