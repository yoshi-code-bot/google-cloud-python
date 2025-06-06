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
import inspect
import json
import logging as std_logging
import pickle
from typing import Awaitable, Callable, Dict, Optional, Sequence, Tuple, Union
import warnings

from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1, grpc_helpers_async
from google.api_core import retry_async as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.protobuf import empty_pb2  # type: ignore
from google.protobuf.json_format import MessageToJson
import google.protobuf.message
import grpc  # type: ignore
from grpc.experimental import aio  # type: ignore
import proto  # type: ignore

from google.apps.chat_v1.types import (
    space_notification_setting as gc_space_notification_setting,
)
from google.apps.chat_v1.types import attachment
from google.apps.chat_v1.types import membership
from google.apps.chat_v1.types import membership as gc_membership
from google.apps.chat_v1.types import message
from google.apps.chat_v1.types import message as gc_message
from google.apps.chat_v1.types import reaction
from google.apps.chat_v1.types import reaction as gc_reaction
from google.apps.chat_v1.types import space
from google.apps.chat_v1.types import space as gc_space
from google.apps.chat_v1.types import space_event
from google.apps.chat_v1.types import space_notification_setting
from google.apps.chat_v1.types import space_read_state
from google.apps.chat_v1.types import space_read_state as gc_space_read_state
from google.apps.chat_v1.types import space_setup, thread_read_state

from .base import DEFAULT_CLIENT_INFO, ChatServiceTransport
from .grpc import ChatServiceGrpcTransport

try:
    from google.api_core import client_logging  # type: ignore

    CLIENT_LOGGING_SUPPORTED = True  # pragma: NO COVER
except ImportError:  # pragma: NO COVER
    CLIENT_LOGGING_SUPPORTED = False

_LOGGER = std_logging.getLogger(__name__)


class _LoggingClientAIOInterceptor(
    grpc.aio.UnaryUnaryClientInterceptor
):  # pragma: NO COVER
    async def intercept_unary_unary(self, continuation, client_call_details, request):
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
                    "serviceName": "google.chat.v1.ChatService",
                    "rpcName": str(client_call_details.method),
                    "request": grpc_request,
                    "metadata": grpc_request["metadata"],
                },
            )
        response = await continuation(client_call_details, request)
        if logging_enabled:  # pragma: NO COVER
            response_metadata = await response.trailing_metadata()
            # Convert gRPC metadata `<class 'grpc.aio._metadata.Metadata'>` to list of tuples
            metadata = (
                dict([(k, str(v)) for k, v in response_metadata])
                if response_metadata
                else None
            )
            result = await response
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
                f"Received response to rpc {client_call_details.method}.",
                extra={
                    "serviceName": "google.chat.v1.ChatService",
                    "rpcName": str(client_call_details.method),
                    "response": grpc_response,
                    "metadata": grpc_response["metadata"],
                },
            )
        return response


