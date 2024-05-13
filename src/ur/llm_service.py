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

import vertexai # type: ignore
from vertexai.generative_models import GenerativeModel # type: ignore
from vertexai.preview.generative_models import Tool, grounding # type: ignore
import vertexai.preview.generative_models as generative_models # type: ignore
from ur.utils import PROJECT_ID, LLM_LOCATION, LLM, LOCATION, SEARCH_DATASTORE_ID, UR_PROMPT_CTX, UR_RECOMMENDATION_CTX

import logging
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

generation_config = {
    "max_output_tokens": 2048,
    "temperature": 1,
    "top_p": 1,
}

safety_settings = {
    generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
}

vertexai.init(project=PROJECT_ID, location=LLM_LOCATION)


def generate_text(ctx: str, input: str) -> str:
    prompt = ctx + input
    model = GenerativeModel(LLM)
    datastore = f"projects/"+PROJECT_ID+"/locations/"+LOCATION+"/collections/default_collection/dataStores/"+SEARCH_DATASTORE_ID
    tool1 = Tool.from_retrieval(
        grounding.Retrieval(grounding.VertexAISearch(datastore=datastore))
    )    
    llm_responses = model.generate_content(prompt, generation_config=generation_config, safety_settings=safety_settings, tools=[tool1])
    
    partStr = str(llm_responses.candidates[0].content.parts[0])
    text = partStr[partStr.find('"') + 1 : partStr.rfind('"')]
    logging.info("----------LLM output-------------")
    logging.info(text)
    return text

def generate_ur_prompt(pa_request: str) -> str:
    context = UR_PROMPT_CTX
    ur_prompt = generate_text(context, pa_request)
    return ur_prompt

def generate_recommendation(ur_prompt: str) -> str:
    context = UR_RECOMMENDATION_CTX
    ur_recommendation = generate_text(context, ur_prompt)
    return ur_recommendation

