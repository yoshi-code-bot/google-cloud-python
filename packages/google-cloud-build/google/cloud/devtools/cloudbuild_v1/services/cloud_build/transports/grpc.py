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
import json
import logging as std_logging
import pickle
from typing import Callable, Dict, Optional, Sequence, Tuple, Union
import warnings

from google.api_core import gapic_v1, grpc_helpers, operations_v1
import google.auth  # type: ignore
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.longrunning import operations_pb2  # type: ignore
from google.protobuf import empty_pb2  # type: ignore
from google.protobuf.json_format import MessageToJson
import google.protobuf.message
import grpc  # type: ignore
import proto  # type: ignore

from google.cloud.devtools.cloudbuild_v1.types import cloudbuild

from .base import DEFAULT_CLIENT_INFO, CloudBuildTransport

try:
    from google.api_core import client_logging  # type: ignore

    CLIENT_LOGGING_SUPPORTED = True  # pragma: NO COVER
except ImportError:  # pragma: NO COVER
    CLIENT_LOGGING_SUPPORTED = False

_LOGGER = std_logging.getLogger(__name__)


class _LoggingClientInterceptor(grpc.UnaryUnaryClientInterceptor):  # pragma: NO COVER
    def intercept_unary_unary(self, continuation, client_call_details, request):
        logging_enabled = CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
            std_logging.DEBUG
        )
        if logging_enabled:  # pragma: NO COVER
            request_metadata = client_call_details.metadata
            if isinstance(request, proto.Message):
                request_payload = type(request).to_json(request)
            elif isinstance(request, google.protobuf.message.Message):
                request_payload = MessageToJson(request)
            else:
                request_payload = f"{type(request).__name__}: {pickle.dumps(request)}"

            request_metadata = {
                key: value.decode("utf-8") if isinstance(value, bytes) else value
                for key, value in request_metadata
            }
            grpc_request = {
                "payload": request_payload,
                "requestMethod": "grpc",
                "metadata": dict(request_metadata),
            }
            _LOGGER.debug(
                f"Sending request for {client_call_details.method}",
                extra={
                    "serviceName": "google.devtools.cloudbuild.v1.CloudBuild",
                    "rpcName": str(client_call_details.method),
                    "request": grpc_request,
                    "metadata": grpc_request["metadata"],
                },
            )
        response = continuation(client_call_details, request)
        if logging_enabled:  # pragma: NO COVER
            response_metadata = response.trailing_metadata()
            # Convert gRPC metadata `<class 'grpc.aio._metadata.Metadata'>` to list of tuples
            metadata = (
                dict([(k, str(v)) for k, v in response_metadata])
                if response_metadata
                else None
            )
            result = response.result()
            if isinstance(result, proto.Message):
                response_payload = type(result).to_json(result)
            elif isinstance(result, google.protobuf.message.Message):
                response_payload = MessageToJson(result)
            else:
                response_payload = f"{type(result).__name__}: {pickle.dumps(result)}"
            grpc_response = {
                "payload": response_payload,
                "metadata": metadata,
                "status": "OK",
            }
            _LOGGER.debug(
                f"Received response for {client_call_details.method}.",
                extra={
                    "serviceName": "google.devtools.cloudbuild.v1.CloudBuild",
                    "rpcName": client_call_details.method,
                    "response": grpc_response,
                    "metadata": grpc_response["metadata"],
                },
            )
        return response


