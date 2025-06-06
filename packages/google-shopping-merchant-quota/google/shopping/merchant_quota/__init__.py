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
from google.shopping.merchant_quota import gapic_version as package_version

__version__ = package_version.__version__


from google.shopping.merchant_quota_v1beta.services.quota_service.async_client import (
    QuotaServiceAsyncClient,
)
from google.shopping.merchant_quota_v1beta.services.quota_service.client import (
    QuotaServiceClient,
)
from google.shopping.merchant_quota_v1beta.types.quota import (
    ListQuotaGroupsRequest,
    ListQuotaGroupsResponse,
    MethodDetails,
    QuotaGroup,
)

__all__ = (
    "QuotaServiceClient",
    "QuotaServiceAsyncClient",
    "ListQuotaGroupsRequest",
    "ListQuotaGroupsResponse",
    "MethodDetails",
    "QuotaGroup",
)
