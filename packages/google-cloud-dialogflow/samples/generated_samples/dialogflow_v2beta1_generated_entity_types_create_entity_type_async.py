# -*- coding: utf-8 -*-
# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Generated code. DO NOT EDIT!
#
# Snippet for CreateEntityType
# NOTE: This snippet has been automatically generated for illustrative purposes only.
# It may require modifications to work in your environment.

# To install the latest published package dependency, execute the following:
#   python3 -m pip install google-cloud-dialogflow


# [START dialogflow_v2beta1_generated_EntityTypes_CreateEntityType_async]
# This snippet has been automatically generated and should be regarded as a
# code template only.
# It will require modifications to work:
# - It may require correct/in-range values for request initialization.
# - It may require specifying regional endpoints when creating the service
#   client as shown in:
#   https://googleapis.dev/python/google-api-core/latest/client_options.html
from google.cloud import dialogflow_v2beta1


async def sample_create_entity_type():
    # Create a client
    client = dialogflow_v2beta1.EntityTypesAsyncClient()

    # Initialize request argument(s)
    entity_type = dialogflow_v2beta1.EntityType()
    entity_type.display_name = "display_name_value"
    entity_type.kind = "KIND_REGEXP"

    request = dialogflow_v2beta1.CreateEntityTypeRequest(
        parent="parent_value",
        entity_type=entity_type,
    )

    # Make the request
    response = await client.create_entity_type(request=request)

    # Handle the response
    print(response)

# [END dialogflow_v2beta1_generated_EntityTypes_CreateEntityType_async]
