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
from google.cloud.dialogflowcx_v3 import gapic_version as package_version

__version__ = package_version.__version__


from .services.agents import AgentsAsyncClient, AgentsClient
from .services.changelogs import ChangelogsAsyncClient, ChangelogsClient
from .services.deployments import DeploymentsAsyncClient, DeploymentsClient
from .services.entity_types import EntityTypesAsyncClient, EntityTypesClient
from .services.environments import EnvironmentsAsyncClient, EnvironmentsClient
from .services.experiments import ExperimentsAsyncClient, ExperimentsClient
from .services.flows import FlowsAsyncClient, FlowsClient
from .services.generators import GeneratorsAsyncClient, GeneratorsClient
from .services.intents import IntentsAsyncClient, IntentsClient
from .services.pages import PagesAsyncClient, PagesClient
from .services.security_settings_service import (
    SecuritySettingsServiceAsyncClient,
    SecuritySettingsServiceClient,
)
from .services.session_entity_types import (
    SessionEntityTypesAsyncClient,
    SessionEntityTypesClient,
)
from .services.sessions import SessionsAsyncClient, SessionsClient
from .services.test_cases import TestCasesAsyncClient, TestCasesClient
from .services.transition_route_groups import (
    TransitionRouteGroupsAsyncClient,
    TransitionRouteGroupsClient,
)
from .services.versions import VersionsAsyncClient, VersionsClient
from .services.webhooks import WebhooksAsyncClient, WebhooksClient
from .types.advanced_settings import AdvancedSettings
from .types.agent import (
    Agent,
    AgentValidationResult,
    CreateAgentRequest,
    DeleteAgentRequest,
    ExportAgentRequest,
    ExportAgentResponse,
    GetAgentRequest,
    GetAgentValidationResultRequest,
    GetGenerativeSettingsRequest,
    ListAgentsRequest,
    ListAgentsResponse,
    RestoreAgentRequest,
    SpeechToTextSettings,
    UpdateAgentRequest,
    UpdateGenerativeSettingsRequest,
    ValidateAgentRequest,
)
from .types.audio_config import (
    AudioEncoding,
    BargeInConfig,
    InputAudioConfig,
    OutputAudioConfig,
    OutputAudioEncoding,
    SpeechModelVariant,
    SpeechWordInfo,
    SsmlVoiceGender,
    SynthesizeSpeechConfig,
    TextToSpeechSettings,
    VoiceSelectionParams,
)
from .types.changelog import (
    Changelog,
    GetChangelogRequest,
    ListChangelogsRequest,
    ListChangelogsResponse,
)
from .types.data_store_connection import (
    DataStoreConnection,
    DataStoreConnectionSignals,
    DataStoreType,
    DocumentProcessingMode,
)
from .types.deployment import (
    Deployment,
    GetDeploymentRequest,
    ListDeploymentsRequest,
    ListDeploymentsResponse,
)
from .types.entity_type import (
    CreateEntityTypeRequest,
    DeleteEntityTypeRequest,
    EntityType,
    ExportEntityTypesMetadata,
    ExportEntityTypesRequest,
    ExportEntityTypesResponse,
    GetEntityTypeRequest,
    ImportEntityTypesMetadata,
    ImportEntityTypesRequest,
    ImportEntityTypesResponse,
    ListEntityTypesRequest,
    ListEntityTypesResponse,
    UpdateEntityTypeRequest,
)
from .types.environment import (
    ContinuousTestResult,
    CreateEnvironmentRequest,
    DeleteEnvironmentRequest,
    DeployFlowMetadata,
    DeployFlowRequest,
    DeployFlowResponse,
    Environment,
    GetEnvironmentRequest,
    ListContinuousTestResultsRequest,
    ListContinuousTestResultsResponse,
    ListEnvironmentsRequest,
    ListEnvironmentsResponse,
    LookupEnvironmentHistoryRequest,
    LookupEnvironmentHistoryResponse,
    RunContinuousTestMetadata,
    RunContinuousTestRequest,
    RunContinuousTestResponse,
    UpdateEnvironmentRequest,
)
from .types.experiment import (
    CreateExperimentRequest,
    DeleteExperimentRequest,
    Experiment,
    GetExperimentRequest,
    ListExperimentsRequest,
    ListExperimentsResponse,
    RolloutConfig,
    RolloutState,
    StartExperimentRequest,
    StopExperimentRequest,
    UpdateExperimentRequest,
    VariantsHistory,
    VersionVariants,
)
from .types.flow import (
    CreateFlowRequest,
    DeleteFlowRequest,
    ExportFlowRequest,
    ExportFlowResponse,
    Flow,
    FlowImportStrategy,
    FlowValidationResult,
    GetFlowRequest,
    GetFlowValidationResultRequest,
    ImportFlowRequest,
    ImportFlowResponse,
    ListFlowsRequest,
    ListFlowsResponse,
    NluSettings,
    TrainFlowRequest,
    UpdateFlowRequest,
    ValidateFlowRequest,
)
from .types.fulfillment import Fulfillment
from .types.gcs import GcsDestination
from .types.generative_settings import GenerativeSettings
from .types.generator import (
    CreateGeneratorRequest,
    DeleteGeneratorRequest,
    Generator,
    GetGeneratorRequest,
    ListGeneratorsRequest,
    ListGeneratorsResponse,
    Phrase,
    UpdateGeneratorRequest,
)
from .types.import_strategy import ImportStrategy
from .types.inline import InlineDestination, InlineSource
from .types.intent import (
    CreateIntentRequest,
    DeleteIntentRequest,
    ExportIntentsMetadata,
    ExportIntentsRequest,
    ExportIntentsResponse,
    GetIntentRequest,
    ImportIntentsMetadata,
    ImportIntentsRequest,
    ImportIntentsResponse,
    Intent,
    IntentView,
    ListIntentsRequest,
    ListIntentsResponse,
    UpdateIntentRequest,
)
from .types.page import (
    CreatePageRequest,
    DeletePageRequest,
    EventHandler,
    Form,
    GetPageRequest,
    KnowledgeConnectorSettings,
    ListPagesRequest,
    ListPagesResponse,
    Page,
    TransitionRoute,
    UpdatePageRequest,
)
from .types.response_message import ResponseMessage
from .types.safety_settings import SafetySettings
from .types.security_settings import (
    CreateSecuritySettingsRequest,
    DeleteSecuritySettingsRequest,
    GetSecuritySettingsRequest,
    ListSecuritySettingsRequest,
    ListSecuritySettingsResponse,
    SecuritySettings,
    UpdateSecuritySettingsRequest,
)
from .types.session import (
    AnswerFeedback,
    AudioInput,
    BoostSpec,
    BoostSpecs,
    CloudConversationDebuggingInfo,
    DetectIntentRequest,
    DetectIntentResponse,
    DtmfInput,
    EventInput,
    FilterSpecs,
    FulfillIntentRequest,
    FulfillIntentResponse,
    IntentInput,
    Match,
    MatchIntentRequest,
    MatchIntentResponse,
    QueryInput,
    QueryParameters,
    QueryResult,
    SearchConfig,
    SentimentAnalysisResult,
    StreamingDetectIntentRequest,
    StreamingDetectIntentResponse,
    StreamingRecognitionResult,
    SubmitAnswerFeedbackRequest,
    TextInput,
)
from .types.session_entity_type import (
    CreateSessionEntityTypeRequest,
    DeleteSessionEntityTypeRequest,
    GetSessionEntityTypeRequest,
    ListSessionEntityTypesRequest,
    ListSessionEntityTypesResponse,
    SessionEntityType,
    UpdateSessionEntityTypeRequest,
)
from .types.test_case import (
    BatchDeleteTestCasesRequest,
    BatchRunTestCasesMetadata,
    BatchRunTestCasesRequest,
    BatchRunTestCasesResponse,
    CalculateCoverageRequest,
    CalculateCoverageResponse,
    ConversationTurn,
    CreateTestCaseRequest,
    ExportTestCasesMetadata,
    ExportTestCasesRequest,
    ExportTestCasesResponse,
    GetTestCaseRequest,
    GetTestCaseResultRequest,
    ImportTestCasesMetadata,
    ImportTestCasesRequest,
    ImportTestCasesResponse,
    IntentCoverage,
    ListTestCaseResultsRequest,
    ListTestCaseResultsResponse,
    ListTestCasesRequest,
    ListTestCasesResponse,
    RunTestCaseMetadata,
    RunTestCaseRequest,
    RunTestCaseResponse,
    TestCase,
    TestCaseError,
    TestCaseResult,
    TestConfig,
    TestError,
    TestResult,
    TestRunDifference,
    TransitionCoverage,
    TransitionRouteGroupCoverage,
    UpdateTestCaseRequest,
)
from .types.transition_route_group import (
    CreateTransitionRouteGroupRequest,
    DeleteTransitionRouteGroupRequest,
    GetTransitionRouteGroupRequest,
    ListTransitionRouteGroupsRequest,
    ListTransitionRouteGroupsResponse,
    TransitionRouteGroup,
    UpdateTransitionRouteGroupRequest,
)
from .types.validation_message import ResourceName, ValidationMessage
from .types.version import (
    CompareVersionsRequest,
    CompareVersionsResponse,
    CreateVersionOperationMetadata,
    CreateVersionRequest,
    DeleteVersionRequest,
    GetVersionRequest,
    ListVersionsRequest,
    ListVersionsResponse,
    LoadVersionRequest,
    UpdateVersionRequest,
    Version,
)
from .types.webhook import (
    CreateWebhookRequest,
    DeleteWebhookRequest,
    GetWebhookRequest,
    LanguageInfo,
    ListWebhooksRequest,
    ListWebhooksResponse,
    PageInfo,
    SessionInfo,
    UpdateWebhookRequest,
    Webhook,
    WebhookRequest,
    WebhookResponse,
)

