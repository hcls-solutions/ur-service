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

from __future__ import annotations

import streamlit as st # type: ignore
from google.protobuf.json_format import MessageToDict # type: ignore
import utils
from typing import List
from google.api_core.client_options import ClientOptions # type: ignore
from google.cloud import discoveryengine_v1 as discoveryengine


import logging
logging.basicConfig(level=logging.ERROR)

# TODO(developer): Uncomment these variables before running the sample.
project_id = utils.PROJECT_ID
location = utils.LOCATION          # Values: "global", "us", "eu"
engine_id = utils.SEARCH_APP_ID
search_query = " "


def execute_search(
    project_id: str,
    location: str,
    engine_id: str,
    search_query: str,
) -> List[discoveryengine.SearchResponse]:
    #  For more information, refer to:
    # https://cloud.google.com/generative-ai-app-builder/docs/locations#specify_a_multi-region_for_your_data_store
    client_options = (
        ClientOptions(api_endpoint=f"{location}-discoveryengine.googleapis.com")
        if location != "global"
        else None
    )

    # Create a client
    client = discoveryengine.SearchServiceClient(client_options=client_options)

    # The full resource name of the search app serving config
    serving_config = f"projects/{project_id}/locations/{location}/collections/default_collection/engines/{engine_id}/servingConfigs/default_config"

    # Optional: Configuration options for search
    # Refer to the `ContentSearchSpec` reference for all supported fields:
    # https://cloud.google.com/python/docs/reference/discoveryengine/latest/google.cloud.discoveryengine_v1.types.SearchRequest.ContentSearchSpec
    content_search_spec = discoveryengine.SearchRequest.ContentSearchSpec(
        # For information about snippets, refer to:
        # https://cloud.google.com/generative-ai-app-buxilder/docs/snippets
        snippet_spec=discoveryengine.SearchRequest.ContentSearchSpec.SnippetSpec(
            return_snippet=True
        ),
        # For information about search summaries, refer to:
        # https://cloud.google.com/generative-ai-app-builder/docs/get-search-summaries
        summary_spec=discoveryengine.SearchRequest.ContentSearchSpec.SummarySpec(
            summary_result_count=3,
            include_citations=True,
            ignore_adversarial_query=True,
            ignore_non_summary_seeking_query=True,
            model_prompt_spec=discoveryengine.SearchRequest.ContentSearchSpec.SummarySpec.ModelPromptSpec(
                preamble="YOUR_CUSTOM_PROMPT"
            ),
            model_spec=discoveryengine.SearchRequest.ContentSearchSpec.SummarySpec.ModelSpec(
                version="stable",
            ),
        ),
    )

    # Refer to the `SearchRequest` reference for all supported fields:
    # https://cloud.google.com/python/docs/reference/discoveryengine/latest/google.cloud.discoveryengine_v1.types.SearchRequest

    request = discoveryengine.SearchRequest(
        serving_config=serving_config,
        query=search_query,
        page_size=3,
        content_search_spec=content_search_spec,
        query_expansion_spec=discoveryengine.SearchRequest.QueryExpansionSpec(
            condition=discoveryengine.SearchRequest.QueryExpansionSpec.Condition.AUTO,
        ),
        spell_correction_spec=discoveryengine.SearchRequest.SpellCorrectionSpec(
            mode=discoveryengine.SearchRequest.SpellCorrectionSpec.Mode.AUTO
        )
    )

    response = client.search(request)
    logging.info(response)

    return response


def _get_sources(response: List) -> list[(str, list)]:
    """Parse ES response and generate list of tuples for sources"""
    sources = []
    for result in response.results:
        # doc_info = MessageToDict(result.document._pb)
        doc_info = MessageToDict(result.document.derived_struct_data)
        if (doc_info.get('snippets')):
            content = [snippet.get('snippet') for snippet in
                       doc_info.get('snippets', []) if
                       snippet.get('snippet') is not None]
            metadata = MessageToDict(result.document.derived_struct_data)
            sources.append((
                metadata["title"],
                # "title",
                metadata["link"],
                # "link",
                content))
    return sources


def generate_answer(query: str) -> dict:
    response = execute_search(
        project_id=utils.PROJECT_ID,
        location=utils.LOCATION,
        engine_id=utils.SEARCH_APP_ID,
        search_query=query)
    result = {}
    result['answer'] = response.summary.summary_text
    result['sources'] = _get_sources(response)
    logging.info(result['sources'])
    return result
