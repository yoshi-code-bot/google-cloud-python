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
from google.cloud.bigquery_datatransfer import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.bigquery_datatransfer_v1.services.data_transfer_service.async_client import (
    DataTransferServiceAsyncClient,
)
from google.cloud.bigquery_datatransfer_v1.services.data_transfer_service.client import (
    DataTransferServiceClient,
)
from google.cloud.bigquery_datatransfer_v1.types.datatransfer import (
    CheckValidCredsRequest,
    CheckValidCredsResponse,
    CreateTransferConfigRequest,
    DataSource,
    DataSourceParameter,
    DeleteTransferConfigRequest,
    DeleteTransferRunRequest,
    EnrollDataSourcesRequest,
    GetDataSourceRequest,
    GetTransferConfigRequest,
    GetTransferRunRequest,
    ListDataSourcesRequest,
    ListDataSourcesResponse,
    ListTransferConfigsRequest,
    ListTransferConfigsResponse,
    ListTransferLogsRequest,
    ListTransferLogsResponse,
    ListTransferRunsRequest,
    ListTransferRunsResponse,
    ScheduleTransferRunsRequest,
    ScheduleTransferRunsResponse,
    StartManualTransferRunsRequest,
    StartManualTransferRunsResponse,
    UnenrollDataSourcesRequest,
    UpdateTransferConfigRequest,
)
from google.cloud.bigquery_datatransfer_v1.types.transfer import (
    EmailPreferences,
    EncryptionConfiguration,
    EventDrivenSchedule,
    ManualSchedule,
    ScheduleOptions,
    ScheduleOptionsV2,
    TimeBasedSchedule,
    TransferConfig,
    TransferMessage,
    TransferRun,
    TransferState,
    TransferType,
    UserInfo,
)

__all__ = (
    "DataTransferServiceClient",
    "DataTransferServiceAsyncClient",
    "CheckValidCredsRequest",
    "CheckValidCredsResponse",
    "CreateTransferConfigRequest",
    "DataSource",
    "DataSourceParameter",
    "DeleteTransferConfigRequest",
    "DeleteTransferRunRequest",
    "EnrollDataSourcesRequest",
    "GetDataSourceRequest",
    "GetTransferConfigRequest",
    "GetTransferRunRequest",
    "ListDataSourcesRequest",
    "ListDataSourcesResponse",
    "ListTransferConfigsRequest",
    "ListTransferConfigsResponse",
    "ListTransferLogsRequest",
    "ListTransferLogsResponse",
    "ListTransferRunsRequest",
    "ListTransferRunsResponse",
    "ScheduleTransferRunsRequest",
    "ScheduleTransferRunsResponse",
    "StartManualTransferRunsRequest",
    "StartManualTransferRunsResponse",
    "UnenrollDataSourcesRequest",
    "UpdateTransferConfigRequest",
    "EmailPreferences",
    "EncryptionConfiguration",
    "EventDrivenSchedule",
    "ManualSchedule",
    "ScheduleOptions",
    "ScheduleOptionsV2",
    "TimeBasedSchedule",
    "TransferConfig",
    "TransferMessage",
    "TransferRun",
    "UserInfo",
    "TransferState",
    "TransferType",
)