class CloudBuildGrpcTransport(CloudBuildTransport):
    """gRPC backend transport for CloudBuild.

    Creates and manages builds on Google Cloud Platform.

    The main concept used by this API is a ``Build``, which describes
    the location of the source to build, how to build the source, and
    where to store the built artifacts, if any.

    A user can list previously-requested builds or get builds by their
    ID to determine the status of the build.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends protocol buffers over the wire using gRPC (which is built on
    top of HTTP/2); the ``grpcio`` package must be installed.
    """

    _stubs: Dict[str, Callable]

    def __init__(
        self,
        *,
        host: str = "cloudbuild.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        channel: Optional[Union[grpc.Channel, Callable[..., grpc.Channel]]] = None,
        api_mtls_endpoint: Optional[str] = None,
        client_cert_source: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        ssl_channel_credentials: Optional[grpc.ChannelCredentials] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'cloudbuild.googleapis.com').
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
                This argument is ignored if a ``channel`` instance is provided.
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is ignored if a ``channel`` instance is provided.
            scopes (Optional(Sequence[str])): A list of scopes. This argument is
                ignored if a ``channel`` instance is provided.
            channel (Optional[Union[grpc.Channel, Callable[..., grpc.Channel]]]):
                A ``Channel`` instance through which to make calls, or a Callable
                that constructs and returns one. If set to None, ``self.create_channel``
                is used to create the channel. If a Callable is given, it will be called
                with the same arguments as used in ``self.create_channel``.
            api_mtls_endpoint (Optional[str]): Deprecated. The mutual TLS endpoint.
                If provided, it overrides the ``host`` argument and tries to create
                a mutual TLS channel with client SSL credentials from
                ``client_cert_source`` or application default SSL credentials.
            client_cert_source (Optional[Callable[[], Tuple[bytes, bytes]]]):
                Deprecated. A callback to provide client SSL certificate bytes and
                private key bytes, both in PEM format. It is ignored if
                ``api_mtls_endpoint`` is None.
            ssl_channel_credentials (grpc.ChannelCredentials): SSL credentials
                for the grpc channel. It is ignored if a ``channel`` instance is provided.
            client_cert_source_for_mtls (Optional[Callable[[], Tuple[bytes, bytes]]]):
                A callback to provide client certificate bytes and private key bytes,
                both in PEM format. It is used to configure a mutual TLS channel. It is
                ignored if a ``channel`` instance or ``ssl_channel_credentials`` is provided.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.
            always_use_jwt_access (Optional[bool]): Whether self signed JWT should
                be used for service account credentials.

        Raises:
          google.auth.exceptions.MutualTLSChannelError: If mutual TLS transport
              creation failed for any reason.
          google.api_core.exceptions.DuplicateCredentialArgs: If both ``credentials``
              and ``credentials_file`` are passed.
        """
        self._grpc_channel = None
        self._ssl_channel_credentials = ssl_channel_credentials
        self._stubs: Dict[str, Callable] = {}
        self._operations_client: Optional[operations_v1.OperationsClient] = None

        if api_mtls_endpoint:
            warnings.warn("api_mtls_endpoint is deprecated", DeprecationWarning)
        if client_cert_source:
            warnings.warn("client_cert_source is deprecated", DeprecationWarning)

        if isinstance(channel, grpc.Channel):
            # Ignore credentials if a channel was passed.
            credentials = None
            self._ignore_credentials = True
            # If a channel was explicitly provided, set it.
            self._grpc_channel = channel
            self._ssl_channel_credentials = None

        else:
            if api_mtls_endpoint:
                host = api_mtls_endpoint

                # Create SSL credentials with client_cert_source or application
                # default SSL credentials.
                if client_cert_source:
                    cert, key = client_cert_source()
                    self._ssl_channel_credentials = grpc.ssl_channel_credentials(
                        certificate_chain=cert, private_key=key
                    )
                else:
                    self._ssl_channel_credentials = SslCredentials().ssl_credentials

            else:
                if client_cert_source_for_mtls and not ssl_channel_credentials:
                    cert, key = client_cert_source_for_mtls()
                    self._ssl_channel_credentials = grpc.ssl_channel_credentials(
                        certificate_chain=cert, private_key=key
                    )

        # The base transport sets the host, credentials and scopes
        super().__init__(
            host=host,
            credentials=credentials,
            credentials_file=credentials_file,
            scopes=scopes,
            quota_project_id=quota_project_id,
            client_info=client_info,
            always_use_jwt_access=always_use_jwt_access,
            api_audience=api_audience,
        )

        if not self._grpc_channel:
            # initialize with the provided callable or the default channel
            channel_init = channel or type(self).create_channel
            self._grpc_channel = channel_init(
                self._host,
                # use the credentials which are saved
                credentials=self._credentials,
                # Set ``credentials_file`` to ``None`` here as
                # the credentials that we saved earlier should be used.
                credentials_file=None,
                scopes=self._scopes,
                ssl_credentials=self._ssl_channel_credentials,
                quota_project_id=quota_project_id,
                options=[
                    ("grpc.max_send_message_length", -1),
                    ("grpc.max_receive_message_length", -1),
                ],
            )

        self._interceptor = _LoggingClientInterceptor()
        self._logged_channel = grpc.intercept_channel(
            self._grpc_channel, self._interceptor
        )

        # Wrap messages. This must be done after self._logged_channel exists
        self._prep_wrapped_messages(client_info)

    @classmethod
    def create_channel(
        cls,
        host: str = "cloudbuild.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        quota_project_id: Optional[str] = None,
        **kwargs,
    ) -> grpc.Channel:
        """Create and return a gRPC channel object.
        Args:
            host (Optional[str]): The host for the channel to use.
            credentials (Optional[~.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If
                none are specified, the client will attempt to ascertain
                the credentials from the environment.
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is mutually exclusive with credentials.
            scopes (Optional[Sequence[str]]): A optional list of scopes needed for this
                service. These are only used when credentials are not specified and
                are passed to :func:`google.auth.default`.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            kwargs (Optional[dict]): Keyword arguments, which are passed to the
                channel creation.
        Returns:
            grpc.Channel: A gRPC channel object.

        Raises:
            google.api_core.exceptions.DuplicateCredentialArgs: If both ``credentials``
              and ``credentials_file`` are passed.
        """

        return grpc_helpers.create_channel(
            host,
            credentials=credentials,
            credentials_file=credentials_file,
            quota_project_id=quota_project_id,
            default_scopes=cls.AUTH_SCOPES,
            scopes=scopes,
            default_host=cls.DEFAULT_HOST,
            **kwargs,
        )

    @property
    def grpc_channel(self) -> grpc.Channel:
        """Return the channel designed to connect to this service."""
        return self._grpc_channel

    @property
    def operations_client(self) -> operations_v1.OperationsClient:
        """Create the client designed to process long-running operations.

        This property caches on the instance; repeated calls return the same
        client.
        """
        # Quick check: Only create a new client if we do not already have one.
        if self._operations_client is None:
            self._operations_client = operations_v1.OperationsClient(
                self._logged_channel
            )

        # Return the client from cache.
        return self._operations_client

    @property
    def create_build(
        self,
    ) -> Callable[[cloudbuild.CreateBuildRequest], operations_pb2.Operation]:
        r"""Return a callable for the create build method over gRPC.

        Starts a build with the specified configuration.

        This method returns a long-running ``Operation``, which includes
        the build ID. Pass the build ID to ``GetBuild`` to determine the
        build status (such as ``SUCCESS`` or ``FAILURE``).

        Returns:
            Callable[[~.CreateBuildRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_build" not in self._stubs:
            self._stubs["create_build"] = self._logged_channel.unary_unary(
                "/google.devtools.cloudbuild.v1.CloudBuild/CreateBuild",
                request_serializer=cloudbuild.CreateBuildRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["create_build"]

    @property
    def get_build(self) -> Callable[[cloudbuild.GetBuildRequest], cloudbuild.Build]:
        r"""Return a callable for the get build method over gRPC.

        Returns information about a previously requested build.

        The ``Build`` that is returned includes its status (such as
        ``SUCCESS``, ``FAILURE``, or ``WORKING``), and timing
        information.

        Returns:
            Callable[[~.GetBuildRequest],
                    ~.Build]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_build" not in self._stubs:
            self._stubs["get_build"] = self._logged_channel.unary_unary(
                "/google.devtools.cloudbuild.v1.CloudBuild/GetBuild",
                request_serializer=cloudbuild.GetBuildRequest.serialize,
                response_deserializer=cloudbuild.Build.deserialize,
            )
        return self._stubs["get_build"]

    @property
    def list_builds(
        self,
    ) -> Callable[[cloudbuild.ListBuildsRequest], cloudbuild.ListBuildsResponse]:
        r"""Return a callable for the list builds method over gRPC.

        Lists previously requested builds.

        Previously requested builds may still be in-progress, or
        may have finished successfully or unsuccessfully.

        Returns:
            Callable[[~.ListBuildsRequest],
                    ~.ListBuildsResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_builds" not in self._stubs:
            self._stubs["list_builds"] = self._logged_channel.unary_unary(
                "/google.devtools.cloudbuild.v1.CloudBuild/ListBuilds",
                request_serializer=cloudbuild.ListBuildsRequest.serialize,
                response_deserializer=cloudbuild.ListBuildsResponse.deserialize,
            )
        return self._stubs["list_builds"]

    @property
    def cancel_build(
        self,
    ) -> Callable[[cloudbuild.CancelBuildRequest], cloudbuild.Build]:
        r"""Return a callable for the cancel build method over gRPC.

        Cancels a build in progress.

        Returns:
            Callable[[~.CancelBuildRequest],
                    ~.Build]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "cancel_build" not in self._stubs:
            self._stubs["cancel_build"] = self._logged_channel.unary_unary(
                "/google.devtools.cloudbuild.v1.CloudBuild/CancelBuild",
                request_serializer=cloudbuild.CancelBuildRequest.serialize,
                response_deserializer=cloudbuild.Build.deserialize,
            )
        return self._stubs["cancel_build"]

    @property
    def retry_build(
        self,
    ) -> Callable[[cloudbuild.RetryBuildRequest], operations_pb2.Operation]:
        r"""Return a callable for the retry build method over gRPC.

        Creates a new build based on the specified build.

        This method creates a new build using the original build
        request, which may or may not result in an identical build.

        For triggered builds:

        -  Triggered builds resolve to a precise revision; therefore a
           retry of a triggered build will result in a build that uses
           the same revision.

        For non-triggered builds that specify ``RepoSource``:

        -  If the original build built from the tip of a branch, the
           retried build will build from the tip of that branch, which
           may not be the same revision as the original build.
        -  If the original build specified a commit sha or revision ID,
           the retried build will use the identical source.

        For builds that specify ``StorageSource``:

        -  If the original build pulled source from Cloud Storage
           without specifying the generation of the object, the new
           build will use the current object, which may be different
           from the original build source.
        -  If the original build pulled source from Cloud Storage and
           specified the generation of the object, the new build will
           attempt to use the same object, which may or may not be
           available depending on the bucket's lifecycle management
           settings.

        Returns:
            Callable[[~.RetryBuildRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "retry_build" not in self._stubs:
            self._stubs["retry_build"] = self._logged_channel.unary_unary(
                "/google.devtools.cloudbuild.v1.CloudBuild/RetryBuild",
                request_serializer=cloudbuild.RetryBuildRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["retry_build"]

    @property
    def approve_build(
        self,
    ) -> Callable[[cloudbuild.ApproveBuildRequest], operations_pb2.Operation]:
        r"""Return a callable for the approve build method over gRPC.

        Approves or rejects a pending build.

        If approved, the returned LRO will be analogous to the
        LRO returned from a CreateBuild call.

        If rejected, the returned LRO will be immediately done.

        Returns:
            Callable[[~.ApproveBuildRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "approve_build" not in self._stubs:
            self._stubs["approve_build"] = self._logged_channel.unary_unary(
                "/google.devtools.cloudbuild.v1.CloudBuild/ApproveBuild",
                request_serializer=cloudbuild.ApproveBuildRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["approve_build"]

    @property
    def create_build_trigger(
        self,
    ) -> Callable[[cloudbuild.CreateBuildTriggerRequest], cloudbuild.BuildTrigger]:
        r"""Return a callable for the create build trigger method over gRPC.

        Creates a new ``BuildTrigger``.

        This API is experimental.

        Returns:
            Callable[[~.CreateBuildTriggerRequest],
                    ~.BuildTrigger]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_build_trigger" not in self._stubs:
            self._stubs["create_build_trigger"] = self._logged_channel.unary_unary(
                "/google.devtools.cloudbuild.v1.CloudBuild/CreateBuildTrigger",
                request_serializer=cloudbuild.CreateBuildTriggerRequest.serialize,
                response_deserializer=cloudbuild.BuildTrigger.deserialize,
            )
        return self._stubs["create_build_trigger"]

    @property
    def get_build_trigger(
        self,
    ) -> Callable[[cloudbuild.GetBuildTriggerRequest], cloudbuild.BuildTrigger]:
        r"""Return a callable for the get build trigger method over gRPC.

        Returns information about a ``BuildTrigger``.

        This API is experimental.

        Returns:
            Callable[[~.GetBuildTriggerRequest],
                    ~.BuildTrigger]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_build_trigger" not in self._stubs:
            self._stubs["get_build_trigger"] = self._logged_channel.unary_unary(
                "/google.devtools.cloudbuild.v1.CloudBuild/GetBuildTrigger",
                request_serializer=cloudbuild.GetBuildTriggerRequest.serialize,
                response_deserializer=cloudbuild.BuildTrigger.deserialize,
            )
        return self._stubs["get_build_trigger"]

    @property
    def list_build_triggers(
        self,
    ) -> Callable[
        [cloudbuild.ListBuildTriggersRequest], cloudbuild.ListBuildTriggersResponse
    ]:
        r"""Return a callable for the list build triggers method over gRPC.

        Lists existing ``BuildTrigger``\ s.

        This API is experimental.

        Returns:
            Callable[[~.ListBuildTriggersRequest],
                    ~.ListBuildTriggersResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_build_triggers" not in self._stubs:
            self._stubs["list_build_triggers"] = self._logged_channel.unary_unary(
                "/google.devtools.cloudbuild.v1.CloudBuild/ListBuildTriggers",
                request_serializer=cloudbuild.ListBuildTriggersRequest.serialize,
                response_deserializer=cloudbuild.ListBuildTriggersResponse.deserialize,
            )
        return self._stubs["list_build_triggers"]

    @property
    def delete_build_trigger(
        self,
    ) -> Callable[[cloudbuild.DeleteBuildTriggerRequest], empty_pb2.Empty]:
        r"""Return a callable for the delete build trigger method over gRPC.

        Deletes a ``BuildTrigger`` by its project ID and trigger ID.

        This API is experimental.

        Returns:
            Callable[[~.DeleteBuildTriggerRequest],
                    ~.Empty]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_build_trigger" not in self._stubs:
            self._stubs["delete_build_trigger"] = self._logged_channel.unary_unary(
                "/google.devtools.cloudbuild.v1.CloudBuild/DeleteBuildTrigger",
                request_serializer=cloudbuild.DeleteBuildTriggerRequest.serialize,
                response_deserializer=empty_pb2.Empty.FromString,
            )
        return self._stubs["delete_build_trigger"]

    @property
    def update_build_trigger(
        self,
    ) -> Callable[[cloudbuild.UpdateBuildTriggerRequest], cloudbuild.BuildTrigger]:
        r"""Return a callable for the update build trigger method over gRPC.

        Updates a ``BuildTrigger`` by its project ID and trigger ID.

        This API is experimental.

        Returns:
            Callable[[~.UpdateBuildTriggerRequest],
                    ~.BuildTrigger]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_build_trigger" not in self._stubs:
            self._stubs["update_build_trigger"] = self._logged_channel.unary_unary(
                "/google.devtools.cloudbuild.v1.CloudBuild/UpdateBuildTrigger",
                request_serializer=cloudbuild.UpdateBuildTriggerRequest.serialize,
                response_deserializer=cloudbuild.BuildTrigger.deserialize,
            )
        return self._stubs["update_build_trigger"]

    @property
    def run_build_trigger(
        self,
    ) -> Callable[[cloudbuild.RunBuildTriggerRequest], operations_pb2.Operation]:
        r"""Return a callable for the run build trigger method over gRPC.

        Runs a ``BuildTrigger`` at a particular source revision.

        To run a regional or global trigger, use the POST request that
        includes the location endpoint in the path (ex.
        v1/projects/{projectId}/locations/{region}/triggers/{triggerId}:run).
        The POST request that does not include the location endpoint in
        the path can only be used when running global triggers.

        Returns:
            Callable[[~.RunBuildTriggerRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "run_build_trigger" not in self._stubs:
            self._stubs["run_build_trigger"] = self._logged_channel.unary_unary(
                "/google.devtools.cloudbuild.v1.CloudBuild/RunBuildTrigger",
                request_serializer=cloudbuild.RunBuildTriggerRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["run_build_trigger"]

    @property
    def receive_trigger_webhook(
        self,
    ) -> Callable[
        [cloudbuild.ReceiveTriggerWebhookRequest],
        cloudbuild.ReceiveTriggerWebhookResponse,
    ]:
        r"""Return a callable for the receive trigger webhook method over gRPC.

        ReceiveTriggerWebhook [Experimental] is called when the API
        receives a webhook request targeted at a specific trigger.

        Returns:
            Callable[[~.ReceiveTriggerWebhookRequest],
                    ~.ReceiveTriggerWebhookResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "receive_trigger_webhook" not in self._stubs:
            self._stubs["receive_trigger_webhook"] = self._logged_channel.unary_unary(
                "/google.devtools.cloudbuild.v1.CloudBuild/ReceiveTriggerWebhook",
                request_serializer=cloudbuild.ReceiveTriggerWebhookRequest.serialize,
                response_deserializer=cloudbuild.ReceiveTriggerWebhookResponse.deserialize,
            )
        return self._stubs["receive_trigger_webhook"]

    @property
    def create_worker_pool(
        self,
    ) -> Callable[[cloudbuild.CreateWorkerPoolRequest], operations_pb2.Operation]:
        r"""Return a callable for the create worker pool method over gRPC.

        Creates a ``WorkerPool``.

        Returns:
            Callable[[~.CreateWorkerPoolRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_worker_pool" not in self._stubs:
            self._stubs["create_worker_pool"] = self._logged_channel.unary_unary(
                "/google.devtools.cloudbuild.v1.CloudBuild/CreateWorkerPool",
                request_serializer=cloudbuild.CreateWorkerPoolRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["create_worker_pool"]

    @property
    def get_worker_pool(
        self,
    ) -> Callable[[cloudbuild.GetWorkerPoolRequest], cloudbuild.WorkerPool]:
        r"""Return a callable for the get worker pool method over gRPC.

        Returns details of a ``WorkerPool``.

        Returns:
            Callable[[~.GetWorkerPoolRequest],
                    ~.WorkerPool]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_worker_pool" not in self._stubs:
            self._stubs["get_worker_pool"] = self._logged_channel.unary_unary(
                "/google.devtools.cloudbuild.v1.CloudBuild/GetWorkerPool",
                request_serializer=cloudbuild.GetWorkerPoolRequest.serialize,
                response_deserializer=cloudbuild.WorkerPool.deserialize,
            )
        return self._stubs["get_worker_pool"]

    @property
    def delete_worker_pool(
        self,
    ) -> Callable[[cloudbuild.DeleteWorkerPoolRequest], operations_pb2.Operation]:
        r"""Return a callable for the delete worker pool method over gRPC.

        Deletes a ``WorkerPool``.

        Returns:
            Callable[[~.DeleteWorkerPoolRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_worker_pool" not in self._stubs:
            self._stubs["delete_worker_pool"] = self._logged_channel.unary_unary(
                "/google.devtools.cloudbuild.v1.CloudBuild/DeleteWorkerPool",
                request_serializer=cloudbuild.DeleteWorkerPoolRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["delete_worker_pool"]

    @property
    def update_worker_pool(
        self,
    ) -> Callable[[cloudbuild.UpdateWorkerPoolRequest], operations_pb2.Operation]:
        r"""Return a callable for the update worker pool method over gRPC.

        Updates a ``WorkerPool``.

        Returns:
            Callable[[~.UpdateWorkerPoolRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_worker_pool" not in self._stubs:
            self._stubs["update_worker_pool"] = self._logged_channel.unary_unary(
                "/google.devtools.cloudbuild.v1.CloudBuild/UpdateWorkerPool",
                request_serializer=cloudbuild.UpdateWorkerPoolRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["update_worker_pool"]

    @property
    def list_worker_pools(
        self,
    ) -> Callable[
        [cloudbuild.ListWorkerPoolsRequest], cloudbuild.ListWorkerPoolsResponse
    ]:
        r"""Return a callable for the list worker pools method over gRPC.

        Lists ``WorkerPool``\ s.

        Returns:
            Callable[[~.ListWorkerPoolsRequest],
                    ~.ListWorkerPoolsResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_worker_pools" not in self._stubs:
            self._stubs["list_worker_pools"] = self._logged_channel.unary_unary(
                "/google.devtools.cloudbuild.v1.CloudBuild/ListWorkerPools",
                request_serializer=cloudbuild.ListWorkerPoolsRequest.serialize,
                response_deserializer=cloudbuild.ListWorkerPoolsResponse.deserialize,
            )
        return self._stubs["list_worker_pools"]

    def close(self):
        self._logged_channel.close()

    @property
    def kind(self) -> str:
        return "grpc"


__all__ = ("CloudBuildGrpcTransport",)
