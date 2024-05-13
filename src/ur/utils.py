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

import base64
import os
import re

from google.cloud import storage

import logging
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

LOCATION = os.environ['LOCATION']
PROJECT_ID = os.environ['GOOGLE_CLOUD_PROJECT']
SEARCH_DATASTORE_ID = os.environ['SEARCH_DATASTORE_ID']
SEARCH_APP_ID = os.environ['SEARCH_APP_ID']

LLM_LOCATION = os.environ['LLM_LOCATION']
LLM = os.environ['LLM']

UR_PROMPT_CTX = """Transform prior authorization requests from JSON format to plain text:
Output template: Review a prior authorization request for {service.type}, {service.description (service.code)}  
for our member, {patient.patient_name}, who is {patient.patient_age} years old, {patient.patient_gender} with 
{current_condition.description}. The Patient is on {current_treatment.description}, and has been diagnosed with 
{diagnosis.description (diagnosis.code)}. Current labs: {labs.1.name} is {labs.1.value}, {labs.2.name} is 
{labs.2.value}, {labs.3.name} is {labs.3.value}, and {labs.4.name} is {labs.4.value}.

input: {\"request_id\":\"000000000\",\"patient\":{\"patient_age\":\"11\",\"patient_id\":\"50005055\",\"patient_gender\":\"Male\",\"patient_name\":\"Razy Joy\"},\"current_treatment\":{\"description\":\"NovoLog® Mix 70/30, 5 units before breakfast + 5 units before dinner\"},\"provider\":{\"phone\":\"555-710-8066\",\"name\":\"Judy Jones\",\"id\":\"9999999999\",\"address\":\"985 Beta Court\"},\"labs\":[{\"name\":\"A1C\",\"value\":\"6.1%\"},{\"name\":\"Weight\",\"value\":\"210 lb.\"},{\"name\":\"Height\",\"value\":\"5 ft.\"}],\"service\":{\"type\":\"MEDICATION\",\"code\":\" \",\"description\":\"12-week supply of Ozempic, 0.5 mg per week\"},\"diagnosis\":{\"code\":\" \",\"description\":\"Type 1 diabetes\"},\"current_condition\":{\"description\":\"Type 1 diabetes\",\"name\":\"Type 1 diabetes\"}}
output: Review a prior authorization request for a MEDICATION, 12-week supply of Ozempic, 0.5 mg per week for our member, Razy Joy, who is 11 years old, male with Type 1 diabetes. The Patient is on NovoLog® Mix 70/30, 5 units before breakfast + 5 units before dinner and has been diagnosed with Type 1 diabetes. Current labs: A1C is 6.1%, Weight is 210 lb, and Height is 5 ft.
input: {\"diagnosis\":{\"description\":\"Type 2 diabetes\",\"code\":\"E11.618\"},\"service\":{\"code\":\"95249, 95250, and 95251\",\"type\":\"DEVICE\",\"description\":\"180-day supply of Dexcom transmitters and sensors\"},\"patient\":{\"patient_age\":\"75\",\"patient_gender\":\"Male\",\"patient_id\":\"111223232\",\"patient_name\":\"Tom Sharp\"},\"labs\":[{\"value\":\"9.4\",\"name\":\"A1C\"},{\"name\":\"Glucose\",\"value\":\"196\"}],\"current_condition\":{\"description\":\"Type 2 diabetes\",\"name\":\"Diabetes\"},\"current_treatment\":{\"description\":\"2000 mg of Metformin and 25 mg of Jardiance daily for several months.\"},\"request_id\":\"111111111\",\"provider\":{\"phone\":\"555-111-2222\",\"name\":\"Dr. Harry\",\"address\":\"123 Dork St\",\"id\":\"1237653\"}}
output: Review a prior authorization request for a DEVICE, 180-day supply of Dexcom transmitters and sensors (95249, 95250, and 95251) for our member, Tom Sharp, who is 75 years old, male with Type 2 diabetes. The Patient is on 2000 mg of Metformin and 25 mg of Jardiance daily for several months and has been diagnosed with Type 2 diabetes. Current labs: A1C is 9.4% and Glucose is 196.
input: {\"labs\":[{\"name\":\"A1C\",\"value\":\"5.0\"},{\"name\":\"Glucose\",\"value\":\"99\"},{\"name\":\"Weight\",\"value\":\"120 lb\"},{\"name\":\"Height\",\"value\":\"5 ft 3 inches\"}],\"current_condition\":{\"name\":\"Normal\",\"description\":\"Occasional heartburns.\"},\"request_id\":\"222222222\",\"current_treatment\":{\"description\":\"Exercise 30 min. daily.\"},\"provider\":{\"id\":\"1023555349\",\"address\":\"123 Kamp St\",\"name\":\"Romer Nelson\",\"phone\":\"555-111-5555\"},\"patient\":{\"patient_id\":\"723223232\",\"patient_gender\":\"Female\",\"patient_age\":\"45\",\"patient_name\":\"Alyssa Baker\"},\"service\":{\"description\":\"Infectious agent detection by nucleic acid\",\"type\":\"SERVICE\",\"code\":\"U0003,87635\"},\"diagnosis\":{\"description\":\"Epigastric pain, Dehydration\",\"code\":\"R10.13, E86.0\"}}
output: Review a prior authorization request for a SERVICE, Infectious agent detection by nucleic acid (U0003,87635) for our member, Alyssa Baker, who is 45 years old, female with Epigastric pain, Dehydration and Normal. The Patient is on Exercise 30 min. daily and has been diagnosed with Epigastric pain, Dehydration. Current labs: A1C is 5.0, Glucose is 99, Weight is 120 lb., and Height is 5 ft 3 inches.
"""