class ChatServiceGrpcAsyncIOTransport(ChatServiceTransport):
    """gRPC AsyncIO backend transport for ChatService.

    Enables developers to build Chat apps and
    integrations on Google Chat Platform.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends protocol buffers over the wire using gRPC (which is built on
    top of HTTP/2); the ``grpcio`` package must be installed.
    """

    _grpc_channel: aio.Channel
    _stubs: Dict[str, Callable] = {}

    @classmethod
    def create_channel(
        cls,
        host: str = "chat.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        quota_project_id: Optional[str] = None,
        **kwargs,
    ) -> aio.Channel:
        """Create and return a gRPC AsyncIO channel object.
        Args:
            host (Optional[str]): The host for the channel to use.
            credentials (Optional[~.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If
                none are specified, the client will attempt to ascertain
                the credentials from the environment.
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
            scopes (Optional[Sequence[str]]): A optional list of scopes needed for this
                service. These are only used when credentials are not specified and
                are passed to :func:`google.auth.default`.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            kwargs (Optional[dict]): Keyword arguments, which are passed to the
                channel creation.
        Returns:
            aio.Channel: A gRPC AsyncIO channel object.
        """

        return grpc_helpers_async.create_channel(
            host,
            credentials=credentials,
            credentials_file=credentials_file,
            quota_project_id=quota_project_id,
            default_scopes=cls.AUTH_SCOPES,
            scopes=scopes,
            default_host=cls.DEFAULT_HOST,
            **kwargs,
        )

    def __init__(
        self,
        *,
        host: str = "chat.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        channel: Optional[Union[aio.Channel, Callable[..., aio.Channel]]] = None,
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
                 The hostname to connect to (default: 'chat.googleapis.com').
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
                This argument is ignored if a ``channel`` instance is provided.
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is ignored if a ``channel`` instance is provided.
            scopes (Optional[Sequence[str]]): A optional list of scopes needed for this
                service. These are only used when credentials are not specified and
                are passed to :func:`google.auth.default`.
            channel (Optional[Union[aio.Channel, Callable[..., aio.Channel]]]):
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
            google.auth.exceptions.MutualTlsChannelError: If mutual TLS transport
              creation failed for any reason.
          google.api_core.exceptions.DuplicateCredentialArgs: If both ``credentials``
              and ``credentials_file`` are passed.
        """
        self._grpc_channel = None
        self._ssl_channel_credentials = ssl_channel_credentials
        self._stubs: Dict[str, Callable] = {}

        if api_mtls_endpoint:
            warnings.warn("api_mtls_endpoint is deprecated", DeprecationWarning)
        if client_cert_source:
            warnings.warn("client_cert_source is deprecated", DeprecationWarning)

        if isinstance(channel, aio.Channel):
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

        self._interceptor = _LoggingClientAIOInterceptor()
        self._grpc_channel._unary_unary_interceptors.append(self._interceptor)
        self._logged_channel = self._grpc_channel
        self._wrap_with_kind = (
            "kind" in inspect.signature(gapic_v1.method_async.wrap_method).parameters
        )
        # Wrap messages. This must be done after self._logged_channel exists
        self._prep_wrapped_messages(client_info)

    @property
    def grpc_channel(self) -> aio.Channel:
        """Create the channel designed to connect to this service.

        This property caches on the instance; repeated calls return
        the same channel.
        """
        # Return the channel from cache.
        return self._grpc_channel

    @property
    def create_message(
        self,
    ) -> Callable[[gc_message.CreateMessageRequest], Awaitable[gc_message.Message]]:
        r"""Return a callable for the create message method over gRPC.

        Creates a message in a Google Chat space. For an example, see
        `Send a
        message <https://developers.google.com/workspace/chat/create-messages>`__.

        The ``create()`` method requires either `user
        authentication <https://developers.google.com/workspace/chat/authenticate-authorize-chat-user>`__
        or `app
        authentication <https://developers.google.com/workspace/chat/authorize-import>`__.
        Chat attributes the message sender differently depending on the
        type of authentication that you use in your request.

        The following image shows how Chat attributes a message when you
        use app authentication. Chat displays the Chat app as the
        message sender. The content of the message can contain text
        (``text``), cards (``cardsV2``), and accessory widgets
        (``accessoryWidgets``).

        |Message sent with app authentication async gRPC|

        The following image shows how Chat attributes a message when you
        use user authentication. Chat displays the user as the message
        sender and attributes the Chat app to the message by displaying
        its name. The content of message can only contain text
        (``text``).

        |Message sent with user authentication async gRPC|

        The maximum message size, including the message contents, is
        32,000 bytes.

        For
        `webhook <https://developers.google.com/workspace/chat/quickstart/webhooks>`__
        requests, the response doesn't contain the full message. The
        response only populates the ``name`` and ``thread.name`` fields
        in addition to the information that was in the request.

        .. |Message sent with app authentication async gRPC| image:: https://developers.google.com/workspace/chat/images/message-app-auth.svg
        .. |Message sent with user authentication async gRPC| image:: https://developers.google.com/workspace/chat/images/message-user-auth.svg

        Returns:
            Callable[[~.CreateMessageRequest],
                    Awaitable[~.Message]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_message" not in self._stubs:
            self._stubs["create_message"] = self._logged_channel.unary_unary(
                "/google.chat.v1.ChatService/CreateMessage",
                request_serializer=gc_message.CreateMessageRequest.serialize,
                response_deserializer=gc_message.Message.deserialize,
            )
        return self._stubs["create_message"]

    @property
    def list_messages(
        self,
    ) -> Callable[
        [message.ListMessagesRequest], Awaitable[message.ListMessagesResponse]
    ]:
        r"""Return a callable for the list messages method over gRPC.

        Lists messages in a space that the caller is a member of,
        including messages from blocked members and spaces. If you list
        messages from a space with no messages, the response is an empty
        object. When using a REST/HTTP interface, the response contains
        an empty JSON object, ``{}``. For an example, see `List
        messages <https://developers.google.com/workspace/chat/api/guides/v1/messages/list>`__.

        Requires `user
        authentication <https://developers.google.com/workspace/chat/authenticate-authorize-chat-user>`__.

        Returns:
            Callable[[~.ListMessagesRequest],
                    Awaitable[~.ListMessagesResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_messages" not in self._stubs:
            self._stubs["list_messages"] = self._logged_channel.unary_unary(
                "/google.chat.v1.ChatService/ListMessages",
                request_serializer=message.ListMessagesRequest.serialize,
                response_deserializer=message.ListMessagesResponse.deserialize,
            )
        return self._stubs["list_messages"]

    @property
    def list_memberships(
        self,
    ) -> Callable[
        [membership.ListMembershipsRequest],
        Awaitable[membership.ListMembershipsResponse],
    ]:
        r"""Return a callable for the list memberships method over gRPC.

        Lists memberships in a space. For an example, see `List users
        and Google Chat apps in a
        space <https://developers.google.com/workspace/chat/list-members>`__.
        Listing memberships with `app
        authentication <https://developers.google.com/workspace/chat/authenticate-authorize-chat-app>`__
        lists memberships in spaces that the Chat app has access to, but
        excludes Chat app memberships, including its own. Listing
        memberships with `User
        authentication <https://developers.google.com/workspace/chat/authenticate-authorize-chat-user>`__
        lists memberships in spaces that the authenticated user has
        access to.

        Supports the following types of
        `authentication <https://developers.google.com/workspace/chat/authenticate-authorize>`__:

        -  `App
           authentication <https://developers.google.com/workspace/chat/authenticate-authorize-chat-app>`__

        -  `User
           authentication <https://developers.google.com/workspace/chat/authenticate-authorize-chat-user>`__
           You can authenticate and authorize this method with
           administrator privileges by setting the ``use_admin_access``
           field in the request.

        Returns:
            Callable[[~.ListMembershipsRequest],
                    Awaitable[~.ListMembershipsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_memberships" not in self._stubs:
            self._stubs["list_memberships"] = self._logged_channel.unary_unary(
                "/google.chat.v1.ChatService/ListMemberships",
                request_serializer=membership.ListMembershipsRequest.serialize,
                response_deserializer=membership.ListMembershipsResponse.deserialize,
            )
        return self._stubs["list_memberships"]

    @property
    def get_membership(
        self,
    ) -> Callable[[membership.GetMembershipRequest], Awaitable[membership.Membership]]:
        r"""Return a callable for the get membership method over gRPC.

        Returns details about a membership. For an example, see `Get
        details about a user's or Google Chat app's
        membership <https://developers.google.com/workspace/chat/get-members>`__.

        Supports the following types of
        `authentication <https://developers.google.com/workspace/chat/authenticate-authorize>`__:

        -  `App
           authentication <https://developers.google.com/workspace/chat/authenticate-authorize-chat-app>`__

        -  `User
           authentication <https://developers.google.com/workspace/chat/authenticate-authorize-chat-user>`__
           You can authenticate and authorize this method with
           administrator privileges by setting the ``use_admin_access``
           field in the request.

        Returns:
            Callable[[~.GetMembershipRequest],
                    Awaitable[~.Membership]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_membership" not in self._stubs:
            self._stubs["get_membership"] = self._logged_channel.unary_unary(
                "/google.chat.v1.ChatService/GetMembership",
                request_serializer=membership.GetMembershipRequest.serialize,
                response_deserializer=membership.Membership.deserialize,
            )
        return self._stubs["get_membership"]

    @property
    def get_message(
        self,
    ) -> Callable[[message.GetMessageRequest], Awaitable[message.Message]]:
        r"""Return a callable for the get message method over gRPC.

        Returns details about a message. For an example, see `Get
        details about a
        message <https://developers.google.com/workspace/chat/get-messages>`__.

        Supports the following types of
        `authentication <https://developers.google.com/workspace/chat/authenticate-authorize>`__:

        -  `App
           authentication <https://developers.google.com/workspace/chat/authenticate-authorize-chat-app>`__

        -  `User
           authentication <https://developers.google.com/workspace/chat/authenticate-authorize-chat-user>`__

        Note: Might return a message from a blocked member or space.

        Returns:
            Callable[[~.GetMessageRequest],
                    Awaitable[~.Message]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_message" not in self._stubs:
            self._stubs["get_message"] = self._logged_channel.unary_unary(
                "/google.chat.v1.ChatService/GetMessage",
                request_serializer=message.GetMessageRequest.serialize,
                response_deserializer=message.Message.deserialize,
            )
        return self._stubs["get_message"]

    @property
    def update_message(
        self,
    ) -> Callable[[gc_message.UpdateMessageRequest], Awaitable[gc_message.Message]]:
        r"""Return a callable for the update message method over gRPC.

        Updates a message. There's a difference between the ``patch``
        and ``update`` methods. The ``patch`` method uses a ``patch``
        request while the ``update`` method uses a ``put`` request. We
        recommend using the ``patch`` method. For an example, see
        `Update a
        message <https://developers.google.com/workspace/chat/update-messages>`__.

        Supports the following types of
        `authentication <https://developers.google.com/workspace/chat/authenticate-authorize>`__:

        -  `App
           authentication <https://developers.google.com/workspace/chat/authenticate-authorize-chat-app>`__

        -  `User
           authentication <https://developers.google.com/workspace/chat/authenticate-authorize-chat-user>`__

        When using app authentication, requests can only update messages
        created by the calling Chat app.

        Returns:
            Callable[[~.UpdateMessageRequest],
                    Awaitable[~.Message]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_message" not in self._stubs:
            self._stubs["update_message"] = self._logged_channel.unary_unary(
                "/google.chat.v1.ChatService/UpdateMessage",
                request_serializer=gc_message.UpdateMessageRequest.serialize,
                response_deserializer=gc_message.Message.deserialize,
            )
        return self._stubs["update_message"]

    @property
    def delete_message(
        self,
    ) -> Callable[[message.DeleteMessageRequest], Awaitable[empty_pb2.Empty]]:
        r"""Return a callable for the delete message method over gRPC.

        Deletes a message. For an example, see `Delete a
        message <https://developers.google.com/workspace/chat/delete-messages>`__.

        Supports the following types of
        `authentication <https://developers.google.com/workspace/chat/authenticate-authorize>`__:

        -  `App
           authentication <https://developers.google.com/workspace/chat/authenticate-authorize-chat-app>`__

        -  `User
           authentication <https://developers.google.com/workspace/chat/authenticate-authorize-chat-user>`__

        When using app authentication, requests can only delete messages
        created by the calling Chat app.

        Returns:
            Callable[[~.DeleteMessageRequest],
                    Awaitable[~.Empty]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_message" not in self._stubs:
            self._stubs["delete_message"] = self._logged_channel.unary_unary(
                "/google.chat.v1.ChatService/DeleteMessage",
                request_serializer=message.DeleteMessageRequest.serialize,
                response_deserializer=empty_pb2.Empty.FromString,
            )
        return self._stubs["delete_message"]

    @property
    def get_attachment(
        self,
    ) -> Callable[[attachment.GetAttachmentRequest], Awaitable[attachment.Attachment]]:
        r"""Return a callable for the get attachment method over gRPC.

        Gets the metadata of a message attachment. The attachment data
        is fetched using the `media
        API <https://developers.google.com/workspace/chat/api/reference/rest/v1/media/download>`__.
        For an example, see `Get metadata about a message
        attachment <https://developers.google.com/workspace/chat/get-media-attachments>`__.
        Requires `app
        authentication <https://developers.google.com/workspace/chat/authenticate-authorize-chat-app>`__.

        Returns:
            Callable[[~.GetAttachmentRequest],
                    Awaitable[~.Attachment]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_attachment" not in self._stubs:
            self._stubs["get_attachment"] = self._logged_channel.unary_unary(
                "/google.chat.v1.ChatService/GetAttachment",
                request_serializer=attachment.GetAttachmentRequest.serialize,
                response_deserializer=attachment.Attachment.deserialize,
            )
        return self._stubs["get_attachment"]

    @property
    def upload_attachment(
        self,
    ) -> Callable[
        [attachment.UploadAttachmentRequest],
        Awaitable[attachment.UploadAttachmentResponse],
    ]:
        r"""Return a callable for the upload attachment method over gRPC.

        Uploads an attachment. For an example, see `Upload media as a
        file
        attachment <https://developers.google.com/workspace/chat/upload-media-attachments>`__.

        Requires user
        `authentication <https://developers.google.com/workspace/chat/authenticate-authorize-chat-user>`__.

        You can upload attachments up to 200 MB. Certain file types
        aren't supported. For details, see `File types blocked by Google
        Chat <https://support.google.com/chat/answer/7651457?&co=GENIE.Platform%3DDesktop#File%20types%20blocked%20in%20Google%20Chat>`__.

        Returns:
            Callable[[~.UploadAttachmentRequest],
                    Awaitable[~.UploadAttachmentResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "upload_attachment" not in self._stubs:
            self._stubs["upload_attachment"] = self._logged_channel.unary_unary(
                "/google.chat.v1.ChatService/UploadAttachment",
                request_serializer=attachment.UploadAttachmentRequest.serialize,
                response_deserializer=attachment.UploadAttachmentResponse.deserialize,
            )
        return self._stubs["upload_attachment"]

    @property
    def list_spaces(
        self,
    ) -> Callable[[space.ListSpacesRequest], Awaitable[space.ListSpacesResponse]]:
        r"""Return a callable for the list spaces method over gRPC.

        Lists spaces the caller is a member of. Group chats and DMs
        aren't listed until the first message is sent. For an example,
        see `List
        spaces <https://developers.google.com/workspace/chat/list-spaces>`__.

        Supports the following types of
        `authentication <https://developers.google.com/workspace/chat/authenticate-authorize>`__:

        -  `App
           authentication <https://developers.google.com/workspace/chat/authenticate-authorize-chat-app>`__

        -  `User
           authentication <https://developers.google.com/workspace/chat/authenticate-authorize-chat-user>`__

        To list all named spaces by Google Workspace organization, use
        the
        ```spaces.search()`` <https://developers.google.com/workspace/chat/api/reference/rest/v1/spaces/search>`__
        method using Workspace administrator privileges instead.

        Returns:
            Callable[[~.ListSpacesRequest],
                    Awaitable[~.ListSpacesResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_spaces" not in self._stubs:
            self._stubs["list_spaces"] = self._logged_channel.unary_unary(
                "/google.chat.v1.ChatService/ListSpaces",
                request_serializer=space.ListSpacesRequest.serialize,
                response_deserializer=space.ListSpacesResponse.deserialize,
            )
        return self._stubs["list_spaces"]

    @property
    def search_spaces(
        self,
    ) -> Callable[[space.SearchSpacesRequest], Awaitable[space.SearchSpacesResponse]]:
        r"""Return a callable for the search spaces method over gRPC.

        Returns a list of spaces in a Google Workspace organization
        based on an administrator's search.

        Requires `user authentication with administrator
        privileges <https://developers.google.com/workspace/chat/authenticate-authorize-chat-user#admin-privileges>`__.
        In the request, set ``use_admin_access`` to ``true``.

        Returns:
            Callable[[~.SearchSpacesRequest],
                    Awaitable[~.SearchSpacesResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "search_spaces" not in self._stubs:
            self._stubs["search_spaces"] = self._logged_channel.unary_unary(
                "/google.chat.v1.ChatService/SearchSpaces",
                request_serializer=space.SearchSpacesRequest.serialize,
                response_deserializer=space.SearchSpacesResponse.deserialize,
            )
        return self._stubs["search_spaces"]

    @property
    def get_space(self) -> Callable[[space.GetSpaceRequest], Awaitable[space.Space]]:
        r"""Return a callable for the get space method over gRPC.

        Returns details about a space. For an example, see `Get details
        about a
        space <https://developers.google.com/workspace/chat/get-spaces>`__.

        Supports the following types of
        `authentication <https://developers.google.com/workspace/chat/authenticate-authorize>`__:

        -  `App
           authentication <https://developers.google.com/workspace/chat/authenticate-authorize-chat-app>`__

        -  `User
           authentication <https://developers.google.com/workspace/chat/authenticate-authorize-chat-user>`__
           You can authenticate and authorize this method with
           administrator privileges by setting the ``use_admin_access``
           field in the request.

        Returns:
            Callable[[~.GetSpaceRequest],
                    Awaitable[~.Space]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_space" not in self._stubs:
            self._stubs["get_space"] = self._logged_channel.unary_unary(
                "/google.chat.v1.ChatService/GetSpace",
                request_serializer=space.GetSpaceRequest.serialize,
                response_deserializer=space.Space.deserialize,
            )
        return self._stubs["get_space"]

    @property
    def create_space(
        self,
    ) -> Callable[[gc_space.CreateSpaceRequest], Awaitable[gc_space.Space]]:
        r"""Return a callable for the create space method over gRPC.

        Creates a space with no members. Can be used to create a named
        space, or a group chat in ``Import mode``. For an example, see
        `Create a
        space <https://developers.google.com/workspace/chat/create-spaces>`__.

        If you receive the error message ``ALREADY_EXISTS`` when
        creating a space, try a different ``displayName``. An existing
        space within the Google Workspace organization might already use
        this display name.

        Supports the following types of
        `authentication <https://developers.google.com/workspace/chat/authenticate-authorize>`__:

        -  `App
           authentication <https://developers.google.com/workspace/chat/authenticate-authorize-chat-app>`__
           with `administrator
           approval <https://support.google.com/a?p=chat-app-auth>`__ in
           `Developer
           Preview <https://developers.google.com/workspace/preview>`__

        -  `User
           authentication <https://developers.google.com/workspace/chat/authenticate-authorize-chat-user>`__

        When authenticating as an app, the ``space.customer`` field must
        be set in the request.

        Returns:
            Callable[[~.CreateSpaceRequest],
                    Awaitable[~.Space]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_space" not in self._stubs:
            self._stubs["create_space"] = self._logged_channel.unary_unary(
                "/google.chat.v1.ChatService/CreateSpace",
                request_serializer=gc_space.CreateSpaceRequest.serialize,
                response_deserializer=gc_space.Space.deserialize,
            )
        return self._stubs["create_space"]

    @property
    def set_up_space(
        self,
    ) -> Callable[[space_setup.SetUpSpaceRequest], Awaitable[space.Space]]:
        r"""Return a callable for the set up space method over gRPC.

        Creates a space and adds specified users to it. The calling user
        is automatically added to the space, and shouldn't be specified
        as a membership in the request. For an example, see `Set up a
        space with initial
        members <https://developers.google.com/workspace/chat/set-up-spaces>`__.

        To specify the human members to add, add memberships with the
        appropriate ``membership.member.name``. To add a human user, use
        ``users/{user}``, where ``{user}`` can be the email address for
        the user. For users in the same Workspace organization
        ``{user}`` can also be the ``id`` for the person from the People
        API, or the ``id`` for the user in the Directory API. For
        example, if the People API Person profile ID for
        ``user@example.com`` is ``123456789``, you can add the user to
        the space by setting the ``membership.member.name`` to
        ``users/user@example.com`` or ``users/123456789``.

        To specify the Google groups to add, add memberships with the
        appropriate ``membership.group_member.name``. To add or invite a
        Google group, use ``groups/{group}``, where ``{group}`` is the
        ``id`` for the group from the Cloud Identity Groups API. For
        example, you can use `Cloud Identity Groups lookup
        API <https://cloud.google.com/identity/docs/reference/rest/v1/groups/lookup>`__
        to retrieve the ID ``123456789`` for group email
        ``group@example.com``, then you can add the group to the space
        by setting the ``membership.group_member.name`` to
        ``groups/123456789``. Group email is not supported, and Google
        groups can only be added as members in named spaces.

        For a named space or group chat, if the caller blocks, or is
        blocked by some members, or doesn't have permission to add some
        members, then those members aren't added to the created space.

        To create a direct message (DM) between the calling user and
        another human user, specify exactly one membership to represent
        the human user. If one user blocks the other, the request fails
        and the DM isn't created.

        To create a DM between the calling user and the calling app, set
        ``Space.singleUserBotDm`` to ``true`` and don't specify any
        memberships. You can only use this method to set up a DM with
        the calling app. To add the calling app as a member of a space
        or an existing DM between two human users, see `Invite or add a
        user or app to a
        space <https://developers.google.com/workspace/chat/create-members>`__.

        If a DM already exists between two users, even when one user
        blocks the other at the time a request is made, then the
        existing DM is returned.

        Spaces with threaded replies aren't supported. If you receive
        the error message ``ALREADY_EXISTS`` when setting up a space,
        try a different ``displayName``. An existing space within the
        Google Workspace organization might already use this display
        name.

        Requires `user
        authentication <https://developers.google.com/workspace/chat/authenticate-authorize-chat-user>`__.

        Returns:
            Callable[[~.SetUpSpaceRequest],
                    Awaitable[~.Space]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "set_up_space" not in self._stubs:
            self._stubs["set_up_space"] = self._logged_channel.unary_unary(
                "/google.chat.v1.ChatService/SetUpSpace",
                request_serializer=space_setup.SetUpSpaceRequest.serialize,
                response_deserializer=space.Space.deserialize,
            )
        return self._stubs["set_up_space"]

    @property
    def update_space(
        self,
    ) -> Callable[[gc_space.UpdateSpaceRequest], Awaitable[gc_space.Space]]:
        r"""Return a callable for the update space method over gRPC.

        Updates a space. For an example, see `Update a
        space <https://developers.google.com/workspace/chat/update-spaces>`__.

        If you're updating the ``displayName`` field and receive the
        error message ``ALREADY_EXISTS``, try a different display name..
        An existing space within the Google Workspace organization might
        already use this display name.

        Supports the following types of
        `authentication <https://developers.google.com/workspace/chat/authenticate-authorize>`__:

        -  `App
           authentication <https://developers.google.com/workspace/chat/authenticate-authorize-chat-app>`__
           with `administrator
           approval <https://support.google.com/a?p=chat-app-auth>`__ in
           `Developer
           Preview <https://developers.google.com/workspace/preview>`__

        -  `User
           authentication <https://developers.google.com/workspace/chat/authenticate-authorize-chat-user>`__
           You can authenticate and authorize this method with
           administrator privileges by setting the ``use_admin_access``
           field in the request.

        Returns:
            Callable[[~.UpdateSpaceRequest],
                    Awaitable[~.Space]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_space" not in self._stubs:
            self._stubs["update_space"] = self._logged_channel.unary_unary(
                "/google.chat.v1.ChatService/UpdateSpace",
                request_serializer=gc_space.UpdateSpaceRequest.serialize,
                response_deserializer=gc_space.Space.deserialize,
            )
        return self._stubs["update_space"]

    @property
    def delete_space(
        self,
    ) -> Callable[[space.DeleteSpaceRequest], Awaitable[empty_pb2.Empty]]:
        r"""Return a callable for the delete space method over gRPC.

        Deletes a named space. Always performs a cascading delete, which
        means that the space's child resources—like messages posted in
        the space and memberships in the space—are also deleted. For an
        example, see `Delete a
        space <https://developers.google.com/workspace/chat/delete-spaces>`__.

        Supports the following types of
        `authentication <https://developers.google.com/workspace/chat/authenticate-authorize>`__:

        -  `App
           authentication <https://developers.google.com/workspace/chat/authenticate-authorize-chat-app>`__
           with `administrator
           approval <https://support.google.com/a?p=chat-app-auth>`__ in
           `Developer
           Preview <https://developers.google.com/workspace/preview>`__

        -  `User
           authentication <https://developers.google.com/workspace/chat/authenticate-authorize-chat-user>`__
           You can authenticate and authorize this method with
           administrator privileges by setting the ``use_admin_access``
           field in the request.

        Returns:
            Callable[[~.DeleteSpaceRequest],
                    Awaitable[~.Empty]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_space" not in self._stubs:
            self._stubs["delete_space"] = self._logged_channel.unary_unary(
                "/google.chat.v1.ChatService/DeleteSpace",
                request_serializer=space.DeleteSpaceRequest.serialize,
                response_deserializer=empty_pb2.Empty.FromString,
            )
        return self._stubs["delete_space"]

    @property
    def complete_import_space(
        self,
    ) -> Callable[
        [space.CompleteImportSpaceRequest], Awaitable[space.CompleteImportSpaceResponse]
    ]:
        r"""Return a callable for the complete import space method over gRPC.

        Completes the `import
        process <https://developers.google.com/workspace/chat/import-data>`__
        for the specified space and makes it visible to users.

        Requires `app
        authentication <https://developers.google.com/workspace/chat/authenticate-authorize-chat-app>`__
        and domain-wide delegation. For more information, see `Authorize
        Google Chat apps to import
        data <https://developers.google.com/workspace/chat/authorize-import>`__.

        Returns:
            Callable[[~.CompleteImportSpaceRequest],
                    Awaitable[~.CompleteImportSpaceResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "complete_import_space" not in self._stubs:
            self._stubs["complete_import_space"] = self._logged_channel.unary_unary(
                "/google.chat.v1.ChatService/CompleteImportSpace",
                request_serializer=space.CompleteImportSpaceRequest.serialize,
                response_deserializer=space.CompleteImportSpaceResponse.deserialize,
            )
        return self._stubs["complete_import_space"]

    @property
    def find_direct_message(
        self,
    ) -> Callable[[space.FindDirectMessageRequest], Awaitable[space.Space]]:
        r"""Return a callable for the find direct message method over gRPC.

        Returns the existing direct message with the specified user. If
        no direct message space is found, returns a ``404 NOT_FOUND``
        error. For an example, see `Find a direct
        message </chat/api/guides/v1/spaces/find-direct-message>`__.

        With `app
        authentication <https://developers.google.com/workspace/chat/authenticate-authorize-chat-app>`__,
        returns the direct message space between the specified user and
        the calling Chat app.

        With `user
        authentication <https://developers.google.com/workspace/chat/authenticate-authorize-chat-user>`__,
        returns the direct message space between the specified user and
        the authenticated user.

        // Supports the following types of
        `authentication <https://developers.google.com/workspace/chat/authenticate-authorize>`__:

        -  `App
           authentication <https://developers.google.com/workspace/chat/authenticate-authorize-chat-app>`__

        -  `User
           authentication <https://developers.google.com/workspace/chat/authenticate-authorize-chat-user>`__

        Returns:
            Callable[[~.FindDirectMessageRequest],
                    Awaitable[~.Space]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "find_direct_message" not in self._stubs:
            self._stubs["find_direct_message"] = self._logged_channel.unary_unary(
                "/google.chat.v1.ChatService/FindDirectMessage",
                request_serializer=space.FindDirectMessageRequest.serialize,
                response_deserializer=space.Space.deserialize,
            )
        return self._stubs["find_direct_message"]

    @property
    def create_membership(
        self,
    ) -> Callable[
        [gc_membership.CreateMembershipRequest], Awaitable[gc_membership.Membership]
    ]:
        r"""Return a callable for the create membership method over gRPC.

        Creates a membership for the calling Chat app, a user, or a
        Google Group. Creating memberships for other Chat apps isn't
        supported. When creating a membership, if the specified member
        has their auto-accept policy turned off, then they're invited,
        and must accept the space invitation before joining. Otherwise,
        creating a membership adds the member directly to the specified
        space.

        Supports the following types of
        `authentication <https://developers.google.com/workspace/chat/authenticate-authorize>`__:

        -  `App
           authentication <https://developers.google.com/workspace/chat/authenticate-authorize-chat-app>`__
           with `administrator
           approval <https://support.google.com/a?p=chat-app-auth>`__ in
           `Developer
           Preview <https://developers.google.com/workspace/preview>`__

        -  `User
           authentication <https://developers.google.com/workspace/chat/authenticate-authorize-chat-user>`__
           You can authenticate and authorize this method with
           administrator privileges by setting the ``use_admin_access``
           field in the request.

        For example usage, see:

        -  `Invite or add a user to a
           space <https://developers.google.com/workspace/chat/create-members#create-user-membership>`__.

        -  `Invite or add a Google Group to a
           space <https://developers.google.com/workspace/chat/create-members#create-group-membership>`__.

        -  `Add the Chat app to a
           space <https://developers.google.com/workspace/chat/create-members#create-membership-calling-api>`__.

        Returns:
            Callable[[~.CreateMembershipRequest],
                    Awaitable[~.Membership]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_membership" not in self._stubs:
            self._stubs["create_membership"] = self._logged_channel.unary_unary(
                "/google.chat.v1.ChatService/CreateMembership",
                request_serializer=gc_membership.CreateMembershipRequest.serialize,
                response_deserializer=gc_membership.Membership.deserialize,
            )
        return self._stubs["create_membership"]

    @property
    def update_membership(
        self,
    ) -> Callable[
        [gc_membership.UpdateMembershipRequest], Awaitable[gc_membership.Membership]
    ]:
        r"""Return a callable for the update membership method over gRPC.

        Updates a membership. For an example, see `Update a user's
        membership in a
        space <https://developers.google.com/workspace/chat/update-members>`__.

        Supports the following types of
        `authentication <https://developers.google.com/workspace/chat/authenticate-authorize>`__:

        -  `App
           authentication <https://developers.google.com/workspace/chat/authenticate-authorize-chat-app>`__
           with `administrator
           approval <https://support.google.com/a?p=chat-app-auth>`__ in
           `Developer
           Preview <https://developers.google.com/workspace/preview>`__

        -  `User
           authentication <https://developers.google.com/workspace/chat/authenticate-authorize-chat-user>`__
           You can authenticate and authorize this method with
           administrator privileges by setting the ``use_admin_access``
           field in the request.

        Returns:
            Callable[[~.UpdateMembershipRequest],
                    Awaitable[~.Membership]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_membership" not in self._stubs:
            self._stubs["update_membership"] = self._logged_channel.unary_unary(
                "/google.chat.v1.ChatService/UpdateMembership",
                request_serializer=gc_membership.UpdateMembershipRequest.serialize,
                response_deserializer=gc_membership.Membership.deserialize,
            )
        return self._stubs["update_membership"]

    @property
    def delete_membership(
        self,
    ) -> Callable[
        [membership.DeleteMembershipRequest], Awaitable[membership.Membership]
    ]:
        r"""Return a callable for the delete membership method over gRPC.

        Deletes a membership. For an example, see `Remove a user or a
        Google Chat app from a
        space <https://developers.google.com/workspace/chat/delete-members>`__.

        Supports the following types of
        `authentication <https://developers.google.com/workspace/chat/authenticate-authorize>`__:

        -  `App
           authentication <https://developers.google.com/workspace/chat/authenticate-authorize-chat-app>`__
           with `administrator
           approval <https://support.google.com/a?p=chat-app-auth>`__ in
           `Developer
           Preview <https://developers.google.com/workspace/preview>`__

        -  `User
           authentication <https://developers.google.com/workspace/chat/authenticate-authorize-chat-user>`__
           You can authenticate and authorize this method with
           administrator privileges by setting the ``use_admin_access``
           field in the request.

        Returns:
            Callable[[~.DeleteMembershipRequest],
                    Awaitable[~.Membership]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_membership" not in self._stubs:
            self._stubs["delete_membership"] = self._logged_channel.unary_unary(
                "/google.chat.v1.ChatService/DeleteMembership",
                request_serializer=membership.DeleteMembershipRequest.serialize,
                response_deserializer=membership.Membership.deserialize,
            )
        return self._stubs["delete_membership"]

    @property
    def create_reaction(
        self,
    ) -> Callable[[gc_reaction.CreateReactionRequest], Awaitable[gc_reaction.Reaction]]:
        r"""Return a callable for the create reaction method over gRPC.

        Creates a reaction and adds it to a message. For an example, see
        `Add a reaction to a
        message <https://developers.google.com/workspace/chat/create-reactions>`__.

        Requires `user
        authentication <https://developers.google.com/workspace/chat/authenticate-authorize-chat-user>`__.

        Returns:
            Callable[[~.CreateReactionRequest],
                    Awaitable[~.Reaction]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_reaction" not in self._stubs:
            self._stubs["create_reaction"] = self._logged_channel.unary_unary(
                "/google.chat.v1.ChatService/CreateReaction",
                request_serializer=gc_reaction.CreateReactionRequest.serialize,
                response_deserializer=gc_reaction.Reaction.deserialize,
            )
        return self._stubs["create_reaction"]

    @property
    def list_reactions(
        self,
    ) -> Callable[
        [reaction.ListReactionsRequest], Awaitable[reaction.ListReactionsResponse]
    ]:
        r"""Return a callable for the list reactions method over gRPC.

        Lists reactions to a message. For an example, see `List
        reactions for a
        message <https://developers.google.com/workspace/chat/list-reactions>`__.

        Requires `user
        authentication <https://developers.google.com/workspace/chat/authenticate-authorize-chat-user>`__.

        Returns:
            Callable[[~.ListReactionsRequest],
                    Awaitable[~.ListReactionsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_reactions" not in self._stubs:
            self._stubs["list_reactions"] = self._logged_channel.unary_unary(
                "/google.chat.v1.ChatService/ListReactions",
                request_serializer=reaction.ListReactionsRequest.serialize,
                response_deserializer=reaction.ListReactionsResponse.deserialize,
            )
        return self._stubs["list_reactions"]

    @property
    def delete_reaction(
        self,
    ) -> Callable[[reaction.DeleteReactionRequest], Awaitable[empty_pb2.Empty]]:
        r"""Return a callable for the delete reaction method over gRPC.

        Deletes a reaction to a message. For an example, see `Delete a
        reaction <https://developers.google.com/workspace/chat/delete-reactions>`__.

        Requires `user
        authentication <https://developers.google.com/workspace/chat/authenticate-authorize-chat-user>`__.

        Returns:
            Callable[[~.DeleteReactionRequest],
                    Awaitable[~.Empty]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_reaction" not in self._stubs:
            self._stubs["delete_reaction"] = self._logged_channel.unary_unary(
                "/google.chat.v1.ChatService/DeleteReaction",
                request_serializer=reaction.DeleteReactionRequest.serialize,
                response_deserializer=empty_pb2.Empty.FromString,
            )
        return self._stubs["delete_reaction"]

    @property
    def create_custom_emoji(
        self,
    ) -> Callable[[reaction.CreateCustomEmojiRequest], Awaitable[reaction.CustomEmoji]]:
        r"""Return a callable for the create custom emoji method over gRPC.

        Creates a custom emoji.

        Custom emojis are only available for Google Workspace accounts,
        and the administrator must turn custom emojis on for the
        organization. For more information, see `Learn about custom
        emojis in Google
        Chat <https://support.google.com/chat/answer/12800149>`__ and
        `Manage custom emoji
        permissions <https://support.google.com/a/answer/12850085>`__.

        Requires `user
        authentication <https://developers.google.com/workspace/chat/authenticate-authorize-chat-user>`__.

        Returns:
            Callable[[~.CreateCustomEmojiRequest],
                    Awaitable[~.CustomEmoji]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_custom_emoji" not in self._stubs:
            self._stubs["create_custom_emoji"] = self._logged_channel.unary_unary(
                "/google.chat.v1.ChatService/CreateCustomEmoji",
                request_serializer=reaction.CreateCustomEmojiRequest.serialize,
                response_deserializer=reaction.CustomEmoji.deserialize,
            )
        return self._stubs["create_custom_emoji"]

    @property
    def get_custom_emoji(
        self,
    ) -> Callable[[reaction.GetCustomEmojiRequest], Awaitable[reaction.CustomEmoji]]:
        r"""Return a callable for the get custom emoji method over gRPC.

        Returns details about a custom emoji.

        Custom emojis are only available for Google Workspace accounts,
        and the administrator must turn custom emojis on for the
        organization. For more information, see `Learn about custom
        emojis in Google
        Chat <https://support.google.com/chat/answer/12800149>`__ and
        `Manage custom emoji
        permissions <https://support.google.com/a/answer/12850085>`__.

        Requires `user
        authentication <https://developers.google.com/workspace/chat/authenticate-authorize-chat-user>`__.

        Returns:
            Callable[[~.GetCustomEmojiRequest],
                    Awaitable[~.CustomEmoji]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_custom_emoji" not in self._stubs:
            self._stubs["get_custom_emoji"] = self._logged_channel.unary_unary(
                "/google.chat.v1.ChatService/GetCustomEmoji",
                request_serializer=reaction.GetCustomEmojiRequest.serialize,
                response_deserializer=reaction.CustomEmoji.deserialize,
            )
        return self._stubs["get_custom_emoji"]

    @property
    def list_custom_emojis(
        self,
    ) -> Callable[
        [reaction.ListCustomEmojisRequest], Awaitable[reaction.ListCustomEmojisResponse]
    ]:
        r"""Return a callable for the list custom emojis method over gRPC.

        Lists custom emojis visible to the authenticated user.

        Custom emojis are only available for Google Workspace accounts,
        and the administrator must turn custom emojis on for the
        organization. For more information, see `Learn about custom
        emojis in Google
        Chat <https://support.google.com/chat/answer/12800149>`__ and
        `Manage custom emoji
        permissions <https://support.google.com/a/answer/12850085>`__.

        Requires `user
        authentication <https://developers.google.com/workspace/chat/authenticate-authorize-chat-user>`__.

        Returns:
            Callable[[~.ListCustomEmojisRequest],
                    Awaitable[~.ListCustomEmojisResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_custom_emojis" not in self._stubs:
            self._stubs["list_custom_emojis"] = self._logged_channel.unary_unary(
                "/google.chat.v1.ChatService/ListCustomEmojis",
                request_serializer=reaction.ListCustomEmojisRequest.serialize,
                response_deserializer=reaction.ListCustomEmojisResponse.deserialize,
            )
        return self._stubs["list_custom_emojis"]

    @property
    def delete_custom_emoji(
        self,
    ) -> Callable[[reaction.DeleteCustomEmojiRequest], Awaitable[empty_pb2.Empty]]:
        r"""Return a callable for the delete custom emoji method over gRPC.

        Deletes a custom emoji. By default, users can only delete custom
        emoji they created. `Emoji
        managers <https://support.google.com/a/answer/12850085>`__
        assigned by the administrator can delete any custom emoji in the
        organization. See `Learn about custom emojis in Google
        Chat <https://support.google.com/chat/answer/12800149>`__.

        Custom emojis are only available for Google Workspace accounts,
        and the administrator must turn custom emojis on for the
        organization. For more information, see `Learn about custom
        emojis in Google
        Chat <https://support.google.com/chat/answer/12800149>`__ and
        `Manage custom emoji
        permissions <https://support.google.com/a/answer/12850085>`__.

        Requires `user
        authentication <https://developers.google.com/workspace/chat/authenticate-authorize-chat-user>`__.

        Returns:
            Callable[[~.DeleteCustomEmojiRequest],
                    Awaitable[~.Empty]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_custom_emoji" not in self._stubs:
            self._stubs["delete_custom_emoji"] = self._logged_channel.unary_unary(
                "/google.chat.v1.ChatService/DeleteCustomEmoji",
                request_serializer=reaction.DeleteCustomEmojiRequest.serialize,
                response_deserializer=empty_pb2.Empty.FromString,
            )
        return self._stubs["delete_custom_emoji"]

    @property
    def get_space_read_state(
        self,
    ) -> Callable[
        [space_read_state.GetSpaceReadStateRequest],
        Awaitable[space_read_state.SpaceReadState],
    ]:
        r"""Return a callable for the get space read state method over gRPC.

        Returns details about a user's read state within a space, used
        to identify read and unread messages. For an example, see `Get
        details about a user's space read
        state <https://developers.google.com/workspace/chat/get-space-read-state>`__.

        Requires `user
        authentication <https://developers.google.com/workspace/chat/authenticate-authorize-chat-user>`__.

        Returns:
            Callable[[~.GetSpaceReadStateRequest],
                    Awaitable[~.SpaceReadState]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_space_read_state" not in self._stubs:
            self._stubs["get_space_read_state"] = self._logged_channel.unary_unary(
                "/google.chat.v1.ChatService/GetSpaceReadState",
                request_serializer=space_read_state.GetSpaceReadStateRequest.serialize,
                response_deserializer=space_read_state.SpaceReadState.deserialize,
            )
        return self._stubs["get_space_read_state"]

    @property
    def update_space_read_state(
        self,
    ) -> Callable[
        [gc_space_read_state.UpdateSpaceReadStateRequest],
        Awaitable[gc_space_read_state.SpaceReadState],
    ]:
        r"""Return a callable for the update space read state method over gRPC.

        Updates a user's read state within a space, used to identify
        read and unread messages. For an example, see `Update a user's
        space read
        state <https://developers.google.com/workspace/chat/update-space-read-state>`__.

        Requires `user
        authentication <https://developers.google.com/workspace/chat/authenticate-authorize-chat-user>`__.

        Returns:
            Callable[[~.UpdateSpaceReadStateRequest],
                    Awaitable[~.SpaceReadState]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_space_read_state" not in self._stubs:
            self._stubs["update_space_read_state"] = self._logged_channel.unary_unary(
                "/google.chat.v1.ChatService/UpdateSpaceReadState",
                request_serializer=gc_space_read_state.UpdateSpaceReadStateRequest.serialize,
                response_deserializer=gc_space_read_state.SpaceReadState.deserialize,
            )
        return self._stubs["update_space_read_state"]

    @property
    def get_thread_read_state(
        self,
    ) -> Callable[
        [thread_read_state.GetThreadReadStateRequest],
        Awaitable[thread_read_state.ThreadReadState],
    ]:
        r"""Return a callable for the get thread read state method over gRPC.

        Returns details about a user's read state within a thread, used
        to identify read and unread messages. For an example, see `Get
        details about a user's thread read
        state <https://developers.google.com/workspace/chat/get-thread-read-state>`__.

        Requires `user
        authentication <https://developers.google.com/workspace/chat/authenticate-authorize-chat-user>`__.

        Returns:
            Callable[[~.GetThreadReadStateRequest],
                    Awaitable[~.ThreadReadState]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_thread_read_state" not in self._stubs:
            self._stubs["get_thread_read_state"] = self._logged_channel.unary_unary(
                "/google.chat.v1.ChatService/GetThreadReadState",
                request_serializer=thread_read_state.GetThreadReadStateRequest.serialize,
                response_deserializer=thread_read_state.ThreadReadState.deserialize,
            )
        return self._stubs["get_thread_read_state"]

    @property
    def get_space_event(
        self,
    ) -> Callable[
        [space_event.GetSpaceEventRequest], Awaitable[space_event.SpaceEvent]
    ]:
        r"""Return a callable for the get space event method over gRPC.

        Returns an event from a Google Chat space. The `event
        payload <https://developers.google.com/workspace/chat/api/reference/rest/v1/spaces.spaceEvents#SpaceEvent.FIELDS.oneof_payload>`__
        contains the most recent version of the resource that changed.
        For example, if you request an event about a new message but the
        message was later updated, the server returns the updated
        ``Message`` resource in the event payload.

        Note: The ``permissionSettings`` field is not returned in the
        Space object of the Space event data for this request.

        Requires `user
        authentication <https://developers.google.com/workspace/chat/authenticate-authorize-chat-user>`__.
        To get an event, the authenticated user must be a member of the
        space.

        For an example, see `Get details about an event from a Google
        Chat
        space <https://developers.google.com/workspace/chat/get-space-event>`__.

        Returns:
            Callable[[~.GetSpaceEventRequest],
                    Awaitable[~.SpaceEvent]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_space_event" not in self._stubs:
            self._stubs["get_space_event"] = self._logged_channel.unary_unary(
                "/google.chat.v1.ChatService/GetSpaceEvent",
                request_serializer=space_event.GetSpaceEventRequest.serialize,
                response_deserializer=space_event.SpaceEvent.deserialize,
            )
        return self._stubs["get_space_event"]

    @property
    def list_space_events(
        self,
    ) -> Callable[
        [space_event.ListSpaceEventsRequest],
        Awaitable[space_event.ListSpaceEventsResponse],
    ]:
        r"""Return a callable for the list space events method over gRPC.

        Lists events from a Google Chat space. For each event, the
        `payload <https://developers.google.com/workspace/chat/api/reference/rest/v1/spaces.spaceEvents#SpaceEvent.FIELDS.oneof_payload>`__
        contains the most recent version of the Chat resource. For
        example, if you list events about new space members, the server
        returns ``Membership`` resources that contain the latest
        membership details. If new members were removed during the
        requested period, the event payload contains an empty
        ``Membership`` resource.

        Requires `user
        authentication <https://developers.google.com/workspace/chat/authenticate-authorize-chat-user>`__.
        To list events, the authenticated user must be a member of the
        space.

        For an example, see `List events from a Google Chat
        space <https://developers.google.com/workspace/chat/list-space-events>`__.

        Returns:
            Callable[[~.ListSpaceEventsRequest],
                    Awaitable[~.ListSpaceEventsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_space_events" not in self._stubs:
            self._stubs["list_space_events"] = self._logged_channel.unary_unary(
                "/google.chat.v1.ChatService/ListSpaceEvents",
                request_serializer=space_event.ListSpaceEventsRequest.serialize,
                response_deserializer=space_event.ListSpaceEventsResponse.deserialize,
            )
        return self._stubs["list_space_events"]

    @property
    def get_space_notification_setting(
        self,
    ) -> Callable[
        [space_notification_setting.GetSpaceNotificationSettingRequest],
        Awaitable[space_notification_setting.SpaceNotificationSetting],
    ]:
        r"""Return a callable for the get space notification setting method over gRPC.

        Gets the space notification setting. For an example, see `Get
        the caller's space notification
        setting <https://developers.google.com/workspace/chat/get-space-notification-setting>`__.

        Requires `user
        authentication <https://developers.google.com/workspace/chat/authenticate-authorize-chat-user>`__.

        Returns:
            Callable[[~.GetSpaceNotificationSettingRequest],
                    Awaitable[~.SpaceNotificationSetting]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_space_notification_setting" not in self._stubs:
            self._stubs[
                "get_space_notification_setting"
            ] = self._logged_channel.unary_unary(
                "/google.chat.v1.ChatService/GetSpaceNotificationSetting",
                request_serializer=space_notification_setting.GetSpaceNotificationSettingRequest.serialize,
                response_deserializer=space_notification_setting.SpaceNotificationSetting.deserialize,
            )
        return self._stubs["get_space_notification_setting"]

    @property
    def update_space_notification_setting(
        self,
    ) -> Callable[
        [gc_space_notification_setting.UpdateSpaceNotificationSettingRequest],
        Awaitable[gc_space_notification_setting.SpaceNotificationSetting],
    ]:
        r"""Return a callable for the update space notification
        setting method over gRPC.

        Updates the space notification setting. For an example, see
        `Update the caller's space notification
        setting <https://developers.google.com/workspace/chat/update-space-notification-setting>`__.

        Requires `user
        authentication <https://developers.google.com/workspace/chat/authenticate-authorize-chat-user>`__.

        Returns:
            Callable[[~.UpdateSpaceNotificationSettingRequest],
                    Awaitable[~.SpaceNotificationSetting]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_space_notification_setting" not in self._stubs:
            self._stubs[
                "update_space_notification_setting"
            ] = self._logged_channel.unary_unary(
                "/google.chat.v1.ChatService/UpdateSpaceNotificationSetting",
                request_serializer=gc_space_notification_setting.UpdateSpaceNotificationSettingRequest.serialize,
                response_deserializer=gc_space_notification_setting.SpaceNotificationSetting.deserialize,
            )
        return self._stubs["update_space_notification_setting"]

    def _prep_wrapped_messages(self, client_info):
        """Precompute the wrapped methods, overriding the base class method to use async wrappers."""
        self._wrapped_methods = {
            self.create_message: self._wrap_method(
                self.create_message,
                default_retry=retries.AsyncRetry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=30.0,
                ),
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.list_messages: self._wrap_method(
                self.list_messages,
                default_retry=retries.AsyncRetry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=30.0,
                ),
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.list_memberships: self._wrap_method(
                self.list_memberships,
                default_retry=retries.AsyncRetry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=30.0,
                ),
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.get_membership: self._wrap_method(
                self.get_membership,
                default_retry=retries.AsyncRetry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=30.0,
                ),
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.get_message: self._wrap_method(
                self.get_message,
                default_retry=retries.AsyncRetry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=30.0,
                ),
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.update_message: self._wrap_method(
                self.update_message,
                default_retry=retries.AsyncRetry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=30.0,
                ),
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.delete_message: self._wrap_method(
                self.delete_message,
                default_retry=retries.AsyncRetry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=30.0,
                ),
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.get_attachment: self._wrap_method(
                self.get_attachment,
                default_retry=retries.AsyncRetry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=30.0,
                ),
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.upload_attachment: self._wrap_method(
                self.upload_attachment,
                default_retry=retries.AsyncRetry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=30.0,
                ),
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.list_spaces: self._wrap_method(
                self.list_spaces,
                default_retry=retries.AsyncRetry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=30.0,
                ),
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.search_spaces: self._wrap_method(
                self.search_spaces,
                default_retry=retries.AsyncRetry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=30.0,
                ),
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.get_space: self._wrap_method(
                self.get_space,
                default_retry=retries.AsyncRetry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=30.0,
                ),
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.create_space: self._wrap_method(
                self.create_space,
                default_retry=retries.AsyncRetry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=30.0,
                ),
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.set_up_space: self._wrap_method(
                self.set_up_space,
                default_retry=retries.AsyncRetry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=30.0,
                ),
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.update_space: self._wrap_method(
                self.update_space,
                default_retry=retries.AsyncRetry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=30.0,
                ),
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.delete_space: self._wrap_method(
                self.delete_space,
                default_retry=retries.AsyncRetry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=30.0,
                ),
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.complete_import_space: self._wrap_method(
                self.complete_import_space,
                default_retry=retries.AsyncRetry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=30.0,
                ),
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.find_direct_message: self._wrap_method(
                self.find_direct_message,
                default_retry=retries.AsyncRetry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=30.0,
                ),
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.create_membership: self._wrap_method(
                self.create_membership,
                default_retry=retries.AsyncRetry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=30.0,
                ),
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.update_membership: self._wrap_method(
                self.update_membership,
                default_retry=retries.AsyncRetry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=30.0,
                ),
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.delete_membership: self._wrap_method(
                self.delete_membership,
                default_retry=retries.AsyncRetry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=30.0,
                ),
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.create_reaction: self._wrap_method(
                self.create_reaction,
                default_retry=retries.AsyncRetry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=30.0,
                ),
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.list_reactions: self._wrap_method(
                self.list_reactions,
                default_retry=retries.AsyncRetry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=30.0,
                ),
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.delete_reaction: self._wrap_method(
                self.delete_reaction,
                default_retry=retries.AsyncRetry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=30.0,
                ),
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.create_custom_emoji: self._wrap_method(
                self.create_custom_emoji,
                default_retry=retries.AsyncRetry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=30.0,
                ),
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.get_custom_emoji: self._wrap_method(
                self.get_custom_emoji,
                default_retry=retries.AsyncRetry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=30.0,
                ),
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.list_custom_emojis: self._wrap_method(
                self.list_custom_emojis,
                default_retry=retries.AsyncRetry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=30.0,
                ),
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.delete_custom_emoji: self._wrap_method(
                self.delete_custom_emoji,
                default_retry=retries.AsyncRetry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=30.0,
                ),
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.get_space_read_state: self._wrap_method(
                self.get_space_read_state,
                default_retry=retries.AsyncRetry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=30.0,
                ),
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.update_space_read_state: self._wrap_method(
                self.update_space_read_state,
                default_retry=retries.AsyncRetry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=30.0,
                ),
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.get_thread_read_state: self._wrap_method(
                self.get_thread_read_state,
                default_retry=retries.AsyncRetry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=30.0,
                ),
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.get_space_event: self._wrap_method(
                self.get_space_event,
                default_retry=retries.AsyncRetry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=30.0,
                ),
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.list_space_events: self._wrap_method(
                self.list_space_events,
                default_retry=retries.AsyncRetry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=30.0,
                ),
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.get_space_notification_setting: self._wrap_method(
                self.get_space_notification_setting,
                default_retry=retries.AsyncRetry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=30.0,
                ),
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.update_space_notification_setting: self._wrap_method(
                self.update_space_notification_setting,
                default_retry=retries.AsyncRetry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=30.0,
                ),
                default_timeout=30.0,
                client_info=client_info,
            ),
        }

    def _wrap_method(self, func, *args, **kwargs):
        if self._wrap_with_kind:  # pragma: NO COVER
            kwargs["kind"] = self.kind
        return gapic_v1.method_async.wrap_method(func, *args, **kwargs)

    def close(self):
        return self._logged_channel.close()

    @property
    def kind(self) -> str:
        return "grpc_asyncio"


__all__ = ("ChatServiceGrpcAsyncIOTransport",)
