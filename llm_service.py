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

import vertexai
from vertexai.generative_models import GenerativeModel
import vertexai.preview.generative_models as generative_models
import utils

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

vertexai.init(project=utils.PROJECT_ID, location=utils.LOCATION)

def generate_text(ctx: str, input: str) -> str:
    prompt = ctx + input
    model = GenerativeModel(utils.LLM)
    llm_responses = model.generate_content(prompt, generation_config=generation_config, safety_settings=safety_settings)
    
    partStr = str(llm_responses.candidates[0].content.parts[0])
    text = partStr[partStr.find('"') + 1 : partStr.rfind('"')]
    # print(text)
    return text

def generate_ur_prompt(pa_request: str) -> str:
    context = utils.UR_PROMPT_CTX
    ur_prompt = generate_text(context, pa_request)
    return ur_prompt

def generate_recommendation(ur_prompt: str) -> str:
    context = utils.UR_RECOMMENDATION_CTX
    ur_recommendation = generate_text(context, ur_prompt)
    return ur_recommendation

