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
from .annotations import (
    AppPlatformCloudFunctionRequest,
    AppPlatformCloudFunctionResponse,
    AppPlatformEventBody,
    AppPlatformMetadata,
    ClassificationPredictionResult,
    ImageObjectDetectionPredictionResult,
    ImageSegmentationPredictionResult,
    NormalizedPolygon,
    NormalizedPolyline,
    NormalizedVertex,
    ObjectDetectionPredictionResult,
    OccupancyCountingPredictionResult,
    PersonalProtectiveEquipmentDetectionOutput,
    StreamAnnotation,
    StreamAnnotations,
    StreamAnnotationType,
    VideoActionRecognitionPredictionResult,
    VideoClassificationPredictionResult,
    VideoObjectTrackingPredictionResult,
)
from .common import Cluster, GcsSource, OperationMetadata
from .lva import AnalysisDefinition, AnalyzerDefinition, AttributeValue
from .lva_resources import Analysis
from .lva_service import (
    CreateAnalysisRequest,
    DeleteAnalysisRequest,
    GetAnalysisRequest,
    ListAnalysesRequest,
    ListAnalysesResponse,
    UpdateAnalysisRequest,
)
from .platform import (
    AcceleratorType,
    AddApplicationStreamInputRequest,
    AddApplicationStreamInputResponse,
    AIEnabledDevicesInputConfig,
    Application,
    ApplicationConfigs,
    ApplicationInstance,
    ApplicationNodeAnnotation,
    ApplicationStreamInput,
    AutoscalingMetricSpec,
    BigQueryConfig,
    CreateApplicationInstancesRequest,
    CreateApplicationInstancesResponse,
    CreateApplicationRequest,
    CreateDraftRequest,
    CreateProcessorRequest,
    CustomProcessorSourceInfo,
    DedicatedResources,
    DeleteApplicationInstancesRequest,
    DeleteApplicationInstancesResponse,
    DeleteApplicationRequest,
    DeleteDraftRequest,
    DeleteProcessorRequest,
    DeployApplicationRequest,
    DeployApplicationResponse,
    Draft,
    GeneralObjectDetectionConfig,
    GetApplicationRequest,
    GetDraftRequest,
    GetInstanceRequest,
    GetProcessorRequest,
    Instance,
    ListApplicationsRequest,
    ListApplicationsResponse,
    ListDraftsRequest,
    ListDraftsResponse,
    ListInstancesRequest,
    ListInstancesResponse,
    ListPrebuiltProcessorsRequest,
    ListPrebuiltProcessorsResponse,
    ListProcessorsRequest,
    ListProcessorsResponse,
    MachineSpec,
    MediaWarehouseConfig,
    ModelType,
    Node,
    OccupancyCountConfig,
    PersonalProtectiveEquipmentDetectionConfig,
    PersonBlurConfig,
    PersonVehicleDetectionConfig,
    Processor,
    ProcessorConfig,
    ProcessorIOSpec,
    RemoveApplicationStreamInputRequest,
    RemoveApplicationStreamInputResponse,
    ResourceAnnotations,
    StreamWithAnnotation,
    UndeployApplicationRequest,
    UndeployApplicationResponse,
    UpdateApplicationInstancesRequest,
    UpdateApplicationInstancesResponse,
    UpdateApplicationRequest,
    UpdateApplicationStreamInputRequest,
    UpdateApplicationStreamInputResponse,
    UpdateDraftRequest,
    UpdateProcessorRequest,
    VertexAutoMLVideoConfig,
    VertexAutoMLVisionConfig,
    VertexCustomConfig,
    VideoStreamInputConfig,
)
from .streaming_resources import (
    GstreamerBufferDescriptor,
    Packet,
    PacketHeader,
    PacketType,
    RawImageDescriptor,
    SeriesMetadata,
    ServerMetadata,
)
from .streaming_service import (
    AcquireLeaseRequest,
    CommitRequest,
    ControlledMode,
    EagerMode,
    EventUpdate,
    Lease,
    LeaseType,
    ReceiveEventsControlResponse,
    ReceiveEventsRequest,
    ReceiveEventsResponse,
    ReceivePacketsControlResponse,
    ReceivePacketsRequest,
    ReceivePacketsResponse,
    ReleaseLeaseRequest,
    ReleaseLeaseResponse,
    RenewLeaseRequest,
    RequestMetadata,
    SendPacketsRequest,
    SendPacketsResponse,
)
from .streams_resources import Channel, Event, Series, Stream
from .streams_service import (
    CreateClusterRequest,
    CreateEventRequest,
    CreateSeriesRequest,
    CreateStreamRequest,
    DeleteClusterRequest,
    DeleteEventRequest,
    DeleteSeriesRequest,
    DeleteStreamRequest,
    GenerateStreamHlsTokenRequest,
    GenerateStreamHlsTokenResponse,
    GetClusterRequest,
    GetEventRequest,
    GetSeriesRequest,
    GetStreamRequest,
    GetStreamThumbnailResponse,
    ListClustersRequest,
    ListClustersResponse,
    ListEventsRequest,
    ListEventsResponse,
    ListSeriesRequest,
    ListSeriesResponse,
    ListStreamsRequest,
    ListStreamsResponse,
    MaterializeChannelRequest,
    UpdateClusterRequest,
    UpdateEventRequest,
    UpdateSeriesRequest,
    UpdateStreamRequest,
)
from .warehouse import (
    Annotation,
    AnnotationMatchingResult,
    AnnotationValue,
    Asset,
    BoolValue,
    CircleArea,
    ClipAssetRequest,
    ClipAssetResponse,
    Corpus,
    CreateAnnotationRequest,
    CreateAssetRequest,
    CreateCorpusMetadata,
    CreateCorpusRequest,
    CreateDataSchemaRequest,
    CreateSearchConfigRequest,
    Criteria,
    DataSchema,
    DataSchemaDetails,
    DateTimeRange,
    DateTimeRangeArray,
    DeleteAnnotationRequest,
    DeleteAssetMetadata,
    DeleteAssetRequest,
    DeleteCorpusRequest,
    DeleteDataSchemaRequest,
    DeleteSearchConfigRequest,
    FacetBucket,
    FacetBucketType,
    FacetGroup,
    FacetProperty,
    FacetValue,
    FloatRange,
    FloatRangeArray,
    GenerateHlsUriRequest,
    GenerateHlsUriResponse,
    GeoCoordinate,
    GeoLocationArray,
    GetAnnotationRequest,
    GetAssetRequest,
    GetCorpusRequest,
    GetDataSchemaRequest,
    GetSearchConfigRequest,
    IngestAssetRequest,
    IngestAssetResponse,
    IntRange,
    IntRangeArray,
    ListAnnotationsRequest,
    ListAnnotationsResponse,
    ListAssetsRequest,
    ListAssetsResponse,
    ListCorporaRequest,
    ListCorporaResponse,
    ListDataSchemasRequest,
    ListDataSchemasResponse,
    ListSearchConfigsRequest,
    ListSearchConfigsResponse,
    Partition,
    SearchAssetsRequest,
    SearchAssetsResponse,
    SearchConfig,
    SearchCriteriaProperty,
    SearchResultItem,
    StringArray,
    UpdateAnnotationRequest,
    UpdateAssetRequest,
    UpdateCorpusRequest,
    UpdateDataSchemaRequest,
    UpdateSearchConfigRequest,
    UserSpecifiedAnnotation,
)

