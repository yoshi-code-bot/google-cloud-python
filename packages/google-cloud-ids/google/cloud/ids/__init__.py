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
from google.cloud.ids import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.ids_v1.services.ids.async_client import IDSAsyncClient
from google.cloud.ids_v1.services.ids.client import IDSClient
from google.cloud.ids_v1.types.ids import (
    CreateEndpointRequest,
    DeleteEndpointRequest,
    Endpoint,
    GetEndpointRequest,
    ListEndpointsRequest,
    ListEndpointsResponse,
    OperationMetadata,
)

__all__ = (
    "IDSClient",
    "IDSAsyncClient",
    "CreateEndpointRequest",
    "DeleteEndpointRequest",
    "Endpoint",
    "GetEndpointRequest",
    "ListEndpointsRequest",
    "ListEndpointsResponse",
    "OperationMetadata",
)
