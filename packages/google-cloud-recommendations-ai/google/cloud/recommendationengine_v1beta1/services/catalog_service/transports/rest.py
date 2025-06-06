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
import dataclasses
import json  # type: ignore
import logging
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union
import warnings

from google.api_core import gapic_v1, operations_v1, rest_helpers, rest_streaming
from google.api_core import exceptions as core_exceptions
from google.api_core import retry as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.requests import AuthorizedSession  # type: ignore
from google.longrunning import operations_pb2  # type: ignore
import google.protobuf
from google.protobuf import empty_pb2  # type: ignore
from google.protobuf import json_format
from requests import __version__ as requests_version

from google.cloud.recommendationengine_v1beta1.types import (
    catalog,
    catalog_service,
    import_,
)

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .rest_base import _BaseCatalogServiceRestTransport

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore

try:
    from google.api_core import client_logging  # type: ignore

    CLIENT_LOGGING_SUPPORTED = True  # pragma: NO COVER
except ImportError:  # pragma: NO COVER
    CLIENT_LOGGING_SUPPORTED = False

_LOGGER = logging.getLogger(__name__)

DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=f"requests@{requests_version}",
)

if hasattr(DEFAULT_CLIENT_INFO, "protobuf_runtime_version"):  # pragma: NO COVER
    DEFAULT_CLIENT_INFO.protobuf_runtime_version = google.protobuf.__version__