__all__ = (
    "AppPlatformCloudFunctionRequest",
    "AppPlatformCloudFunctionResponse",
    "AppPlatformEventBody",
    "AppPlatformMetadata",
    "ClassificationPredictionResult",
    "ImageObjectDetectionPredictionResult",
    "ImageSegmentationPredictionResult",
    "NormalizedPolygon",
    "NormalizedPolyline",
    "NormalizedVertex",
    "ObjectDetectionPredictionResult",
    "OccupancyCountingPredictionResult",
    "PersonalProtectiveEquipmentDetectionOutput",
    "StreamAnnotation",
    "StreamAnnotations",
    "VideoActionRecognitionPredictionResult",
    "VideoClassificationPredictionResult",
    "VideoObjectTrackingPredictionResult",
    "StreamAnnotationType",
    "Cluster",
    "GcsSource",
    "OperationMetadata",
    "AnalysisDefinition",
    "AnalyzerDefinition",
    "AttributeValue",
    "Analysis",
    "CreateAnalysisRequest",
    "DeleteAnalysisRequest",
    "GetAnalysisRequest",
    "ListAnalysesRequest",
    "ListAnalysesResponse",
    "UpdateAnalysisRequest",
    "AddApplicationStreamInputRequest",
    "AddApplicationStreamInputResponse",
    "AIEnabledDevicesInputConfig",
    "Application",
    "ApplicationConfigs",
    "ApplicationInstance",
    "ApplicationNodeAnnotation",
    "ApplicationStreamInput",
    "AutoscalingMetricSpec",
    "BigQueryConfig",
    "CreateApplicationInstancesRequest",
    "CreateApplicationInstancesResponse",
    "CreateApplicationRequest",
    "CreateDraftRequest",
    "CreateProcessorRequest",
    "CustomProcessorSourceInfo",
    "DedicatedResources",
    "DeleteApplicationInstancesRequest",
    "DeleteApplicationInstancesResponse",
    "DeleteApplicationRequest",
    "DeleteDraftRequest",
    "DeleteProcessorRequest",
    "DeployApplicationRequest",
    "DeployApplicationResponse",
    "Draft",
    "GeneralObjectDetectionConfig",
    "GetApplicationRequest",
    "GetDraftRequest",
    "GetInstanceRequest",
    "GetProcessorRequest",
    "Instance",
    "ListApplicationsRequest",
    "ListApplicationsResponse",
    "ListDraftsRequest",
    "ListDraftsResponse",
    "ListInstancesRequest",
    "ListInstancesResponse",
    "ListPrebuiltProcessorsRequest",
    "ListPrebuiltProcessorsResponse",
    "ListProcessorsRequest",
    "ListProcessorsResponse",
    "MachineSpec",
    "MediaWarehouseConfig",
    "Node",
    "OccupancyCountConfig",
    "PersonalProtectiveEquipmentDetectionConfig",
    "PersonBlurConfig",
    "PersonVehicleDetectionConfig",
    "Processor",
    "ProcessorConfig",
    "ProcessorIOSpec",
    "RemoveApplicationStreamInputRequest",
    "RemoveApplicationStreamInputResponse",
    "ResourceAnnotations",
    "StreamWithAnnotation",
    "UndeployApplicationRequest",
    "UndeployApplicationResponse",
    "UpdateApplicationInstancesRequest",
    "UpdateApplicationInstancesResponse",
    "UpdateApplicationRequest",
    "UpdateApplicationStreamInputRequest",
    "UpdateApplicationStreamInputResponse",
    "UpdateDraftRequest",
    "UpdateProcessorRequest",
    "VertexAutoMLVideoConfig",
    "VertexAutoMLVisionConfig",
    "VertexCustomConfig",
    "VideoStreamInputConfig",
    "AcceleratorType",
    "ModelType",
    "GstreamerBufferDescriptor",
    "Packet",
    "PacketHeader",
    "PacketType",
    "RawImageDescriptor",
    "SeriesMetadata",
    "ServerMetadata",
    "AcquireLeaseRequest",
    "CommitRequest",
    "ControlledMode",
    "EagerMode",
    "EventUpdate",
    "Lease",
    "ReceiveEventsControlResponse",
    "ReceiveEventsRequest",
    "ReceiveEventsResponse",
    "ReceivePacketsControlResponse",
    "ReceivePacketsRequest",
    "ReceivePacketsResponse",
    "ReleaseLeaseRequest",
    "ReleaseLeaseResponse",
    "RenewLeaseRequest",
    "RequestMetadata",
    "SendPacketsRequest",
    "SendPacketsResponse",
    "LeaseType",
    "Channel",
    "Event",
    "Series",
    "Stream",
    "CreateClusterRequest",
    "CreateEventRequest",
    "CreateSeriesRequest",
    "CreateStreamRequest",
    "DeleteClusterRequest",
    "DeleteEventRequest",
    "DeleteSeriesRequest",
    "DeleteStreamRequest",
    "GenerateStreamHlsTokenRequest",
    "GenerateStreamHlsTokenResponse",
    "GetClusterRequest",
    "GetEventRequest",
    "GetSeriesRequest",
    "GetStreamRequest",
    "GetStreamThumbnailResponse",
    "ListClustersRequest",
    "ListClustersResponse",
    "ListEventsRequest",
    "ListEventsResponse",
    "ListSeriesRequest",
    "ListSeriesResponse",
    "ListStreamsRequest",
    "ListStreamsResponse",
    "MaterializeChannelRequest",
    "UpdateClusterRequest",
    "UpdateEventRequest",
    "UpdateSeriesRequest",
    "UpdateStreamRequest",
    "Annotation",
    "AnnotationMatchingResult",
    "AnnotationValue",
    "Asset",
    "BoolValue",
    "CircleArea",
    "ClipAssetRequest",
    "ClipAssetResponse",
    "Corpus",
    "CreateAnnotationRequest",
    "CreateAssetRequest",
    "CreateCorpusMetadata",
    "CreateCorpusRequest",
    "CreateDataSchemaRequest",
    "CreateSearchConfigRequest",
    "Criteria",
    "DataSchema",
    "DataSchemaDetails",
    "DateTimeRange",
    "DateTimeRangeArray",
    "DeleteAnnotationRequest",
    "DeleteAssetMetadata",
    "DeleteAssetRequest",
    "DeleteCorpusRequest",
    "DeleteDataSchemaRequest",
    "DeleteSearchConfigRequest",
    "FacetBucket",
    "FacetGroup",
    "FacetProperty",
    "FacetValue",
    "FloatRange",
    "FloatRangeArray",
    "GenerateHlsUriRequest",
    "GenerateHlsUriResponse",
    "GeoCoordinate",
    "GeoLocationArray",
    "GetAnnotationRequest",
    "GetAssetRequest",
    "GetCorpusRequest",
    "GetDataSchemaRequest",
    "GetSearchConfigRequest",
    "IngestAssetRequest",
    "IngestAssetResponse",
    "IntRange",
    "IntRangeArray",
    "ListAnnotationsRequest",
    "ListAnnotationsResponse",
    "ListAssetsRequest",
    "ListAssetsResponse",
    "ListCorporaRequest",
    "ListCorporaResponse",
    "ListDataSchemasRequest",
    "ListDataSchemasResponse",
    "ListSearchConfigsRequest",
    "ListSearchConfigsResponse",
    "Partition",
    "SearchAssetsRequest",
    "SearchAssetsResponse",
    "SearchConfig",
    "SearchCriteriaProperty",
    "SearchResultItem",
    "StringArray",
    "UpdateAnnotationRequest",
    "UpdateAssetRequest",
    "UpdateCorpusRequest",
    "UpdateDataSchemaRequest",
    "UpdateSearchConfigRequest",
    "UserSpecifiedAnnotation",
    "FacetBucketType",
)
