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
# Snippet for UpdateDataExchange
# NOTE: This snippet has been automatically generated for illustrative purposes only.
# It may require modifications to work in your environment.

# To install the latest published package dependency, execute the following:
#   python3 -m pip install google-cloud-bigquery-data-exchange


# [START analyticshub_v1beta1_generated_AnalyticsHubService_UpdateDataExchange_sync]
# This snippet has been automatically generated and should be regarded as a
# code template only.
# It will require modifications to work:
# - It may require correct/in-range values for request initialization.
# - It may require specifying regional endpoints when creating the service
#   client as shown in:
#   https://googleapis.dev/python/google-api-core/latest/client_options.html
from google.cloud import bigquery_data_exchange_v1beta1


def sample_update_data_exchange():
    # Create a client
    client = bigquery_data_exchange_v1beta1.AnalyticsHubServiceClient()

    # Initialize request argument(s)
    data_exchange = bigquery_data_exchange_v1beta1.DataExchange()
    data_exchange.display_name = "display_name_value"

    request = bigquery_data_exchange_v1beta1.UpdateDataExchangeRequest(
        data_exchange=data_exchange,
    )

    # Make the request
    response = client.update_data_exchange(request=request)

    # Handle the response
    print(response)

# [END analyticshub_v1beta1_generated_AnalyticsHubService_UpdateDataExchange_sync]
