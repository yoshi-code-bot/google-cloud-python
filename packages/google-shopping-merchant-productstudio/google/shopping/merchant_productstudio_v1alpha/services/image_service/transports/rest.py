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

from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1, rest_helpers, rest_streaming
from google.api_core import retry as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.requests import AuthorizedSession  # type: ignore
import google.protobuf
from google.protobuf import json_format
from requests import __version__ as requests_version

from google.shopping.merchant_productstudio_v1alpha.types import image

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .rest_base import _BaseImageServiceRestTransport

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


class ImageServiceRestInterceptor:
    """Interceptor for ImageService.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the ImageServiceRestTransport.

    .. code-block:: python
        class MyCustomImageServiceInterceptor(ImageServiceRestInterceptor):
            def pre_generate_product_image_background(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_generate_product_image_background(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_remove_product_image_background(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_remove_product_image_background(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_upscale_product_image(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_upscale_product_image(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = ImageServiceRestTransport(interceptor=MyCustomImageServiceInterceptor())
        client = ImageServiceClient(transport=transport)


    """

    def pre_generate_product_image_background(
        self,
        request: image.GenerateProductImageBackgroundRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        image.GenerateProductImageBackgroundRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for generate_product_image_background

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ImageService server.
        """
        return request, metadata

    def post_generate_product_image_background(
        self, response: image.GenerateProductImageBackgroundResponse
    ) -> image.GenerateProductImageBackgroundResponse:
        """Post-rpc interceptor for generate_product_image_background

        DEPRECATED. Please use the `post_generate_product_image_background_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the ImageService server but before
        it is returned to user code. This `post_generate_product_image_background` interceptor runs
        before the `post_generate_product_image_background_with_metadata` interceptor.
        """
        return response

    def post_generate_product_image_background_with_metadata(
        self,
        response: image.GenerateProductImageBackgroundResponse,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        image.GenerateProductImageBackgroundResponse,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Post-rpc interceptor for generate_product_image_background

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the ImageService server but before it is returned to user code.

        We recommend only using this `post_generate_product_image_background_with_metadata`
        interceptor in new development instead of the `post_generate_product_image_background` interceptor.
        When both interceptors are used, this `post_generate_product_image_background_with_metadata` interceptor runs after the
        `post_generate_product_image_background` interceptor. The (possibly modified) response returned by
        `post_generate_product_image_background` will be passed to
        `post_generate_product_image_background_with_metadata`.
        """
        return response, metadata

    def pre_remove_product_image_background(
        self,
        request: image.RemoveProductImageBackgroundRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        image.RemoveProductImageBackgroundRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for remove_product_image_background

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ImageService server.
        """
        return request, metadata

    def post_remove_product_image_background(
        self, response: image.RemoveProductImageBackgroundResponse
    ) -> image.RemoveProductImageBackgroundResponse:
        """Post-rpc interceptor for remove_product_image_background

        DEPRECATED. Please use the `post_remove_product_image_background_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the ImageService server but before
        it is returned to user code. This `post_remove_product_image_background` interceptor runs
        before the `post_remove_product_image_background_with_metadata` interceptor.
        """
        return response

    def post_remove_product_image_background_with_metadata(
        self,
        response: image.RemoveProductImageBackgroundResponse,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        image.RemoveProductImageBackgroundResponse,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Post-rpc interceptor for remove_product_image_background

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the ImageService server but before it is returned to user code.

        We recommend only using this `post_remove_product_image_background_with_metadata`
        interceptor in new development instead of the `post_remove_product_image_background` interceptor.
        When both interceptors are used, this `post_remove_product_image_background_with_metadata` interceptor runs after the
        `post_remove_product_image_background` interceptor. The (possibly modified) response returned by
        `post_remove_product_image_background` will be passed to
        `post_remove_product_image_background_with_metadata`.
        """
        return response, metadata

    def pre_upscale_product_image(
        self,
        request: image.UpscaleProductImageRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        image.UpscaleProductImageRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for upscale_product_image

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ImageService server.
        """
        return request, metadata

    def post_upscale_product_image(
        self, response: image.UpscaleProductImageResponse
    ) -> image.UpscaleProductImageResponse:
        """Post-rpc interceptor for upscale_product_image

        DEPRECATED. Please use the `post_upscale_product_image_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the ImageService server but before
        it is returned to user code. This `post_upscale_product_image` interceptor runs
        before the `post_upscale_product_image_with_metadata` interceptor.
        """
        return response

    def post_upscale_product_image_with_metadata(
        self,
        response: image.UpscaleProductImageResponse,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        image.UpscaleProductImageResponse, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Post-rpc interceptor for upscale_product_image

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the ImageService server but before it is returned to user code.

        We recommend only using this `post_upscale_product_image_with_metadata`
        interceptor in new development instead of the `post_upscale_product_image` interceptor.
        When both interceptors are used, this `post_upscale_product_image_with_metadata` interceptor runs after the
        `post_upscale_product_image` interceptor. The (possibly modified) response returned by
        `post_upscale_product_image` will be passed to
        `post_upscale_product_image_with_metadata`.
        """
        return response, metadata


@dataclasses.dataclass
class ImageServiceRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: ImageServiceRestInterceptor


class ImageServiceRestTransport(_BaseImageServiceRestTransport):
    """REST backend synchronous transport for ImageService.

    Service that exposes Generative AI (GenAI) endpoints for
    creating and enhancing product image content.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1
    """

    def __init__(
        self,
        *,
        host: str = "merchantapi.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[ImageServiceRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'merchantapi.googleapis.com').
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
        if client_cert_source_for_mtls:
            self._session.configure_mtls_channel(client_cert_source_for_mtls)
        self._interceptor = interceptor or ImageServiceRestInterceptor()
        self._prep_wrapped_messages(client_info)

    class _GenerateProductImageBackground(
        _BaseImageServiceRestTransport._BaseGenerateProductImageBackground,
        ImageServiceRestStub,
    ):
        def __hash__(self):
            return hash("ImageServiceRestTransport.GenerateProductImageBackground")

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
            request: image.GenerateProductImageBackgroundRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> image.GenerateProductImageBackgroundResponse:
            r"""Call the generate product image
            background method over HTTP.

                Args:
                    request (~.image.GenerateProductImageBackgroundRequest):
                        The request object. Request message for the
                    GenerateProductImageBackground method.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                        sent along with the request as metadata. Normally, each value must be of type `str`,
                        but for metadata keys ending with the suffix `-bin`, the corresponding values must
                        be of type `bytes`.

                Returns:
                    ~.image.GenerateProductImageBackgroundResponse:
                        Response message for the
                    GenerateProductImageBackground method.

            """

            http_options = (
                _BaseImageServiceRestTransport._BaseGenerateProductImageBackground._get_http_options()
            )

            request, metadata = self._interceptor.pre_generate_product_image_background(
                request, metadata
            )
            transcoded_request = _BaseImageServiceRestTransport._BaseGenerateProductImageBackground._get_transcoded_request(
                http_options, request
            )

            body = _BaseImageServiceRestTransport._BaseGenerateProductImageBackground._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseImageServiceRestTransport._BaseGenerateProductImageBackground._get_query_params_json(
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
                    f"Sending request for google.shopping.merchant.productstudio_v1alpha.ImageServiceClient.GenerateProductImageBackground",
                    extra={
                        "serviceName": "google.shopping.merchant.productstudio.v1alpha.ImageService",
                        "rpcName": "GenerateProductImageBackground",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = (
                ImageServiceRestTransport._GenerateProductImageBackground._get_response(
                    self._host,
                    metadata,
                    query_params,
                    self._session,
                    timeout,
                    transcoded_request,
                    body,
                )
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = image.GenerateProductImageBackgroundResponse()
            pb_resp = image.GenerateProductImageBackgroundResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_generate_product_image_background(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            (
                resp,
                _,
            ) = self._interceptor.post_generate_product_image_background_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = (
                        image.GenerateProductImageBackgroundResponse.to_json(response)
                    )
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.shopping.merchant.productstudio_v1alpha.ImageServiceClient.generate_product_image_background",
                    extra={
                        "serviceName": "google.shopping.merchant.productstudio.v1alpha.ImageService",
                        "rpcName": "GenerateProductImageBackground",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _RemoveProductImageBackground(
        _BaseImageServiceRestTransport._BaseRemoveProductImageBackground,
        ImageServiceRestStub,
    ):
        def __hash__(self):
            return hash("ImageServiceRestTransport.RemoveProductImageBackground")

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
            request: image.RemoveProductImageBackgroundRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> image.RemoveProductImageBackgroundResponse:
            r"""Call the remove product image
            background method over HTTP.

                Args:
                    request (~.image.RemoveProductImageBackgroundRequest):
                        The request object. Request message for the
                    RemoveProductImageBackground method.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                        sent along with the request as metadata. Normally, each value must be of type `str`,
                        but for metadata keys ending with the suffix `-bin`, the corresponding values must
                        be of type `bytes`.

                Returns:
                    ~.image.RemoveProductImageBackgroundResponse:
                        Response message for the
                    RemoveProductImageBackground method.

            """

            http_options = (
                _BaseImageServiceRestTransport._BaseRemoveProductImageBackground._get_http_options()
            )

            request, metadata = self._interceptor.pre_remove_product_image_background(
                request, metadata
            )
            transcoded_request = _BaseImageServiceRestTransport._BaseRemoveProductImageBackground._get_transcoded_request(
                http_options, request
            )

            body = _BaseImageServiceRestTransport._BaseRemoveProductImageBackground._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseImageServiceRestTransport._BaseRemoveProductImageBackground._get_query_params_json(
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
                    f"Sending request for google.shopping.merchant.productstudio_v1alpha.ImageServiceClient.RemoveProductImageBackground",
                    extra={
                        "serviceName": "google.shopping.merchant.productstudio.v1alpha.ImageService",
                        "rpcName": "RemoveProductImageBackground",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = (
                ImageServiceRestTransport._RemoveProductImageBackground._get_response(
                    self._host,
                    metadata,
                    query_params,
                    self._session,
                    timeout,
                    transcoded_request,
                    body,
                )
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = image.RemoveProductImageBackgroundResponse()
            pb_resp = image.RemoveProductImageBackgroundResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_remove_product_image_background(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            (
                resp,
                _,
            ) = self._interceptor.post_remove_product_image_background_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = (
                        image.RemoveProductImageBackgroundResponse.to_json(response)
                    )
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.shopping.merchant.productstudio_v1alpha.ImageServiceClient.remove_product_image_background",
                    extra={
                        "serviceName": "google.shopping.merchant.productstudio.v1alpha.ImageService",
                        "rpcName": "RemoveProductImageBackground",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _UpscaleProductImage(
        _BaseImageServiceRestTransport._BaseUpscaleProductImage, ImageServiceRestStub
    ):
        def __hash__(self):
            return hash("ImageServiceRestTransport.UpscaleProductImage")

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
            request: image.UpscaleProductImageRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> image.UpscaleProductImageResponse:
            r"""Call the upscale product image method over HTTP.

            Args:
                request (~.image.UpscaleProductImageRequest):
                    The request object. Request message for the
                UpscaleProductImage method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.image.UpscaleProductImageResponse:
                    Response message for the
                UpscaleProductImage method.

            """

            http_options = (
                _BaseImageServiceRestTransport._BaseUpscaleProductImage._get_http_options()
            )

            request, metadata = self._interceptor.pre_upscale_product_image(
                request, metadata
            )
            transcoded_request = _BaseImageServiceRestTransport._BaseUpscaleProductImage._get_transcoded_request(
                http_options, request
            )

            body = _BaseImageServiceRestTransport._BaseUpscaleProductImage._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseImageServiceRestTransport._BaseUpscaleProductImage._get_query_params_json(
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
                    f"Sending request for google.shopping.merchant.productstudio_v1alpha.ImageServiceClient.UpscaleProductImage",
                    extra={
                        "serviceName": "google.shopping.merchant.productstudio.v1alpha.ImageService",
                        "rpcName": "UpscaleProductImage",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = ImageServiceRestTransport._UpscaleProductImage._get_response(
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
            resp = image.UpscaleProductImageResponse()
            pb_resp = image.UpscaleProductImageResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_upscale_product_image(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_upscale_product_image_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = image.UpscaleProductImageResponse.to_json(
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
                    "Received response for google.shopping.merchant.productstudio_v1alpha.ImageServiceClient.upscale_product_image",
                    extra={
                        "serviceName": "google.shopping.merchant.productstudio.v1alpha.ImageService",
                        "rpcName": "UpscaleProductImage",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    @property
    def generate_product_image_background(
        self,
    ) -> Callable[
        [image.GenerateProductImageBackgroundRequest],
        image.GenerateProductImageBackgroundResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GenerateProductImageBackground(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def remove_product_image_background(
        self,
    ) -> Callable[
        [image.RemoveProductImageBackgroundRequest],
        image.RemoveProductImageBackgroundResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._RemoveProductImageBackground(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def upscale_product_image(
        self,
    ) -> Callable[
        [image.UpscaleProductImageRequest], image.UpscaleProductImageResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpscaleProductImage(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("ImageServiceRestTransport",)
