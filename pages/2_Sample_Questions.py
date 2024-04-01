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
    st.title('Sample Questions')
st.divider()
st.write("You can use these questions to search policies and care guidelines.")
st.markdown('''
    ### You may try the following questions:
    ``` Will Medicare approve a request for hyperbaric oxygen (HBO) therapy? ```  
    ``` Will Medicare approve a test for Infectious Agent Detection by Nucleic Acid? ```   
    ``` Will Medicare approve CGM for patients with Type 2 diabetes? ```               
    ``` What are Medicare guidelines for prescribing CGM? ```  
    ``` What are Medicare guidelines for prescribing Ozempic? ```          
    ``` Do I need prior authorization for deep anesthesia services for dental procedures? ```  
    ``` Does Medicare requires prior authorization for insulin pumps prescription? ```  
    ``` Does Medicare requires prior authorization for CGM Device? ```  
    ``` Does Medicare requires prior authorization for GLP Drugs? ```  
    ``` Will Medicare require prior authorization for prescribing CGM to Type 1 diabetic patient? ```  
''')  