__all__ = (
    "AgentsAsyncClient",
    "ChangelogsAsyncClient",
    "DeploymentsAsyncClient",
    "EntityTypesAsyncClient",
    "EnvironmentsAsyncClient",
    "ExperimentsAsyncClient",
    "FlowsAsyncClient",
    "GeneratorsAsyncClient",
    "IntentsAsyncClient",
    "PagesAsyncClient",
    "SecuritySettingsServiceAsyncClient",
    "SessionEntityTypesAsyncClient",
    "SessionsAsyncClient",
    "TestCasesAsyncClient",
    "TransitionRouteGroupsAsyncClient",
    "VersionsAsyncClient",
    "WebhooksAsyncClient",
    "AdvancedSettings",
    "Agent",
    "AgentValidationResult",
    "AgentsClient",
    "AnswerFeedback",
    "AudioEncoding",
    "AudioInput",
    "BargeInConfig",
    "BatchDeleteTestCasesRequest",
    "BatchRunTestCasesMetadata",
    "BatchRunTestCasesRequest",
    "BatchRunTestCasesResponse",
    "BoostSpec",
    "BoostSpecs",
    "CalculateCoverageRequest",
    "CalculateCoverageResponse",
    "Changelog",
    "ChangelogsClient",
    "CloudConversationDebuggingInfo",
    "CompareVersionsRequest",
    "CompareVersionsResponse",
    "ContinuousTestResult",
    "ConversationTurn",
    "CreateAgentRequest",
    "CreateEntityTypeRequest",
    "CreateEnvironmentRequest",
    "CreateExperimentRequest",
    "CreateFlowRequest",
    "CreateGeneratorRequest",
    "CreateIntentRequest",
    "CreatePageRequest",
    "CreateSecuritySettingsRequest",
    "CreateSessionEntityTypeRequest",
    "CreateTestCaseRequest",
    "CreateTransitionRouteGroupRequest",
    "CreateVersionOperationMetadata",
    "CreateVersionRequest",
    "CreateWebhookRequest",
    "DataStoreConnection",
    "DataStoreConnectionSignals",
    "DataStoreType",
    "DeleteAgentRequest",
    "DeleteEntityTypeRequest",
    "DeleteEnvironmentRequest",
    "DeleteExperimentRequest",
    "DeleteFlowRequest",
    "DeleteGeneratorRequest",
    "DeleteIntentRequest",
    "DeletePageRequest",
    "DeleteSecuritySettingsRequest",
    "DeleteSessionEntityTypeRequest",
    "DeleteTransitionRouteGroupRequest",
    "DeleteVersionRequest",
    "DeleteWebhookRequest",
    "DeployFlowMetadata",
    "DeployFlowRequest",
    "DeployFlowResponse",
    "Deployment",
    "DeploymentsClient",
    "DetectIntentRequest",
    "DetectIntentResponse",
    "DocumentProcessingMode",
    "DtmfInput",
    "EntityType",
    "EntityTypesClient",
    "Environment",
    "EnvironmentsClient",
    "EventHandler",
    "EventInput",
    "Experiment",
    "ExperimentsClient",
    "ExportAgentRequest",
    "ExportAgentResponse",
    "ExportEntityTypesMetadata",
    "ExportEntityTypesRequest",
    "ExportEntityTypesResponse",
    "ExportFlowRequest",
    "ExportFlowResponse",
    "ExportIntentsMetadata",
    "ExportIntentsRequest",
    "ExportIntentsResponse",
    "ExportTestCasesMetadata",
    "ExportTestCasesRequest",
    "ExportTestCasesResponse",
    "FilterSpecs",
    "Flow",
    "FlowImportStrategy",
    "FlowValidationResult",
    "FlowsClient",
    "Form",
    "FulfillIntentRequest",
    "FulfillIntentResponse",
    "Fulfillment",
    "GcsDestination",
    "GenerativeSettings",
    "Generator",
    "GeneratorsClient",
    "GetAgentRequest",
    "GetAgentValidationResultRequest",
    "GetChangelogRequest",
    "GetDeploymentRequest",
    "GetEntityTypeRequest",
    "GetEnvironmentRequest",
    "GetExperimentRequest",
    "GetFlowRequest",
    "GetFlowValidationResultRequest",
    "GetGenerativeSettingsRequest",
    "GetGeneratorRequest",
    "GetIntentRequest",
    "GetPageRequest",
    "GetSecuritySettingsRequest",
    "GetSessionEntityTypeRequest",
    "GetTestCaseRequest",
    "GetTestCaseResultRequest",
    "GetTransitionRouteGroupRequest",
    "GetVersionRequest",
    "GetWebhookRequest",
    "ImportEntityTypesMetadata",
    "ImportEntityTypesRequest",
    "ImportEntityTypesResponse",
    "ImportFlowRequest",
    "ImportFlowResponse",
    "ImportIntentsMetadata",
    "ImportIntentsRequest",
    "ImportIntentsResponse",
    "ImportStrategy",
    "ImportTestCasesMetadata",
    "ImportTestCasesRequest",
    "ImportTestCasesResponse",
    "InlineDestination",
    "InlineSource",
    "InputAudioConfig",
    "Intent",
    "IntentCoverage",
    "IntentInput",
    "IntentView",
    "IntentsClient",
    "KnowledgeConnectorSettings",
    "LanguageInfo",
    "ListAgentsRequest",
    "ListAgentsResponse",
    "ListChangelogsRequest",
    "ListChangelogsResponse",
    "ListContinuousTestResultsRequest",
    "ListContinuousTestResultsResponse",
    "ListDeploymentsRequest",
    "ListDeploymentsResponse",
    "ListEntityTypesRequest",
    "ListEntityTypesResponse",
    "ListEnvironmentsRequest",
    "ListEnvironmentsResponse",
    "ListExperimentsRequest",
    "ListExperimentsResponse",
    "ListFlowsRequest",
    "ListFlowsResponse",
    "ListGeneratorsRequest",
    "ListGeneratorsResponse",
    "ListIntentsRequest",
    "ListIntentsResponse",
    "ListPagesRequest",
    "ListPagesResponse",
    "ListSecuritySettingsRequest",
    "ListSecuritySettingsResponse",
    "ListSessionEntityTypesRequest",
    "ListSessionEntityTypesResponse",
    "ListTestCaseResultsRequest",
    "ListTestCaseResultsResponse",
    "ListTestCasesRequest",
    "ListTestCasesResponse",
    "ListTransitionRouteGroupsRequest",
    "ListTransitionRouteGroupsResponse",
    "ListVersionsRequest",
    "ListVersionsResponse",
    "ListWebhooksRequest",
    "ListWebhooksResponse",
    "LoadVersionRequest",
    "LookupEnvironmentHistoryRequest",
    "LookupEnvironmentHistoryResponse",
    "Match",
    "MatchIntentRequest",
    "MatchIntentResponse",
    "NluSettings",
    "OutputAudioConfig",
    "OutputAudioEncoding",
    "Page",
    "PageInfo",
    "PagesClient",
    "Phrase",
    "QueryInput",
    "QueryParameters",
    "QueryResult",
    "ResourceName",
    "ResponseMessage",
    "RestoreAgentRequest",
    "RolloutConfig",
    "RolloutState",
    "RunContinuousTestMetadata",
    "RunContinuousTestRequest",
    "RunContinuousTestResponse",
    "RunTestCaseMetadata",
    "RunTestCaseRequest",
    "RunTestCaseResponse",
    "SafetySettings",
    "SearchConfig",
    "SecuritySettings",
    "SecuritySettingsServiceClient",
    "SentimentAnalysisResult",
    "SessionEntityType",
    "SessionEntityTypesClient",
    "SessionInfo",
    "SessionsClient",
    "SpeechModelVariant",
    "SpeechToTextSettings",
    "SpeechWordInfo",
    "SsmlVoiceGender",
    "StartExperimentRequest",
    "StopExperimentRequest",
    "StreamingDetectIntentRequest",
    "StreamingDetectIntentResponse",
    "StreamingRecognitionResult",
    "SubmitAnswerFeedbackRequest",
    "SynthesizeSpeechConfig",
    "TestCase",
    "TestCaseError",
    "TestCaseResult",
    "TestCasesClient",
    "TestConfig",
    "TestError",
    "TestResult",
    "TestRunDifference",
    "TextInput",
    "TextToSpeechSettings",
    "TrainFlowRequest",
    "TransitionCoverage",
    "TransitionRoute",
    "TransitionRouteGroup",
    "TransitionRouteGroupCoverage",
    "TransitionRouteGroupsClient",
    "UpdateAgentRequest",
    "UpdateEntityTypeRequest",
    "UpdateEnvironmentRequest",
    "UpdateExperimentRequest",
    "UpdateFlowRequest",
    "UpdateGenerativeSettingsRequest",
    "UpdateGeneratorRequest",
    "UpdateIntentRequest",
    "UpdatePageRequest",
    "UpdateSecuritySettingsRequest",
    "UpdateSessionEntityTypeRequest",
    "UpdateTestCaseRequest",
    "UpdateTransitionRouteGroupRequest",
    "UpdateVersionRequest",
    "UpdateWebhookRequest",
    "ValidateAgentRequest",
    "ValidateFlowRequest",
    "ValidationMessage",
    "VariantsHistory",
    "Version",
    "VersionVariants",
    "VersionsClient",
    "VoiceSelectionParams",
    "Webhook",
    "WebhookRequest",
    "WebhookResponse",
    "WebhooksClient",
)