class CatalogServiceRestInterceptor:
    """Interceptor for CatalogService.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the CatalogServiceRestTransport.

    .. code-block:: python
        class MyCustomCatalogServiceInterceptor(CatalogServiceRestInterceptor):
            def pre_create_catalog_item(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_catalog_item(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_catalog_item(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_get_catalog_item(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_catalog_item(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_import_catalog_items(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_import_catalog_items(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_catalog_items(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_catalog_items(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_catalog_item(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_catalog_item(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = CatalogServiceRestTransport(interceptor=MyCustomCatalogServiceInterceptor())
        client = CatalogServiceClient(transport=transport)


    """

    def pre_create_catalog_item(
        self,
        request: catalog_service.CreateCatalogItemRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        catalog_service.CreateCatalogItemRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for create_catalog_item

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CatalogService server.
        """
        return request, metadata

    def post_create_catalog_item(
        self, response: catalog.CatalogItem
    ) -> catalog.CatalogItem:
        """Post-rpc interceptor for create_catalog_item

        DEPRECATED. Please use the `post_create_catalog_item_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the CatalogService server but before
        it is returned to user code. This `post_create_catalog_item` interceptor runs
        before the `post_create_catalog_item_with_metadata` interceptor.
        """
        return response

    def post_create_catalog_item_with_metadata(
        self,
        response: catalog.CatalogItem,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[catalog.CatalogItem, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for create_catalog_item

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the CatalogService server but before it is returned to user code.

        We recommend only using this `post_create_catalog_item_with_metadata`
        interceptor in new development instead of the `post_create_catalog_item` interceptor.
        When both interceptors are used, this `post_create_catalog_item_with_metadata` interceptor runs after the
        `post_create_catalog_item` interceptor. The (possibly modified) response returned by
        `post_create_catalog_item` will be passed to
        `post_create_catalog_item_with_metadata`.
        """
        return response, metadata

    def pre_delete_catalog_item(
        self,
        request: catalog_service.DeleteCatalogItemRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        catalog_service.DeleteCatalogItemRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for delete_catalog_item

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CatalogService server.
        """
        return request, metadata

    def pre_get_catalog_item(
        self,
        request: catalog_service.GetCatalogItemRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        catalog_service.GetCatalogItemRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for get_catalog_item

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CatalogService server.
        """
        return request, metadata

    def post_get_catalog_item(
        self, response: catalog.CatalogItem
    ) -> catalog.CatalogItem:
        """Post-rpc interceptor for get_catalog_item

        DEPRECATED. Please use the `post_get_catalog_item_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the CatalogService server but before
        it is returned to user code. This `post_get_catalog_item` interceptor runs
        before the `post_get_catalog_item_with_metadata` interceptor.
        """
        return response

    def post_get_catalog_item_with_metadata(
        self,
        response: catalog.CatalogItem,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[catalog.CatalogItem, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for get_catalog_item

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the CatalogService server but before it is returned to user code.

        We recommend only using this `post_get_catalog_item_with_metadata`
        interceptor in new development instead of the `post_get_catalog_item` interceptor.
        When both interceptors are used, this `post_get_catalog_item_with_metadata` interceptor runs after the
        `post_get_catalog_item` interceptor. The (possibly modified) response returned by
        `post_get_catalog_item` will be passed to
        `post_get_catalog_item_with_metadata`.
        """
        return response, metadata

    def pre_import_catalog_items(
        self,
        request: import_.ImportCatalogItemsRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        import_.ImportCatalogItemsRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for import_catalog_items

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CatalogService server.
        """
        return request, metadata

    def post_import_catalog_items(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for import_catalog_items

        DEPRECATED. Please use the `post_import_catalog_items_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the CatalogService server but before
        it is returned to user code. This `post_import_catalog_items` interceptor runs
        before the `post_import_catalog_items_with_metadata` interceptor.
        """
        return response

    def post_import_catalog_items_with_metadata(
        self,
        response: operations_pb2.Operation,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[operations_pb2.Operation, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for import_catalog_items

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the CatalogService server but before it is returned to user code.

        We recommend only using this `post_import_catalog_items_with_metadata`
        interceptor in new development instead of the `post_import_catalog_items` interceptor.
        When both interceptors are used, this `post_import_catalog_items_with_metadata` interceptor runs after the
        `post_import_catalog_items` interceptor. The (possibly modified) response returned by
        `post_import_catalog_items` will be passed to
        `post_import_catalog_items_with_metadata`.
        """
        return response, metadata

    def pre_list_catalog_items(
        self,
        request: catalog_service.ListCatalogItemsRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        catalog_service.ListCatalogItemsRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for list_catalog_items

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CatalogService server.
        """
        return request, metadata

    def post_list_catalog_items(
        self, response: catalog_service.ListCatalogItemsResponse
    ) -> catalog_service.ListCatalogItemsResponse:
        """Post-rpc interceptor for list_catalog_items

        DEPRECATED. Please use the `post_list_catalog_items_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the CatalogService server but before
        it is returned to user code. This `post_list_catalog_items` interceptor runs
        before the `post_list_catalog_items_with_metadata` interceptor.
        """
        return response

    def post_list_catalog_items_with_metadata(
        self,
        response: catalog_service.ListCatalogItemsResponse,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        catalog_service.ListCatalogItemsResponse,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Post-rpc interceptor for list_catalog_items

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the CatalogService server but before it is returned to user code.

        We recommend only using this `post_list_catalog_items_with_metadata`
        interceptor in new development instead of the `post_list_catalog_items` interceptor.
        When both interceptors are used, this `post_list_catalog_items_with_metadata` interceptor runs after the
        `post_list_catalog_items` interceptor. The (possibly modified) response returned by
        `post_list_catalog_items` will be passed to
        `post_list_catalog_items_with_metadata`.
        """
        return response, metadata

    def pre_update_catalog_item(
        self,
        request: catalog_service.UpdateCatalogItemRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        catalog_service.UpdateCatalogItemRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for update_catalog_item

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CatalogService server.
        """
        return request, metadata

    def post_update_catalog_item(
        self, response: catalog.CatalogItem
    ) -> catalog.CatalogItem:
        """Post-rpc interceptor for update_catalog_item

        DEPRECATED. Please use the `post_update_catalog_item_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the CatalogService server but before
        it is returned to user code. This `post_update_catalog_item` interceptor runs
        before the `post_update_catalog_item_with_metadata` interceptor.
        """
        return response

    def post_update_catalog_item_with_metadata(
        self,
        response: catalog.CatalogItem,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[catalog.CatalogItem, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for update_catalog_item

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the CatalogService server but before it is returned to user code.

        We recommend only using this `post_update_catalog_item_with_metadata`
        interceptor in new development instead of the `post_update_catalog_item` interceptor.
        When both interceptors are used, this `post_update_catalog_item_with_metadata` interceptor runs after the
        `post_update_catalog_item` interceptor. The (possibly modified) response returned by
        `post_update_catalog_item` will be passed to
        `post_update_catalog_item_with_metadata`.
        """
        return response, metadata


@dataclasses.dataclass
class CatalogServiceRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: CatalogServiceRestInterceptor


class CatalogServiceRestTransport(_BaseCatalogServiceRestTransport):
    """REST backend synchronous transport for CatalogService.

    Service for ingesting catalog information of the customer's
    website.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1
    """

    def __init__(
        self,
        *,
        host: str = "recommendationengine.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[CatalogServiceRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'recommendationengine.googleapis.com').
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.

            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is ignored if ``channel`` is provided.
            scopes (Optional(Sequence[str])): A list of scopes. This argument is
                ignored if ``channel`` is provided.
            client_cert_source_for_mtls (Callable[[], Tuple[bytes, bytes]]): Client
                certificate to configure mutual TLS HTTP channel. It is ignored
                if ``channel`` is provided.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you are developing
                your own client library.
            always_use_jwt_access (Optional[bool]): Whether self signed JWT should
                be used for service account credentials.
            url_scheme: the protocol scheme for the API endpoint.  Normally
                "https", but for testing or local servers,
                "http" can be specified.
        """
        # Run the base constructor
        # TODO(yon-mg): resolve other ctor params i.e. scopes, quota, etc.
        # TODO: When custom host (api_endpoint) is set, `scopes` must *also* be set on the
        # credentials object
        super().__init__(
            host=host,
            credentials=credentials,
            client_info=client_info,
            always_use_jwt_access=always_use_jwt_access,
            url_scheme=url_scheme,
            api_audience=api_audience,
        )
        self._session = AuthorizedSession(
            self._credentials, default_host=self.DEFAULT_HOST
        )
        self._operations_client: Optional[operations_v1.AbstractOperationsClient] = None
        if client_cert_source_for_mtls:
            self._session.configure_mtls_channel(client_cert_source_for_mtls)
        self._interceptor = interceptor or CatalogServiceRestInterceptor()
        self._prep_wrapped_messages(client_info)

    @property
    def operations_client(self) -> operations_v1.AbstractOperationsClient:
        """Create the client designed to process long-running operations.

        This property caches on the instance; repeated calls return the same
        client.
        """
        # Only create a new client if we do not already have one.
        if self._operations_client is None:
            http_options: Dict[str, List[Dict[str, str]]] = {
                "google.longrunning.Operations.GetOperation": [
                    {
                        "method": "get",
                        "uri": "/v1beta1/{name=projects/*/locations/*/catalogs/*/operations/*}",
                    },
                    {
                        "method": "get",
                        "uri": "/v1beta1/{name=projects/*/locations/*/catalogs/*/eventStores/*/operations/*}",
                    },
                ],
                "google.longrunning.Operations.ListOperations": [
                    {
                        "method": "get",
                        "uri": "/v1beta1/{name=projects/*/locations/*/catalogs/*}/operations",
                    },
                    {
                        "method": "get",
                        "uri": "/v1beta1/{name=projects/*/locations/*/catalogs/*/eventStores/*}/operations",
                    },
                ],
            }

            rest_transport = operations_v1.OperationsRestTransport(
                host=self._host,
                # use the credentials which are saved
                credentials=self._credentials,
                scopes=self._scopes,
                http_options=http_options,
                path_prefix="v1beta1",
            )

            self._operations_client = operations_v1.AbstractOperationsClient(
                transport=rest_transport
            )

        # Return the client from cache.
        return self._operations_client

    class _CreateCatalogItem(
        _BaseCatalogServiceRestTransport._BaseCreateCatalogItem, CatalogServiceRestStub
    ):
        def __hash__(self):
            return hash("CatalogServiceRestTransport.CreateCatalogItem")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )
            return response

        def __call__(
            self,
            request: catalog_service.CreateCatalogItemRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> catalog.CatalogItem:
            r"""Call the create catalog item method over HTTP.

            Args:
                request (~.catalog_service.CreateCatalogItemRequest):
                    The request object. Request message for CreateCatalogItem
                method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.catalog.CatalogItem:
                    CatalogItem captures all metadata
                information of items to be recommended.

            """

            http_options = (
                _BaseCatalogServiceRestTransport._BaseCreateCatalogItem._get_http_options()
            )

            request, metadata = self._interceptor.pre_create_catalog_item(
                request, metadata
            )
            transcoded_request = _BaseCatalogServiceRestTransport._BaseCreateCatalogItem._get_transcoded_request(
                http_options, request
            )

            body = _BaseCatalogServiceRestTransport._BaseCreateCatalogItem._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseCatalogServiceRestTransport._BaseCreateCatalogItem._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.recommendationengine_v1beta1.CatalogServiceClient.CreateCatalogItem",
                    extra={
                        "serviceName": "google.cloud.recommendationengine.v1beta1.CatalogService",
                        "rpcName": "CreateCatalogItem",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = CatalogServiceRestTransport._CreateCatalogItem._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
                body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = catalog.CatalogItem()
            pb_resp = catalog.CatalogItem.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_create_catalog_item(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_create_catalog_item_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = catalog.CatalogItem.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.recommendationengine_v1beta1.CatalogServiceClient.create_catalog_item",
                    extra={
                        "serviceName": "google.cloud.recommendationengine.v1beta1.CatalogService",
                        "rpcName": "CreateCatalogItem",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _DeleteCatalogItem(
        _BaseCatalogServiceRestTransport._BaseDeleteCatalogItem, CatalogServiceRestStub
    ):
        def __hash__(self):
            return hash("CatalogServiceRestTransport.DeleteCatalogItem")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: catalog_service.DeleteCatalogItemRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ):
            r"""Call the delete catalog item method over HTTP.

            Args:
                request (~.catalog_service.DeleteCatalogItemRequest):
                    The request object. Request message for DeleteCatalogItem
                method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.
            """

            http_options = (
                _BaseCatalogServiceRestTransport._BaseDeleteCatalogItem._get_http_options()
            )

            request, metadata = self._interceptor.pre_delete_catalog_item(
                request, metadata
            )
            transcoded_request = _BaseCatalogServiceRestTransport._BaseDeleteCatalogItem._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseCatalogServiceRestTransport._BaseDeleteCatalogItem._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = json_format.MessageToJson(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.recommendationengine_v1beta1.CatalogServiceClient.DeleteCatalogItem",
                    extra={
                        "serviceName": "google.cloud.recommendationengine.v1beta1.CatalogService",
                        "rpcName": "DeleteCatalogItem",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = CatalogServiceRestTransport._DeleteCatalogItem._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

    class _GetCatalogItem(
        _BaseCatalogServiceRestTransport._BaseGetCatalogItem, CatalogServiceRestStub
    ):
        def __hash__(self):
            return hash("CatalogServiceRestTransport.GetCatalogItem")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: catalog_service.GetCatalogItemRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> catalog.CatalogItem:
            r"""Call the get catalog item method over HTTP.

            Args:
                request (~.catalog_service.GetCatalogItemRequest):
                    The request object. Request message for GetCatalogItem
                method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.catalog.CatalogItem:
                    CatalogItem captures all metadata
                information of items to be recommended.

            """

            http_options = (
                _BaseCatalogServiceRestTransport._BaseGetCatalogItem._get_http_options()
            )

            request, metadata = self._interceptor.pre_get_catalog_item(
                request, metadata
            )
            transcoded_request = _BaseCatalogServiceRestTransport._BaseGetCatalogItem._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseCatalogServiceRestTransport._BaseGetCatalogItem._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.recommendationengine_v1beta1.CatalogServiceClient.GetCatalogItem",
                    extra={
                        "serviceName": "google.cloud.recommendationengine.v1beta1.CatalogService",
                        "rpcName": "GetCatalogItem",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = CatalogServiceRestTransport._GetCatalogItem._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = catalog.CatalogItem()
            pb_resp = catalog.CatalogItem.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_get_catalog_item(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_get_catalog_item_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = catalog.CatalogItem.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.recommendationengine_v1beta1.CatalogServiceClient.get_catalog_item",
                    extra={
                        "serviceName": "google.cloud.recommendationengine.v1beta1.CatalogService",
                        "rpcName": "GetCatalogItem",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _ImportCatalogItems(
        _BaseCatalogServiceRestTransport._BaseImportCatalogItems, CatalogServiceRestStub
    ):
        def __hash__(self):
            return hash("CatalogServiceRestTransport.ImportCatalogItems")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )
            return response

        def __call__(
            self,
            request: import_.ImportCatalogItemsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the import catalog items method over HTTP.

            Args:
                request (~.import_.ImportCatalogItemsRequest):
                    The request object. Request message for Import methods.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options = (
                _BaseCatalogServiceRestTransport._BaseImportCatalogItems._get_http_options()
            )

            request, metadata = self._interceptor.pre_import_catalog_items(
                request, metadata
            )
            transcoded_request = _BaseCatalogServiceRestTransport._BaseImportCatalogItems._get_transcoded_request(
                http_options, request
            )

            body = _BaseCatalogServiceRestTransport._BaseImportCatalogItems._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseCatalogServiceRestTransport._BaseImportCatalogItems._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = json_format.MessageToJson(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.recommendationengine_v1beta1.CatalogServiceClient.ImportCatalogItems",
                    extra={
                        "serviceName": "google.cloud.recommendationengine.v1beta1.CatalogService",
                        "rpcName": "ImportCatalogItems",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = CatalogServiceRestTransport._ImportCatalogItems._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
                body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_import_catalog_items(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_import_catalog_items_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = json_format.MessageToJson(resp)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.recommendationengine_v1beta1.CatalogServiceClient.import_catalog_items",
                    extra={
                        "serviceName": "google.cloud.recommendationengine.v1beta1.CatalogService",
                        "rpcName": "ImportCatalogItems",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _ListCatalogItems(
        _BaseCatalogServiceRestTransport._BaseListCatalogItems, CatalogServiceRestStub
    ):
        def __hash__(self):
            return hash("CatalogServiceRestTransport.ListCatalogItems")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: catalog_service.ListCatalogItemsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> catalog_service.ListCatalogItemsResponse:
            r"""Call the list catalog items method over HTTP.

            Args:
                request (~.catalog_service.ListCatalogItemsRequest):
                    The request object. Request message for ListCatalogItems
                method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.catalog_service.ListCatalogItemsResponse:
                    Response message for ListCatalogItems
                method.

            """

            http_options = (
                _BaseCatalogServiceRestTransport._BaseListCatalogItems._get_http_options()
            )

            request, metadata = self._interceptor.pre_list_catalog_items(
                request, metadata
            )
            transcoded_request = _BaseCatalogServiceRestTransport._BaseListCatalogItems._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseCatalogServiceRestTransport._BaseListCatalogItems._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.recommendationengine_v1beta1.CatalogServiceClient.ListCatalogItems",
                    extra={
                        "serviceName": "google.cloud.recommendationengine.v1beta1.CatalogService",
                        "rpcName": "ListCatalogItems",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = CatalogServiceRestTransport._ListCatalogItems._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = catalog_service.ListCatalogItemsResponse()
            pb_resp = catalog_service.ListCatalogItemsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_list_catalog_items(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_list_catalog_items_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = catalog_service.ListCatalogItemsResponse.to_json(
                        response
                    )
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.recommendationengine_v1beta1.CatalogServiceClient.list_catalog_items",
                    extra={
                        "serviceName": "google.cloud.recommendationengine.v1beta1.CatalogService",
                        "rpcName": "ListCatalogItems",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _UpdateCatalogItem(
        _BaseCatalogServiceRestTransport._BaseUpdateCatalogItem, CatalogServiceRestStub
    ):
        def __hash__(self):
            return hash("CatalogServiceRestTransport.UpdateCatalogItem")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )
            return response

        def __call__(
            self,
            request: catalog_service.UpdateCatalogItemRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> catalog.CatalogItem:
            r"""Call the update catalog item method over HTTP.

            Args:
                request (~.catalog_service.UpdateCatalogItemRequest):
                    The request object. Request message for UpdateCatalogItem
                method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.catalog.CatalogItem:
                    CatalogItem captures all metadata
                information of items to be recommended.

            """

            http_options = (
                _BaseCatalogServiceRestTransport._BaseUpdateCatalogItem._get_http_options()
            )

            request, metadata = self._interceptor.pre_update_catalog_item(
                request, metadata
            )
            transcoded_request = _BaseCatalogServiceRestTransport._BaseUpdateCatalogItem._get_transcoded_request(
                http_options, request
            )

            body = _BaseCatalogServiceRestTransport._BaseUpdateCatalogItem._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseCatalogServiceRestTransport._BaseUpdateCatalogItem._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.recommendationengine_v1beta1.CatalogServiceClient.UpdateCatalogItem",
                    extra={
                        "serviceName": "google.cloud.recommendationengine.v1beta1.CatalogService",
                        "rpcName": "UpdateCatalogItem",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = CatalogServiceRestTransport._UpdateCatalogItem._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
                body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = catalog.CatalogItem()
            pb_resp = catalog.CatalogItem.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_update_catalog_item(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_update_catalog_item_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = catalog.CatalogItem.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.recommendationengine_v1beta1.CatalogServiceClient.update_catalog_item",
                    extra={
                        "serviceName": "google.cloud.recommendationengine.v1beta1.CatalogService",
                        "rpcName": "UpdateCatalogItem",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    @property
    def create_catalog_item(
        self,
    ) -> Callable[[catalog_service.CreateCatalogItemRequest], catalog.CatalogItem]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateCatalogItem(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_catalog_item(
        self,
    ) -> Callable[[catalog_service.DeleteCatalogItemRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteCatalogItem(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_catalog_item(
        self,
    ) -> Callable[[catalog_service.GetCatalogItemRequest], catalog.CatalogItem]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetCatalogItem(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def import_catalog_items(
        self,
    ) -> Callable[[import_.ImportCatalogItemsRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ImportCatalogItems(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_catalog_items(
        self,
    ) -> Callable[
        [catalog_service.ListCatalogItemsRequest],
        catalog_service.ListCatalogItemsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListCatalogItems(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_catalog_item(
        self,
    ) -> Callable[[catalog_service.UpdateCatalogItemRequest], catalog.CatalogItem]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateCatalogItem(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("CatalogServiceRestTransport",)
