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
# Snippet for DeleteProductInput
# NOTE: This snippet has been automatically generated for illustrative purposes only.
# It may require modifications to work in your environment.

# To install the latest published package dependency, execute the following:
#   python3 -m pip install google-shopping-merchant-products


# [START merchantapi_v1beta_generated_ProductInputsService_DeleteProductInput_async]
# This snippet has been automatically generated and should be regarded as a
# code template only.
# It will require modifications to work:
# - It may require correct/in-range values for request initialization.
# - It may require specifying regional endpoints when creating the service
#   client as shown in:
#   https://googleapis.dev/python/google-api-core/latest/client_options.html
from google.shopping import merchant_products_v1beta


async def sample_delete_product_input():
    # Create a client
    client = merchant_products_v1beta.ProductInputsServiceAsyncClient()

    # Initialize request argument(s)
    request = merchant_products_v1beta.DeleteProductInputRequest(
        name="name_value",
        data_source="data_source_value",
    )

    # Make the request
    await client.delete_product_input(request=request)


# [END merchantapi_v1beta_generated_ProductInputsService_DeleteProductInput_async]
