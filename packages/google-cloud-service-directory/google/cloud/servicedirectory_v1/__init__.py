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
from google.cloud.servicedirectory_v1 import gapic_version as package_version

__version__ = package_version.__version__


from .services.lookup_service import LookupServiceAsyncClient, LookupServiceClient
from .services.registration_service import (
    RegistrationServiceAsyncClient,
    RegistrationServiceClient,
)
from .types.endpoint import Endpoint
from .types.lookup_service import ResolveServiceRequest, ResolveServiceResponse
from .types.namespace import Namespace
from .types.registration_service import (
    CreateEndpointRequest,
    CreateNamespaceRequest,
    CreateServiceRequest,
    DeleteEndpointRequest,
    DeleteNamespaceRequest,
    DeleteServiceRequest,
    GetEndpointRequest,
    GetNamespaceRequest,
    GetServiceRequest,
    ListEndpointsRequest,
    ListEndpointsResponse,
    ListNamespacesRequest,
    ListNamespacesResponse,
    ListServicesRequest,
    ListServicesResponse,
    UpdateEndpointRequest,
    UpdateNamespaceRequest,
    UpdateServiceRequest,
)
from .types.service import Service

__all__ = (
    "LookupServiceAsyncClient",
    "RegistrationServiceAsyncClient",
    "CreateEndpointRequest",
    "CreateNamespaceRequest",
    "CreateServiceRequest",
    "DeleteEndpointRequest",
    "DeleteNamespaceRequest",
    "DeleteServiceRequest",
    "Endpoint",
    "GetEndpointRequest",
    "GetNamespaceRequest",
    "GetServiceRequest",
    "ListEndpointsRequest",
    "ListEndpointsResponse",
    "ListNamespacesRequest",
    "ListNamespacesResponse",
    "ListServicesRequest",
    "ListServicesResponse",
    "LookupServiceClient",
    "Namespace",
    "RegistrationServiceClient",
    "ResolveServiceRequest",
    "ResolveServiceResponse",
    "Service",
    "UpdateEndpointRequest",
    "UpdateNamespaceRequest",
    "UpdateServiceRequest",
)