UR_RECOMMENDATION_CTX = """Cymbal Healthcare delivers all types of medical care to patients. 
Cymbal Insurance, a Medicare Administrative Contractor, offers Medicare Advantage (MA) health plans.  
Cymbal Healthcare has a contractual agreement with Cymbal Insurance to provide medical care to the members of Cymbal Insurance. 

Cymbal Healthcare requires prior authorization from Cymbal Insurance for delivering certain types of medical care. 
Cymbal Healthcare sends letters and patient medical documents to obtain authorization from Cymbal Insurance. 
Cymbal Insurance MA plan provides authorization based on medical necessity guidelines/criteria defined in the 
National Coverage Determination (NCD)by the CMS. 

Cymbal Insurance reviews prior authorization requests against the NCD medical necessity guidelines/criteria and communicates the 
decisions to Cymbal Healthcare with references to applicable policies and guidelines. 

Review the following request and generate a recommendation for the staff of Cymbal Insurance. 
Include whether they can unconditionally approve it, approve with some conditions, or potentially deny it because of the unmet criteria. 
Provide rationale and citations. 
Elaborate on the reasons and add citations to the documents in the datastore.
Do not make things up. 

input: Review a prior authorization request for a 180-day supply of Dexcom
transmitters and sensors for our member, Tom Sharp, who is 75 years old
with Type 2 diabetes. His last A1C lab result is 9.5%. He has been taking
2000 mg of Metformin and 25 mg of Jardiance daily for several months. 

output: Prior Authorization Recommendation: Approve
The patient has uncontrolled diabetes despite being on the maximum dose of metformin and Jardiance. 
The patient's A1C level is 9.5%. The NCD medical necessity guidelines for CGMs state that CGMs 
are covered for patients with type 2 diabetes who have an A1C level of '7.0%' or higher despite 
treatment with metformin and a sulfonylurea or metformin and a DPP-4 inhibitor.
Therefore, prior authorization for Dexcom transmitters and sensors should be approved.

input: Review a prior authorization request for a 90-day supply of the Omnipod DASH 
pods for a patient, Razy Joy, a member of Cymbal Insurance, 11 years old, with Type 1 diabetes.
His A1C lab result is 6.1%. He takes NovoLog® Mix 70/30, 5 units before breakfast + 5 units 
before dinner.

output: Prior Authorization Recommendation: Approve
The patient has type 1 diabetes and is on insulin therapy. The NCD medical necessity guidelines 
for insulin pumps state that insulin pumps are covered for patients with type 1 diabetes
who are on insulin therapy and have an A1C level of '7.0%' or higher. The patient's A1C level 
is 6.1%, which is below the threshold of 7.0%. However, the NCD also states that insulin pumps 
may be covered for patients with type 1 diabetes who have an A1C level below '7.0%' if they have 
other medical conditions that make it difficult to control their diabetes with insulin injections. 
The patient is 11 years old, which is a young age to be managing diabetes with insulin injections.
Therefore, prior authorization for the Omnipod DASH pods should be approved.

input: Review a prior authorization request for a 12-week supply of Ozempic, 0.5 mg per week, for 
a Cymbal Insurance member, Razy Joy, 11 years old, with Type 1 diabetes. His A1C lab result is 6.1%.
He takes NovoLog® Mix 70/30, 5 units before breakfast + 5 units before dinner.

output: Prior Authorization Recommendation: Deny
The patient has type 1 diabetes and is taking NovoLog® Mix 70/30, 5 units before breakfast + 
5 units before dinner. His A1C level is 6.1%, which is within the target range for people with 
diabetes. Ozempic is not indicated for the treatment of type 1 diabetes. It is indicated for
the treatment of type 2 diabetes. Therefore, prior authorization for Ozempic should be denied.

input: Review a prior authorization request for a 90-day supply of the Omnipod DASH pods for our 
member, Sanjy Smart, who is 26 years old with a condition of obesity. Her last A1/C lab result
is 5.4%. She is 5 feet and weighs 210 lb.

output: Prior Authorization Recommendation: Deny
The patient does not meet the medical necessity criteria for an insulin pump. The patient's
A1C level is 5.4%, which is within the normal range. The patient is also not taking insulin. 
Therefore, an insulin pump is not medically necessary for this patient."""

def show_pdf(uri: str) -> str:
    """Given gs:// uri, return html code to embed pdf in iframe"""
    pdf_file = download_from_gcs(uri)
    base64_pdf = base64.b64encode(pdf_file).decode('utf-8')
    pdf_iframe = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="800" height="800" type="application/pdf"></iframe>'
    return pdf_iframe

def download_from_gcs(uri: str) -> bytes:
    """Given gs:// uri, download file"""
    client = storage.Client()
    matches = re.search(r'gs://(.*?)/(.*)', uri)
    bucket_name, object_name = matches.group(1), matches.group(2)
    blob = client.bucket(bucket_name).blob(object_name)
    return blob.download_as_string()