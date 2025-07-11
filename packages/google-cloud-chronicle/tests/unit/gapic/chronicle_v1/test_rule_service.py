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
import os
import re

# try/except added for compatibility with python < 3.8
try:
    from unittest import mock
    from unittest.mock import AsyncMock  # pragma: NO COVER
except ImportError:  # pragma: NO COVER
    import mock

from collections.abc import AsyncIterable, Iterable
import json
import math

from google.api_core import api_core_version
from google.protobuf import json_format
import grpc
from grpc.experimental import aio
from proto.marshal.rules import wrappers
from proto.marshal.rules.dates import DurationRule, TimestampRule
import pytest
from requests import PreparedRequest, Request, Response
from requests.sessions import Session

try:
    from google.auth.aio import credentials as ga_credentials_async

    HAS_GOOGLE_AUTH_AIO = True
except ImportError:  # pragma: NO COVER
    HAS_GOOGLE_AUTH_AIO = False

from google.api_core import (
    future,
    gapic_v1,
    grpc_helpers,
    grpc_helpers_async,
    operation,
    operations_v1,
    path_template,
)
from google.api_core import client_options
from google.api_core import exceptions as core_exceptions
from google.api_core import operation_async  # type: ignore
from google.api_core import retry as retries
import google.auth
from google.auth import credentials as ga_credentials
from google.auth.exceptions import MutualTLSChannelError
from google.longrunning import operations_pb2  # type: ignore
from google.oauth2 import service_account
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
from google.type import interval_pb2  # type: ignore

from google.cloud.chronicle_v1.services.rule_service import (
    RuleServiceAsyncClient,
    RuleServiceClient,
    pagers,
    transports,
)
from google.cloud.chronicle_v1.types import rule
from google.cloud.chronicle_v1.types import rule as gcc_rule

CRED_INFO_JSON = {
    "credential_source": "/path/to/file",
    "credential_type": "service account credentials",
    "principal": "service-account@example.com",
}
CRED_INFO_STRING = json.dumps(CRED_INFO_JSON)


async def mock_async_gen(data, chunk_size=1):
    for i in range(0, len(data)):  # pragma: NO COVER
        chunk = data[i : i + chunk_size]
        yield chunk.encode("utf-8")


def client_cert_source_callback():
    return b"cert bytes", b"key bytes"


# TODO: use async auth anon credentials by default once the minimum version of google-auth is upgraded.
# See related issue: https://github.com/googleapis/gapic-generator-python/issues/2107.
def async_anonymous_credentials():
    if HAS_GOOGLE_AUTH_AIO:
        return ga_credentials_async.AnonymousCredentials()
    return ga_credentials.AnonymousCredentials()


# If default endpoint is localhost, then default mtls endpoint will be the same.
# This method modifies the default endpoint so the client can produce a different
# mtls endpoint for endpoint testing purposes.
def modify_default_endpoint(client):
    return (
        "foo.googleapis.com"
        if ("localhost" in client.DEFAULT_ENDPOINT)
        else client.DEFAULT_ENDPOINT
    )


# If default endpoint template is localhost, then default mtls endpoint will be the same.
# This method modifies the default endpoint template so the client can produce a different
# mtls endpoint for endpoint testing purposes.
def modify_default_endpoint_template(client):
    return (
        "test.{UNIVERSE_DOMAIN}"
        if ("localhost" in client._DEFAULT_ENDPOINT_TEMPLATE)
        else client._DEFAULT_ENDPOINT_TEMPLATE
    )


def test__get_default_mtls_endpoint():
    api_endpoint = "example.googleapis.com"
    api_mtls_endpoint = "example.mtls.googleapis.com"
    sandbox_endpoint = "example.sandbox.googleapis.com"
    sandbox_mtls_endpoint = "example.mtls.sandbox.googleapis.com"
    non_googleapi = "api.example.com"

    assert RuleServiceClient._get_default_mtls_endpoint(None) is None
    assert (
        RuleServiceClient._get_default_mtls_endpoint(api_endpoint) == api_mtls_endpoint
    )
    assert (
        RuleServiceClient._get_default_mtls_endpoint(api_mtls_endpoint)
        == api_mtls_endpoint
    )
    assert (
        RuleServiceClient._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        RuleServiceClient._get_default_mtls_endpoint(sandbox_mtls_endpoint)
        == sandbox_mtls_endpoint
    )
    assert RuleServiceClient._get_default_mtls_endpoint(non_googleapi) == non_googleapi


def test__read_environment_variables():
    assert RuleServiceClient._read_environment_variables() == (False, "auto", None)

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        assert RuleServiceClient._read_environment_variables() == (True, "auto", None)

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "false"}):
        assert RuleServiceClient._read_environment_variables() == (False, "auto", None)

    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "Unsupported"}
    ):
        with pytest.raises(ValueError) as excinfo:
            RuleServiceClient._read_environment_variables()
    assert (
        str(excinfo.value)
        == "Environment variable `GOOGLE_API_USE_CLIENT_CERTIFICATE` must be either `true` or `false`"
    )

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}):
        assert RuleServiceClient._read_environment_variables() == (False, "never", None)

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "always"}):
        assert RuleServiceClient._read_environment_variables() == (
            False,
            "always",
            None,
        )

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"}):
        assert RuleServiceClient._read_environment_variables() == (False, "auto", None)

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "Unsupported"}):
        with pytest.raises(MutualTLSChannelError) as excinfo:
            RuleServiceClient._read_environment_variables()
    assert (
        str(excinfo.value)
        == "Environment variable `GOOGLE_API_USE_MTLS_ENDPOINT` must be `never`, `auto` or `always`"
    )

    with mock.patch.dict(os.environ, {"GOOGLE_CLOUD_UNIVERSE_DOMAIN": "foo.com"}):
        assert RuleServiceClient._read_environment_variables() == (
            False,
            "auto",
            "foo.com",
        )


def test__get_client_cert_source():
    mock_provided_cert_source = mock.Mock()
    mock_default_cert_source = mock.Mock()

    assert RuleServiceClient._get_client_cert_source(None, False) is None
    assert (
        RuleServiceClient._get_client_cert_source(mock_provided_cert_source, False)
        is None
    )
    assert (
        RuleServiceClient._get_client_cert_source(mock_provided_cert_source, True)
        == mock_provided_cert_source
    )

    with mock.patch(
        "google.auth.transport.mtls.has_default_client_cert_source", return_value=True
    ):
        with mock.patch(
            "google.auth.transport.mtls.default_client_cert_source",
            return_value=mock_default_cert_source,
        ):
            assert (
                RuleServiceClient._get_client_cert_source(None, True)
                is mock_default_cert_source
            )
            assert (
                RuleServiceClient._get_client_cert_source(
                    mock_provided_cert_source, "true"
                )
                is mock_provided_cert_source
            )


@mock.patch.object(
    RuleServiceClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(RuleServiceClient),
)
@mock.patch.object(
    RuleServiceAsyncClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(RuleServiceAsyncClient),
)
def test__get_api_endpoint():
    api_override = "foo.com"
    mock_client_cert_source = mock.Mock()
    default_universe = RuleServiceClient._DEFAULT_UNIVERSE
    default_endpoint = RuleServiceClient._DEFAULT_ENDPOINT_TEMPLATE.format(
        UNIVERSE_DOMAIN=default_universe
    )
    mock_universe = "bar.com"
    mock_endpoint = RuleServiceClient._DEFAULT_ENDPOINT_TEMPLATE.format(
        UNIVERSE_DOMAIN=mock_universe
    )

    assert (
        RuleServiceClient._get_api_endpoint(
            api_override, mock_client_cert_source, default_universe, "always"
        )
        == api_override
    )
    assert (
        RuleServiceClient._get_api_endpoint(
            None, mock_client_cert_source, default_universe, "auto"
        )
        == RuleServiceClient.DEFAULT_MTLS_ENDPOINT
    )
    assert (
        RuleServiceClient._get_api_endpoint(None, None, default_universe, "auto")
        == default_endpoint
    )
    assert (
        RuleServiceClient._get_api_endpoint(None, None, default_universe, "always")
        == RuleServiceClient.DEFAULT_MTLS_ENDPOINT
    )
    assert (
        RuleServiceClient._get_api_endpoint(
            None, mock_client_cert_source, default_universe, "always"
        )
        == RuleServiceClient.DEFAULT_MTLS_ENDPOINT
    )
    assert (
        RuleServiceClient._get_api_endpoint(None, None, mock_universe, "never")
        == mock_endpoint
    )
    assert (
        RuleServiceClient._get_api_endpoint(None, None, default_universe, "never")
        == default_endpoint
    )

    with pytest.raises(MutualTLSChannelError) as excinfo:
        RuleServiceClient._get_api_endpoint(
            None, mock_client_cert_source, mock_universe, "auto"
        )
    assert (
        str(excinfo.value)
        == "mTLS is not supported in any universe other than googleapis.com."
    )


def test__get_universe_domain():
    client_universe_domain = "foo.com"
    universe_domain_env = "bar.com"

    assert (
        RuleServiceClient._get_universe_domain(
            client_universe_domain, universe_domain_env
        )
        == client_universe_domain
    )
    assert (
        RuleServiceClient._get_universe_domain(None, universe_domain_env)
        == universe_domain_env
    )
    assert (
        RuleServiceClient._get_universe_domain(None, None)
        == RuleServiceClient._DEFAULT_UNIVERSE
    )

    with pytest.raises(ValueError) as excinfo:
        RuleServiceClient._get_universe_domain("", None)
    assert str(excinfo.value) == "Universe Domain cannot be an empty string."


@pytest.mark.parametrize(
    "error_code,cred_info_json,show_cred_info",
    [
        (401, CRED_INFO_JSON, True),
        (403, CRED_INFO_JSON, True),
        (404, CRED_INFO_JSON, True),
        (500, CRED_INFO_JSON, False),
        (401, None, False),
        (403, None, False),
        (404, None, False),
        (500, None, False),
    ],
)
def test__add_cred_info_for_auth_errors(error_code, cred_info_json, show_cred_info):
    cred = mock.Mock(["get_cred_info"])
    cred.get_cred_info = mock.Mock(return_value=cred_info_json)
    client = RuleServiceClient(credentials=cred)
    client._transport._credentials = cred

    error = core_exceptions.GoogleAPICallError("message", details=["foo"])
    error.code = error_code

    client._add_cred_info_for_auth_errors(error)
    if show_cred_info:
        assert error.details == ["foo", CRED_INFO_STRING]
    else:
        assert error.details == ["foo"]


@pytest.mark.parametrize("error_code", [401, 403, 404, 500])
def test__add_cred_info_for_auth_errors_no_get_cred_info(error_code):
    cred = mock.Mock([])
    assert not hasattr(cred, "get_cred_info")
    client = RuleServiceClient(credentials=cred)
    client._transport._credentials = cred

    error = core_exceptions.GoogleAPICallError("message", details=[])
    error.code = error_code

    client._add_cred_info_for_auth_errors(error)
    assert error.details == []


@pytest.mark.parametrize(
    "client_class,transport_name",
    [
        (RuleServiceClient, "grpc"),
        (RuleServiceAsyncClient, "grpc_asyncio"),
        (RuleServiceClient, "rest"),
    ],
)
def test_rule_service_client_from_service_account_info(client_class, transport_name):
    creds = ga_credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_info"
    ) as factory:
        factory.return_value = creds
        info = {"valid": True}
        client = client_class.from_service_account_info(info, transport=transport_name)
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        assert client.transport._host == (
            "chronicle.googleapis.com:443"
            if transport_name in ["grpc", "grpc_asyncio"]
            else "https://chronicle.googleapis.com"
        )


@pytest.mark.parametrize(
    "transport_class,transport_name",
    [
        (transports.RuleServiceGrpcTransport, "grpc"),
        (transports.RuleServiceGrpcAsyncIOTransport, "grpc_asyncio"),
        (transports.RuleServiceRestTransport, "rest"),
    ],
)
def test_rule_service_client_service_account_always_use_jwt(
    transport_class, transport_name
):
    with mock.patch.object(
        service_account.Credentials, "with_always_use_jwt_access", create=True
    ) as use_jwt:
        creds = service_account.Credentials(None, None, None)
        transport = transport_class(credentials=creds, always_use_jwt_access=True)
        use_jwt.assert_called_once_with(True)

    with mock.patch.object(
        service_account.Credentials, "with_always_use_jwt_access", create=True
    ) as use_jwt:
        creds = service_account.Credentials(None, None, None)
        transport = transport_class(credentials=creds, always_use_jwt_access=False)
        use_jwt.assert_not_called()


@pytest.mark.parametrize(
    "client_class,transport_name",
    [
        (RuleServiceClient, "grpc"),
        (RuleServiceAsyncClient, "grpc_asyncio"),
        (RuleServiceClient, "rest"),
    ],
)
def test_rule_service_client_from_service_account_file(client_class, transport_name):
    creds = ga_credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_file"
    ) as factory:
        factory.return_value = creds
        client = client_class.from_service_account_file(
            "dummy/file/path.json", transport=transport_name
        )
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        client = client_class.from_service_account_json(
            "dummy/file/path.json", transport=transport_name
        )
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        assert client.transport._host == (
            "chronicle.googleapis.com:443"
            if transport_name in ["grpc", "grpc_asyncio"]
            else "https://chronicle.googleapis.com"
        )


def test_rule_service_client_get_transport_class():
    transport = RuleServiceClient.get_transport_class()
    available_transports = [
        transports.RuleServiceGrpcTransport,
        transports.RuleServiceRestTransport,
    ]
    assert transport in available_transports

    transport = RuleServiceClient.get_transport_class("grpc")
    assert transport == transports.RuleServiceGrpcTransport


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (RuleServiceClient, transports.RuleServiceGrpcTransport, "grpc"),
        (
            RuleServiceAsyncClient,
            transports.RuleServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
        (RuleServiceClient, transports.RuleServiceRestTransport, "rest"),
    ],
)
@mock.patch.object(
    RuleServiceClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(RuleServiceClient),
)
@mock.patch.object(
    RuleServiceAsyncClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(RuleServiceAsyncClient),
)
def test_rule_service_client_client_options(
    client_class, transport_class, transport_name
):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(RuleServiceClient, "get_transport_class") as gtc:
        transport = transport_class(credentials=ga_credentials.AnonymousCredentials())
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(RuleServiceClient, "get_transport_class") as gtc:
        client = client_class(transport=transport_name)
        gtc.assert_called()

    # Check the case api_endpoint is provided.
    options = client_options.ClientOptions(api_endpoint="squid.clam.whelk")
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(transport=transport_name, client_options=options)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host="squid.clam.whelk",
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT is
    # "never".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}):
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class(transport=transport_name)
            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=client._DEFAULT_ENDPOINT_TEMPLATE.format(
                    UNIVERSE_DOMAIN=client._DEFAULT_UNIVERSE
                ),
                scopes=None,
                client_cert_source_for_mtls=None,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
                always_use_jwt_access=True,
                api_audience=None,
            )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT is
    # "always".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "always"}):
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class(transport=transport_name)
            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=client.DEFAULT_MTLS_ENDPOINT,
                scopes=None,
                client_cert_source_for_mtls=None,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
                always_use_jwt_access=True,
                api_audience=None,
            )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT has
    # unsupported value.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "Unsupported"}):
        with pytest.raises(MutualTLSChannelError) as excinfo:
            client = client_class(transport=transport_name)
    assert (
        str(excinfo.value)
        == "Environment variable `GOOGLE_API_USE_MTLS_ENDPOINT` must be `never`, `auto` or `always`"
    )

    # Check the case GOOGLE_API_USE_CLIENT_CERTIFICATE has unsupported value.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "Unsupported"}
    ):
        with pytest.raises(ValueError) as excinfo:
            client = client_class(transport=transport_name)
    assert (
        str(excinfo.value)
        == "Environment variable `GOOGLE_API_USE_CLIENT_CERTIFICATE` must be either `true` or `false`"
    )

    # Check the case quota_project_id is provided
    options = client_options.ClientOptions(quota_project_id="octopus")
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client._DEFAULT_ENDPOINT_TEMPLATE.format(
                UNIVERSE_DOMAIN=client._DEFAULT_UNIVERSE
            ),
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id="octopus",
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )
    # Check the case api_endpoint is provided
    options = client_options.ClientOptions(
        api_audience="https://language.googleapis.com"
    )
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client._DEFAULT_ENDPOINT_TEMPLATE.format(
                UNIVERSE_DOMAIN=client._DEFAULT_UNIVERSE
            ),
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience="https://language.googleapis.com",
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name,use_client_cert_env",
    [
        (RuleServiceClient, transports.RuleServiceGrpcTransport, "grpc", "true"),
        (
            RuleServiceAsyncClient,
            transports.RuleServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
            "true",
        ),
        (RuleServiceClient, transports.RuleServiceGrpcTransport, "grpc", "false"),
        (
            RuleServiceAsyncClient,
            transports.RuleServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
            "false",
        ),
        (RuleServiceClient, transports.RuleServiceRestTransport, "rest", "true"),
        (RuleServiceClient, transports.RuleServiceRestTransport, "rest", "false"),
    ],
)
@mock.patch.object(
    RuleServiceClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(RuleServiceClient),
)
@mock.patch.object(
    RuleServiceAsyncClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(RuleServiceAsyncClient),
)
@mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"})
def test_rule_service_client_mtls_env_auto(
    client_class, transport_class, transport_name, use_client_cert_env
):
    # This tests the endpoint autoswitch behavior. Endpoint is autoswitched to the default
    # mtls endpoint, if GOOGLE_API_USE_CLIENT_CERTIFICATE is "true" and client cert exists.

    # Check the case client_cert_source is provided. Whether client cert is used depends on
    # GOOGLE_API_USE_CLIENT_CERTIFICATE value.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}
    ):
        options = client_options.ClientOptions(
            client_cert_source=client_cert_source_callback
        )
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class(client_options=options, transport=transport_name)

            if use_client_cert_env == "false":
                expected_client_cert_source = None
                expected_host = client._DEFAULT_ENDPOINT_TEMPLATE.format(
                    UNIVERSE_DOMAIN=client._DEFAULT_UNIVERSE
                )
            else:
                expected_client_cert_source = client_cert_source_callback
                expected_host = client.DEFAULT_MTLS_ENDPOINT

            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=expected_host,
                scopes=None,
                client_cert_source_for_mtls=expected_client_cert_source,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
                always_use_jwt_access=True,
                api_audience=None,
            )

    # Check the case ADC client cert is provided. Whether client cert is used depends on
    # GOOGLE_API_USE_CLIENT_CERTIFICATE value.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}
    ):
        with mock.patch.object(transport_class, "__init__") as patched:
            with mock.patch(
                "google.auth.transport.mtls.has_default_client_cert_source",
                return_value=True,
            ):
                with mock.patch(
                    "google.auth.transport.mtls.default_client_cert_source",
                    return_value=client_cert_source_callback,
                ):
                    if use_client_cert_env == "false":
                        expected_host = client._DEFAULT_ENDPOINT_TEMPLATE.format(
                            UNIVERSE_DOMAIN=client._DEFAULT_UNIVERSE
                        )
                        expected_client_cert_source = None
                    else:
                        expected_host = client.DEFAULT_MTLS_ENDPOINT
                        expected_client_cert_source = client_cert_source_callback

                    patched.return_value = None
                    client = client_class(transport=transport_name)
                    patched.assert_called_once_with(
                        credentials=None,
                        credentials_file=None,
                        host=expected_host,
                        scopes=None,
                        client_cert_source_for_mtls=expected_client_cert_source,
                        quota_project_id=None,
                        client_info=transports.base.DEFAULT_CLIENT_INFO,
                        always_use_jwt_access=True,
                        api_audience=None,
                    )

    # Check the case client_cert_source and ADC client cert are not provided.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}
    ):
        with mock.patch.object(transport_class, "__init__") as patched:
            with mock.patch(
                "google.auth.transport.mtls.has_default_client_cert_source",
                return_value=False,
            ):
                patched.return_value = None
                client = client_class(transport=transport_name)
                patched.assert_called_once_with(
                    credentials=None,
                    credentials_file=None,
                    host=client._DEFAULT_ENDPOINT_TEMPLATE.format(
                        UNIVERSE_DOMAIN=client._DEFAULT_UNIVERSE
                    ),
                    scopes=None,
                    client_cert_source_for_mtls=None,
                    quota_project_id=None,
                    client_info=transports.base.DEFAULT_CLIENT_INFO,
                    always_use_jwt_access=True,
                    api_audience=None,
                )


@pytest.mark.parametrize("client_class", [RuleServiceClient, RuleServiceAsyncClient])
@mock.patch.object(
    RuleServiceClient, "DEFAULT_ENDPOINT", modify_default_endpoint(RuleServiceClient)
)
@mock.patch.object(
    RuleServiceAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(RuleServiceAsyncClient),
)
def test_rule_service_client_get_mtls_endpoint_and_cert_source(client_class):
    mock_client_cert_source = mock.Mock()

    # Test the case GOOGLE_API_USE_CLIENT_CERTIFICATE is "true".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        mock_api_endpoint = "foo"
        options = client_options.ClientOptions(
            client_cert_source=mock_client_cert_source, api_endpoint=mock_api_endpoint
        )
        api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source(
            options
        )
        assert api_endpoint == mock_api_endpoint
        assert cert_source == mock_client_cert_source

    # Test the case GOOGLE_API_USE_CLIENT_CERTIFICATE is "false".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "false"}):
        mock_client_cert_source = mock.Mock()
        mock_api_endpoint = "foo"
        options = client_options.ClientOptions(
            client_cert_source=mock_client_cert_source, api_endpoint=mock_api_endpoint
        )
        api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source(
            options
        )
        assert api_endpoint == mock_api_endpoint
        assert cert_source is None

    # Test the case GOOGLE_API_USE_MTLS_ENDPOINT is "never".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}):
        api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source()
        assert api_endpoint == client_class.DEFAULT_ENDPOINT
        assert cert_source is None

    # Test the case GOOGLE_API_USE_MTLS_ENDPOINT is "always".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "always"}):
        api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source()
        assert api_endpoint == client_class.DEFAULT_MTLS_ENDPOINT
        assert cert_source is None

    # Test the case GOOGLE_API_USE_MTLS_ENDPOINT is "auto" and default cert doesn't exist.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        with mock.patch(
            "google.auth.transport.mtls.has_default_client_cert_source",
            return_value=False,
        ):
            api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source()
            assert api_endpoint == client_class.DEFAULT_ENDPOINT
            assert cert_source is None

    # Test the case GOOGLE_API_USE_MTLS_ENDPOINT is "auto" and default cert exists.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        with mock.patch(
            "google.auth.transport.mtls.has_default_client_cert_source",
            return_value=True,
        ):
            with mock.patch(
                "google.auth.transport.mtls.default_client_cert_source",
                return_value=mock_client_cert_source,
            ):
                (
                    api_endpoint,
                    cert_source,
                ) = client_class.get_mtls_endpoint_and_cert_source()
                assert api_endpoint == client_class.DEFAULT_MTLS_ENDPOINT
                assert cert_source == mock_client_cert_source

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT has
    # unsupported value.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "Unsupported"}):
        with pytest.raises(MutualTLSChannelError) as excinfo:
            client_class.get_mtls_endpoint_and_cert_source()

        assert (
            str(excinfo.value)
            == "Environment variable `GOOGLE_API_USE_MTLS_ENDPOINT` must be `never`, `auto` or `always`"
        )

    # Check the case GOOGLE_API_USE_CLIENT_CERTIFICATE has unsupported value.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "Unsupported"}
    ):
        with pytest.raises(ValueError) as excinfo:
            client_class.get_mtls_endpoint_and_cert_source()

        assert (
            str(excinfo.value)
            == "Environment variable `GOOGLE_API_USE_CLIENT_CERTIFICATE` must be either `true` or `false`"
        )


@pytest.mark.parametrize("client_class", [RuleServiceClient, RuleServiceAsyncClient])
@mock.patch.object(
    RuleServiceClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(RuleServiceClient),
)
@mock.patch.object(
    RuleServiceAsyncClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(RuleServiceAsyncClient),
)
def test_rule_service_client_client_api_endpoint(client_class):
    mock_client_cert_source = client_cert_source_callback
    api_override = "foo.com"
    default_universe = RuleServiceClient._DEFAULT_UNIVERSE
    default_endpoint = RuleServiceClient._DEFAULT_ENDPOINT_TEMPLATE.format(
        UNIVERSE_DOMAIN=default_universe
    )
    mock_universe = "bar.com"
    mock_endpoint = RuleServiceClient._DEFAULT_ENDPOINT_TEMPLATE.format(
        UNIVERSE_DOMAIN=mock_universe
    )

    # If ClientOptions.api_endpoint is set and GOOGLE_API_USE_CLIENT_CERTIFICATE="true",
    # use ClientOptions.api_endpoint as the api endpoint regardless.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        with mock.patch(
            "google.auth.transport.requests.AuthorizedSession.configure_mtls_channel"
        ):
            options = client_options.ClientOptions(
                client_cert_source=mock_client_cert_source, api_endpoint=api_override
            )
            client = client_class(
                client_options=options,
                credentials=ga_credentials.AnonymousCredentials(),
            )
            assert client.api_endpoint == api_override

    # If ClientOptions.api_endpoint is not set and GOOGLE_API_USE_MTLS_ENDPOINT="never",
    # use the _DEFAULT_ENDPOINT_TEMPLATE populated with GDU as the api endpoint.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}):
        client = client_class(credentials=ga_credentials.AnonymousCredentials())
        assert client.api_endpoint == default_endpoint

    # If ClientOptions.api_endpoint is not set and GOOGLE_API_USE_MTLS_ENDPOINT="always",
    # use the DEFAULT_MTLS_ENDPOINT as the api endpoint.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "always"}):
        client = client_class(credentials=ga_credentials.AnonymousCredentials())
        assert client.api_endpoint == client_class.DEFAULT_MTLS_ENDPOINT

    # If ClientOptions.api_endpoint is not set, GOOGLE_API_USE_MTLS_ENDPOINT="auto" (default),
    # GOOGLE_API_USE_CLIENT_CERTIFICATE="false" (default), default cert source doesn't exist,
    # and ClientOptions.universe_domain="bar.com",
    # use the _DEFAULT_ENDPOINT_TEMPLATE populated with universe domain as the api endpoint.
    options = client_options.ClientOptions()
    universe_exists = hasattr(options, "universe_domain")
    if universe_exists:
        options = client_options.ClientOptions(universe_domain=mock_universe)
        client = client_class(
            client_options=options, credentials=ga_credentials.AnonymousCredentials()
        )
    else:
        client = client_class(
            client_options=options, credentials=ga_credentials.AnonymousCredentials()
        )
    assert client.api_endpoint == (
        mock_endpoint if universe_exists else default_endpoint
    )
    assert client.universe_domain == (
        mock_universe if universe_exists else default_universe
    )

    # If ClientOptions does not have a universe domain attribute and GOOGLE_API_USE_MTLS_ENDPOINT="never",
    # use the _DEFAULT_ENDPOINT_TEMPLATE populated with GDU as the api endpoint.
    options = client_options.ClientOptions()
    if hasattr(options, "universe_domain"):
        delattr(options, "universe_domain")
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}):
        client = client_class(
            client_options=options, credentials=ga_credentials.AnonymousCredentials()
        )
        assert client.api_endpoint == default_endpoint


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (RuleServiceClient, transports.RuleServiceGrpcTransport, "grpc"),
        (
            RuleServiceAsyncClient,
            transports.RuleServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
        (RuleServiceClient, transports.RuleServiceRestTransport, "rest"),
    ],
)
def test_rule_service_client_client_options_scopes(
    client_class, transport_class, transport_name
):
    # Check the case scopes are provided.
    options = client_options.ClientOptions(
        scopes=["1", "2"],
    )
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client._DEFAULT_ENDPOINT_TEMPLATE.format(
                UNIVERSE_DOMAIN=client._DEFAULT_UNIVERSE
            ),
            scopes=["1", "2"],
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name,grpc_helpers",
    [
        (RuleServiceClient, transports.RuleServiceGrpcTransport, "grpc", grpc_helpers),
        (
            RuleServiceAsyncClient,
            transports.RuleServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
            grpc_helpers_async,
        ),
        (RuleServiceClient, transports.RuleServiceRestTransport, "rest", None),
    ],
)
def test_rule_service_client_client_options_credentials_file(
    client_class, transport_class, transport_name, grpc_helpers
):
    # Check the case credentials file is provided.
    options = client_options.ClientOptions(credentials_file="credentials.json")

    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file="credentials.json",
            host=client._DEFAULT_ENDPOINT_TEMPLATE.format(
                UNIVERSE_DOMAIN=client._DEFAULT_UNIVERSE
            ),
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )


def test_rule_service_client_client_options_from_dict():
    with mock.patch(
        "google.cloud.chronicle_v1.services.rule_service.transports.RuleServiceGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = RuleServiceClient(client_options={"api_endpoint": "squid.clam.whelk"})
        grpc_transport.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host="squid.clam.whelk",
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name,grpc_helpers",
    [
        (RuleServiceClient, transports.RuleServiceGrpcTransport, "grpc", grpc_helpers),
        (
            RuleServiceAsyncClient,
            transports.RuleServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
            grpc_helpers_async,
        ),
    ],
)
def test_rule_service_client_create_channel_credentials_file(
    client_class, transport_class, transport_name, grpc_helpers
):
    # Check the case credentials file is provided.
    options = client_options.ClientOptions(credentials_file="credentials.json")

    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file="credentials.json",
            host=client._DEFAULT_ENDPOINT_TEMPLATE.format(
                UNIVERSE_DOMAIN=client._DEFAULT_UNIVERSE
            ),
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )

    # test that the credentials from file are saved and used as the credentials.
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch.object(
        google.auth, "default", autospec=True
    ) as adc, mock.patch.object(
        grpc_helpers, "create_channel"
    ) as create_channel:
        creds = ga_credentials.AnonymousCredentials()
        file_creds = ga_credentials.AnonymousCredentials()
        load_creds.return_value = (file_creds, None)
        adc.return_value = (creds, None)
        client = client_class(client_options=options, transport=transport_name)
        create_channel.assert_called_with(
            "chronicle.googleapis.com:443",
            credentials=file_creds,
            credentials_file=None,
            quota_project_id=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            scopes=None,
            default_host="chronicle.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "request_type",
    [
        gcc_rule.CreateRuleRequest,
        dict,
    ],
)
def test_create_rule(request_type, transport: str = "grpc"):
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_rule), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcc_rule.Rule(
            name="name_value",
            revision_id="revision_id_value",
            display_name="display_name_value",
            text="text_value",
            author="author_value",
            compilation_state=gcc_rule.Rule.CompilationState.SUCCEEDED,
            type_=gcc_rule.RuleType.SINGLE_EVENT,
            reference_lists=["reference_lists_value"],
            allowed_run_frequencies=[gcc_rule.RunFrequency.LIVE],
            etag="etag_value",
            scope="scope_value",
            near_real_time_live_rule_eligible=True,
        )
        response = client.create_rule(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = gcc_rule.CreateRuleRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, gcc_rule.Rule)
    assert response.name == "name_value"
    assert response.revision_id == "revision_id_value"
    assert response.display_name == "display_name_value"
    assert response.text == "text_value"
    assert response.author == "author_value"
    assert response.compilation_state == gcc_rule.Rule.CompilationState.SUCCEEDED
    assert response.type_ == gcc_rule.RuleType.SINGLE_EVENT
    assert response.reference_lists == ["reference_lists_value"]
    assert response.allowed_run_frequencies == [gcc_rule.RunFrequency.LIVE]
    assert response.etag == "etag_value"
    assert response.scope == "scope_value"
    assert response.near_real_time_live_rule_eligible is True


def test_create_rule_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = gcc_rule.CreateRuleRequest(
        parent="parent_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_rule), "__call__") as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.create_rule(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == gcc_rule.CreateRuleRequest(
            parent="parent_value",
        )


def test_create_rule_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = RuleServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.create_rule in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.create_rule] = mock_rpc
        request = {}
        client.create_rule(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.create_rule(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_create_rule_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = RuleServiceAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.create_rule
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.create_rule
        ] = mock_rpc

        request = {}
        await client.create_rule(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.create_rule(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_create_rule_async(
    transport: str = "grpc_asyncio", request_type=gcc_rule.CreateRuleRequest
):
    client = RuleServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_rule), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gcc_rule.Rule(
                name="name_value",
                revision_id="revision_id_value",
                display_name="display_name_value",
                text="text_value",
                author="author_value",
                compilation_state=gcc_rule.Rule.CompilationState.SUCCEEDED,
                type_=gcc_rule.RuleType.SINGLE_EVENT,
                reference_lists=["reference_lists_value"],
                allowed_run_frequencies=[gcc_rule.RunFrequency.LIVE],
                etag="etag_value",
                scope="scope_value",
                near_real_time_live_rule_eligible=True,
            )
        )
        response = await client.create_rule(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = gcc_rule.CreateRuleRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, gcc_rule.Rule)
    assert response.name == "name_value"
    assert response.revision_id == "revision_id_value"
    assert response.display_name == "display_name_value"
    assert response.text == "text_value"
    assert response.author == "author_value"
    assert response.compilation_state == gcc_rule.Rule.CompilationState.SUCCEEDED
    assert response.type_ == gcc_rule.RuleType.SINGLE_EVENT
    assert response.reference_lists == ["reference_lists_value"]
    assert response.allowed_run_frequencies == [gcc_rule.RunFrequency.LIVE]
    assert response.etag == "etag_value"
    assert response.scope == "scope_value"
    assert response.near_real_time_live_rule_eligible is True


@pytest.mark.asyncio
async def test_create_rule_async_from_dict():
    await test_create_rule_async(request_type=dict)


def test_create_rule_field_headers():
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gcc_rule.CreateRuleRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_rule), "__call__") as call:
        call.return_value = gcc_rule.Rule()
        client.create_rule(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_rule_field_headers_async():
    client = RuleServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gcc_rule.CreateRuleRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_rule), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(gcc_rule.Rule())
        await client.create_rule(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


def test_create_rule_flattened():
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_rule), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcc_rule.Rule()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_rule(
            parent="parent_value",
            rule=gcc_rule.Rule(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].rule
        mock_val = gcc_rule.Rule(name="name_value")
        assert arg == mock_val


def test_create_rule_flattened_error():
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_rule(
            gcc_rule.CreateRuleRequest(),
            parent="parent_value",
            rule=gcc_rule.Rule(name="name_value"),
        )


@pytest.mark.asyncio
async def test_create_rule_flattened_async():
    client = RuleServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_rule), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcc_rule.Rule()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(gcc_rule.Rule())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_rule(
            parent="parent_value",
            rule=gcc_rule.Rule(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].rule
        mock_val = gcc_rule.Rule(name="name_value")
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_rule_flattened_error_async():
    client = RuleServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_rule(
            gcc_rule.CreateRuleRequest(),
            parent="parent_value",
            rule=gcc_rule.Rule(name="name_value"),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        rule.GetRuleRequest,
        dict,
    ],
)
def test_get_rule(request_type, transport: str = "grpc"):
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_rule), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = rule.Rule(
            name="name_value",
            revision_id="revision_id_value",
            display_name="display_name_value",
            text="text_value",
            author="author_value",
            compilation_state=rule.Rule.CompilationState.SUCCEEDED,
            type_=rule.RuleType.SINGLE_EVENT,
            reference_lists=["reference_lists_value"],
            allowed_run_frequencies=[rule.RunFrequency.LIVE],
            etag="etag_value",
            scope="scope_value",
            near_real_time_live_rule_eligible=True,
        )
        response = client.get_rule(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = rule.GetRuleRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, rule.Rule)
    assert response.name == "name_value"
    assert response.revision_id == "revision_id_value"
    assert response.display_name == "display_name_value"
    assert response.text == "text_value"
    assert response.author == "author_value"
    assert response.compilation_state == rule.Rule.CompilationState.SUCCEEDED
    assert response.type_ == rule.RuleType.SINGLE_EVENT
    assert response.reference_lists == ["reference_lists_value"]
    assert response.allowed_run_frequencies == [rule.RunFrequency.LIVE]
    assert response.etag == "etag_value"
    assert response.scope == "scope_value"
    assert response.near_real_time_live_rule_eligible is True


def test_get_rule_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = rule.GetRuleRequest(
        name="name_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_rule), "__call__") as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.get_rule(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == rule.GetRuleRequest(
            name="name_value",
        )


def test_get_rule_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = RuleServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.get_rule in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.get_rule] = mock_rpc
        request = {}
        client.get_rule(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.get_rule(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_get_rule_async_use_cached_wrapped_rpc(transport: str = "grpc_asyncio"):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = RuleServiceAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.get_rule
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.get_rule
        ] = mock_rpc

        request = {}
        await client.get_rule(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.get_rule(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_get_rule_async(
    transport: str = "grpc_asyncio", request_type=rule.GetRuleRequest
):
    client = RuleServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_rule), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            rule.Rule(
                name="name_value",
                revision_id="revision_id_value",
                display_name="display_name_value",
                text="text_value",
                author="author_value",
                compilation_state=rule.Rule.CompilationState.SUCCEEDED,
                type_=rule.RuleType.SINGLE_EVENT,
                reference_lists=["reference_lists_value"],
                allowed_run_frequencies=[rule.RunFrequency.LIVE],
                etag="etag_value",
                scope="scope_value",
                near_real_time_live_rule_eligible=True,
            )
        )
        response = await client.get_rule(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = rule.GetRuleRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, rule.Rule)
    assert response.name == "name_value"
    assert response.revision_id == "revision_id_value"
    assert response.display_name == "display_name_value"
    assert response.text == "text_value"
    assert response.author == "author_value"
    assert response.compilation_state == rule.Rule.CompilationState.SUCCEEDED
    assert response.type_ == rule.RuleType.SINGLE_EVENT
    assert response.reference_lists == ["reference_lists_value"]
    assert response.allowed_run_frequencies == [rule.RunFrequency.LIVE]
    assert response.etag == "etag_value"
    assert response.scope == "scope_value"
    assert response.near_real_time_live_rule_eligible is True


@pytest.mark.asyncio
async def test_get_rule_async_from_dict():
    await test_get_rule_async(request_type=dict)


def test_get_rule_field_headers():
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = rule.GetRuleRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_rule), "__call__") as call:
        call.return_value = rule.Rule()
        client.get_rule(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_rule_field_headers_async():
    client = RuleServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = rule.GetRuleRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_rule), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(rule.Rule())
        await client.get_rule(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


def test_get_rule_flattened():
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_rule), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = rule.Rule()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_rule(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_rule_flattened_error():
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_rule(
            rule.GetRuleRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_rule_flattened_async():
    client = RuleServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_rule), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = rule.Rule()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(rule.Rule())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_rule(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_get_rule_flattened_error_async():
    client = RuleServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_rule(
            rule.GetRuleRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        rule.ListRulesRequest,
        dict,
    ],
)
def test_list_rules(request_type, transport: str = "grpc"):
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_rules), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = rule.ListRulesResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_rules(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = rule.ListRulesRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListRulesPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_rules_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = rule.ListRulesRequest(
        parent="parent_value",
        page_token="page_token_value",
        filter="filter_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_rules), "__call__") as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.list_rules(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == rule.ListRulesRequest(
            parent="parent_value",
            page_token="page_token_value",
            filter="filter_value",
        )


def test_list_rules_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = RuleServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.list_rules in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.list_rules] = mock_rpc
        request = {}
        client.list_rules(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.list_rules(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_list_rules_async_use_cached_wrapped_rpc(transport: str = "grpc_asyncio"):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = RuleServiceAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.list_rules
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.list_rules
        ] = mock_rpc

        request = {}
        await client.list_rules(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.list_rules(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_list_rules_async(
    transport: str = "grpc_asyncio", request_type=rule.ListRulesRequest
):
    client = RuleServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_rules), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            rule.ListRulesResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_rules(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = rule.ListRulesRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListRulesAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_rules_async_from_dict():
    await test_list_rules_async(request_type=dict)


def test_list_rules_field_headers():
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = rule.ListRulesRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_rules), "__call__") as call:
        call.return_value = rule.ListRulesResponse()
        client.list_rules(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_rules_field_headers_async():
    client = RuleServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = rule.ListRulesRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_rules), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            rule.ListRulesResponse()
        )
        await client.list_rules(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


def test_list_rules_flattened():
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_rules), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = rule.ListRulesResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_rules(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_rules_flattened_error():
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_rules(
            rule.ListRulesRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_rules_flattened_async():
    client = RuleServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_rules), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = rule.ListRulesResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            rule.ListRulesResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_rules(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_list_rules_flattened_error_async():
    client = RuleServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_rules(
            rule.ListRulesRequest(),
            parent="parent_value",
        )


def test_list_rules_pager(transport_name: str = "grpc"):
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_rules), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            rule.ListRulesResponse(
                rules=[
                    rule.Rule(),
                    rule.Rule(),
                    rule.Rule(),
                ],
                next_page_token="abc",
            ),
            rule.ListRulesResponse(
                rules=[],
                next_page_token="def",
            ),
            rule.ListRulesResponse(
                rules=[
                    rule.Rule(),
                ],
                next_page_token="ghi",
            ),
            rule.ListRulesResponse(
                rules=[
                    rule.Rule(),
                    rule.Rule(),
                ],
            ),
            RuntimeError,
        )

        expected_metadata = ()
        retry = retries.Retry()
        timeout = 5
        expected_metadata = tuple(expected_metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_rules(request={}, retry=retry, timeout=timeout)

        assert pager._metadata == expected_metadata
        assert pager._retry == retry
        assert pager._timeout == timeout

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, rule.Rule) for i in results)


def test_list_rules_pages(transport_name: str = "grpc"):
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_rules), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            rule.ListRulesResponse(
                rules=[
                    rule.Rule(),
                    rule.Rule(),
                    rule.Rule(),
                ],
                next_page_token="abc",
            ),
            rule.ListRulesResponse(
                rules=[],
                next_page_token="def",
            ),
            rule.ListRulesResponse(
                rules=[
                    rule.Rule(),
                ],
                next_page_token="ghi",
            ),
            rule.ListRulesResponse(
                rules=[
                    rule.Rule(),
                    rule.Rule(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_rules(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_rules_async_pager():
    client = RuleServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_rules), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            rule.ListRulesResponse(
                rules=[
                    rule.Rule(),
                    rule.Rule(),
                    rule.Rule(),
                ],
                next_page_token="abc",
            ),
            rule.ListRulesResponse(
                rules=[],
                next_page_token="def",
            ),
            rule.ListRulesResponse(
                rules=[
                    rule.Rule(),
                ],
                next_page_token="ghi",
            ),
            rule.ListRulesResponse(
                rules=[
                    rule.Rule(),
                    rule.Rule(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_rules(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, rule.Rule) for i in responses)


@pytest.mark.asyncio
async def test_list_rules_async_pages():
    client = RuleServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_rules), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            rule.ListRulesResponse(
                rules=[
                    rule.Rule(),
                    rule.Rule(),
                    rule.Rule(),
                ],
                next_page_token="abc",
            ),
            rule.ListRulesResponse(
                rules=[],
                next_page_token="def",
            ),
            rule.ListRulesResponse(
                rules=[
                    rule.Rule(),
                ],
                next_page_token="ghi",
            ),
            rule.ListRulesResponse(
                rules=[
                    rule.Rule(),
                    rule.Rule(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_rules(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        gcc_rule.UpdateRuleRequest,
        dict,
    ],
)
def test_update_rule(request_type, transport: str = "grpc"):
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_rule), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcc_rule.Rule(
            name="name_value",
            revision_id="revision_id_value",
            display_name="display_name_value",
            text="text_value",
            author="author_value",
            compilation_state=gcc_rule.Rule.CompilationState.SUCCEEDED,
            type_=gcc_rule.RuleType.SINGLE_EVENT,
            reference_lists=["reference_lists_value"],
            allowed_run_frequencies=[gcc_rule.RunFrequency.LIVE],
            etag="etag_value",
            scope="scope_value",
            near_real_time_live_rule_eligible=True,
        )
        response = client.update_rule(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = gcc_rule.UpdateRuleRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, gcc_rule.Rule)
    assert response.name == "name_value"
    assert response.revision_id == "revision_id_value"
    assert response.display_name == "display_name_value"
    assert response.text == "text_value"
    assert response.author == "author_value"
    assert response.compilation_state == gcc_rule.Rule.CompilationState.SUCCEEDED
    assert response.type_ == gcc_rule.RuleType.SINGLE_EVENT
    assert response.reference_lists == ["reference_lists_value"]
    assert response.allowed_run_frequencies == [gcc_rule.RunFrequency.LIVE]
    assert response.etag == "etag_value"
    assert response.scope == "scope_value"
    assert response.near_real_time_live_rule_eligible is True


def test_update_rule_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = gcc_rule.UpdateRuleRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_rule), "__call__") as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.update_rule(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == gcc_rule.UpdateRuleRequest()


def test_update_rule_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = RuleServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.update_rule in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.update_rule] = mock_rpc
        request = {}
        client.update_rule(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.update_rule(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_update_rule_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = RuleServiceAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.update_rule
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.update_rule
        ] = mock_rpc

        request = {}
        await client.update_rule(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.update_rule(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_update_rule_async(
    transport: str = "grpc_asyncio", request_type=gcc_rule.UpdateRuleRequest
):
    client = RuleServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_rule), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gcc_rule.Rule(
                name="name_value",
                revision_id="revision_id_value",
                display_name="display_name_value",
                text="text_value",
                author="author_value",
                compilation_state=gcc_rule.Rule.CompilationState.SUCCEEDED,
                type_=gcc_rule.RuleType.SINGLE_EVENT,
                reference_lists=["reference_lists_value"],
                allowed_run_frequencies=[gcc_rule.RunFrequency.LIVE],
                etag="etag_value",
                scope="scope_value",
                near_real_time_live_rule_eligible=True,
            )
        )
        response = await client.update_rule(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = gcc_rule.UpdateRuleRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, gcc_rule.Rule)
    assert response.name == "name_value"
    assert response.revision_id == "revision_id_value"
    assert response.display_name == "display_name_value"
    assert response.text == "text_value"
    assert response.author == "author_value"
    assert response.compilation_state == gcc_rule.Rule.CompilationState.SUCCEEDED
    assert response.type_ == gcc_rule.RuleType.SINGLE_EVENT
    assert response.reference_lists == ["reference_lists_value"]
    assert response.allowed_run_frequencies == [gcc_rule.RunFrequency.LIVE]
    assert response.etag == "etag_value"
    assert response.scope == "scope_value"
    assert response.near_real_time_live_rule_eligible is True


@pytest.mark.asyncio
async def test_update_rule_async_from_dict():
    await test_update_rule_async(request_type=dict)


def test_update_rule_field_headers():
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gcc_rule.UpdateRuleRequest()

    request.rule.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_rule), "__call__") as call:
        call.return_value = gcc_rule.Rule()
        client.update_rule(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "rule.name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_rule_field_headers_async():
    client = RuleServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gcc_rule.UpdateRuleRequest()

    request.rule.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_rule), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(gcc_rule.Rule())
        await client.update_rule(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "rule.name=name_value",
    ) in kw["metadata"]


def test_update_rule_flattened():
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_rule), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcc_rule.Rule()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_rule(
            rule=gcc_rule.Rule(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].rule
        mock_val = gcc_rule.Rule(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


def test_update_rule_flattened_error():
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_rule(
            gcc_rule.UpdateRuleRequest(),
            rule=gcc_rule.Rule(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_rule_flattened_async():
    client = RuleServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_rule), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcc_rule.Rule()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(gcc_rule.Rule())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_rule(
            rule=gcc_rule.Rule(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].rule
        mock_val = gcc_rule.Rule(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_rule_flattened_error_async():
    client = RuleServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_rule(
            gcc_rule.UpdateRuleRequest(),
            rule=gcc_rule.Rule(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        rule.DeleteRuleRequest,
        dict,
    ],
)
def test_delete_rule(request_type, transport: str = "grpc"):
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_rule), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.delete_rule(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = rule.DeleteRuleRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_rule_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = rule.DeleteRuleRequest(
        name="name_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_rule), "__call__") as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.delete_rule(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == rule.DeleteRuleRequest(
            name="name_value",
        )


def test_delete_rule_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = RuleServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.delete_rule in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.delete_rule] = mock_rpc
        request = {}
        client.delete_rule(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.delete_rule(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_delete_rule_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = RuleServiceAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.delete_rule
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.delete_rule
        ] = mock_rpc

        request = {}
        await client.delete_rule(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.delete_rule(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_delete_rule_async(
    transport: str = "grpc_asyncio", request_type=rule.DeleteRuleRequest
):
    client = RuleServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_rule), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.delete_rule(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = rule.DeleteRuleRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_rule_async_from_dict():
    await test_delete_rule_async(request_type=dict)


def test_delete_rule_field_headers():
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = rule.DeleteRuleRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_rule), "__call__") as call:
        call.return_value = None
        client.delete_rule(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_delete_rule_field_headers_async():
    client = RuleServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = rule.DeleteRuleRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_rule), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.delete_rule(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


def test_delete_rule_flattened():
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_rule), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_rule(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_delete_rule_flattened_error():
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_rule(
            rule.DeleteRuleRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_rule_flattened_async():
    client = RuleServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_rule), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_rule(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_delete_rule_flattened_error_async():
    client = RuleServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_rule(
            rule.DeleteRuleRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        rule.ListRuleRevisionsRequest,
        dict,
    ],
)
def test_list_rule_revisions(request_type, transport: str = "grpc"):
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_rule_revisions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = rule.ListRuleRevisionsResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_rule_revisions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = rule.ListRuleRevisionsRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListRuleRevisionsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_rule_revisions_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = rule.ListRuleRevisionsRequest(
        name="name_value",
        page_token="page_token_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_rule_revisions), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.list_rule_revisions(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == rule.ListRuleRevisionsRequest(
            name="name_value",
            page_token="page_token_value",
        )


def test_list_rule_revisions_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = RuleServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.list_rule_revisions in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.list_rule_revisions
        ] = mock_rpc
        request = {}
        client.list_rule_revisions(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.list_rule_revisions(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_list_rule_revisions_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = RuleServiceAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.list_rule_revisions
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.list_rule_revisions
        ] = mock_rpc

        request = {}
        await client.list_rule_revisions(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.list_rule_revisions(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_list_rule_revisions_async(
    transport: str = "grpc_asyncio", request_type=rule.ListRuleRevisionsRequest
):
    client = RuleServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_rule_revisions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            rule.ListRuleRevisionsResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_rule_revisions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = rule.ListRuleRevisionsRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListRuleRevisionsAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_rule_revisions_async_from_dict():
    await test_list_rule_revisions_async(request_type=dict)


def test_list_rule_revisions_field_headers():
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = rule.ListRuleRevisionsRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_rule_revisions), "__call__"
    ) as call:
        call.return_value = rule.ListRuleRevisionsResponse()
        client.list_rule_revisions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_rule_revisions_field_headers_async():
    client = RuleServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = rule.ListRuleRevisionsRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_rule_revisions), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            rule.ListRuleRevisionsResponse()
        )
        await client.list_rule_revisions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


def test_list_rule_revisions_flattened():
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_rule_revisions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = rule.ListRuleRevisionsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_rule_revisions(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_list_rule_revisions_flattened_error():
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_rule_revisions(
            rule.ListRuleRevisionsRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_list_rule_revisions_flattened_async():
    client = RuleServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_rule_revisions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = rule.ListRuleRevisionsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            rule.ListRuleRevisionsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_rule_revisions(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_list_rule_revisions_flattened_error_async():
    client = RuleServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_rule_revisions(
            rule.ListRuleRevisionsRequest(),
            name="name_value",
        )


def test_list_rule_revisions_pager(transport_name: str = "grpc"):
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_rule_revisions), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            rule.ListRuleRevisionsResponse(
                rules=[
                    rule.Rule(),
                    rule.Rule(),
                    rule.Rule(),
                ],
                next_page_token="abc",
            ),
            rule.ListRuleRevisionsResponse(
                rules=[],
                next_page_token="def",
            ),
            rule.ListRuleRevisionsResponse(
                rules=[
                    rule.Rule(),
                ],
                next_page_token="ghi",
            ),
            rule.ListRuleRevisionsResponse(
                rules=[
                    rule.Rule(),
                    rule.Rule(),
                ],
            ),
            RuntimeError,
        )

        expected_metadata = ()
        retry = retries.Retry()
        timeout = 5
        expected_metadata = tuple(expected_metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", ""),)),
        )
        pager = client.list_rule_revisions(request={}, retry=retry, timeout=timeout)

        assert pager._metadata == expected_metadata
        assert pager._retry == retry
        assert pager._timeout == timeout

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, rule.Rule) for i in results)


def test_list_rule_revisions_pages(transport_name: str = "grpc"):
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_rule_revisions), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            rule.ListRuleRevisionsResponse(
                rules=[
                    rule.Rule(),
                    rule.Rule(),
                    rule.Rule(),
                ],
                next_page_token="abc",
            ),
            rule.ListRuleRevisionsResponse(
                rules=[],
                next_page_token="def",
            ),
            rule.ListRuleRevisionsResponse(
                rules=[
                    rule.Rule(),
                ],
                next_page_token="ghi",
            ),
            rule.ListRuleRevisionsResponse(
                rules=[
                    rule.Rule(),
                    rule.Rule(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_rule_revisions(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_rule_revisions_async_pager():
    client = RuleServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_rule_revisions),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            rule.ListRuleRevisionsResponse(
                rules=[
                    rule.Rule(),
                    rule.Rule(),
                    rule.Rule(),
                ],
                next_page_token="abc",
            ),
            rule.ListRuleRevisionsResponse(
                rules=[],
                next_page_token="def",
            ),
            rule.ListRuleRevisionsResponse(
                rules=[
                    rule.Rule(),
                ],
                next_page_token="ghi",
            ),
            rule.ListRuleRevisionsResponse(
                rules=[
                    rule.Rule(),
                    rule.Rule(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_rule_revisions(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, rule.Rule) for i in responses)


@pytest.mark.asyncio
async def test_list_rule_revisions_async_pages():
    client = RuleServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_rule_revisions),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            rule.ListRuleRevisionsResponse(
                rules=[
                    rule.Rule(),
                    rule.Rule(),
                    rule.Rule(),
                ],
                next_page_token="abc",
            ),
            rule.ListRuleRevisionsResponse(
                rules=[],
                next_page_token="def",
            ),
            rule.ListRuleRevisionsResponse(
                rules=[
                    rule.Rule(),
                ],
                next_page_token="ghi",
            ),
            rule.ListRuleRevisionsResponse(
                rules=[
                    rule.Rule(),
                    rule.Rule(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_rule_revisions(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        rule.CreateRetrohuntRequest,
        dict,
    ],
)
def test_create_retrohunt(request_type, transport: str = "grpc"):
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_retrohunt), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.create_retrohunt(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = rule.CreateRetrohuntRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_create_retrohunt_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = rule.CreateRetrohuntRequest(
        parent="parent_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_retrohunt), "__call__") as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.create_retrohunt(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == rule.CreateRetrohuntRequest(
            parent="parent_value",
        )


def test_create_retrohunt_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = RuleServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.create_retrohunt in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.create_retrohunt
        ] = mock_rpc
        request = {}
        client.create_retrohunt(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        # Operation methods call wrapper_fn to build a cached
        # client._transport.operations_client instance on first rpc call.
        # Subsequent calls should use the cached wrapper
        wrapper_fn.reset_mock()

        client.create_retrohunt(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_create_retrohunt_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = RuleServiceAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.create_retrohunt
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.create_retrohunt
        ] = mock_rpc

        request = {}
        await client.create_retrohunt(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        # Operation methods call wrapper_fn to build a cached
        # client._transport.operations_client instance on first rpc call.
        # Subsequent calls should use the cached wrapper
        wrapper_fn.reset_mock()

        await client.create_retrohunt(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_create_retrohunt_async(
    transport: str = "grpc_asyncio", request_type=rule.CreateRetrohuntRequest
):
    client = RuleServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_retrohunt), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.create_retrohunt(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = rule.CreateRetrohuntRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_create_retrohunt_async_from_dict():
    await test_create_retrohunt_async(request_type=dict)


def test_create_retrohunt_field_headers():
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = rule.CreateRetrohuntRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_retrohunt), "__call__") as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.create_retrohunt(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_retrohunt_field_headers_async():
    client = RuleServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = rule.CreateRetrohuntRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_retrohunt), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.create_retrohunt(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


def test_create_retrohunt_flattened():
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_retrohunt), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_retrohunt(
            parent="parent_value",
            retrohunt=rule.Retrohunt(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].retrohunt
        mock_val = rule.Retrohunt(name="name_value")
        assert arg == mock_val


def test_create_retrohunt_flattened_error():
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_retrohunt(
            rule.CreateRetrohuntRequest(),
            parent="parent_value",
            retrohunt=rule.Retrohunt(name="name_value"),
        )


@pytest.mark.asyncio
async def test_create_retrohunt_flattened_async():
    client = RuleServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_retrohunt), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_retrohunt(
            parent="parent_value",
            retrohunt=rule.Retrohunt(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].retrohunt
        mock_val = rule.Retrohunt(name="name_value")
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_retrohunt_flattened_error_async():
    client = RuleServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_retrohunt(
            rule.CreateRetrohuntRequest(),
            parent="parent_value",
            retrohunt=rule.Retrohunt(name="name_value"),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        rule.GetRetrohuntRequest,
        dict,
    ],
)
def test_get_retrohunt(request_type, transport: str = "grpc"):
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_retrohunt), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = rule.Retrohunt(
            name="name_value",
            state=rule.Retrohunt.State.RUNNING,
            progress_percentage=0.2034,
        )
        response = client.get_retrohunt(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = rule.GetRetrohuntRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, rule.Retrohunt)
    assert response.name == "name_value"
    assert response.state == rule.Retrohunt.State.RUNNING
    assert math.isclose(response.progress_percentage, 0.2034, rel_tol=1e-6)


def test_get_retrohunt_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = rule.GetRetrohuntRequest(
        name="name_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_retrohunt), "__call__") as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.get_retrohunt(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == rule.GetRetrohuntRequest(
            name="name_value",
        )


def test_get_retrohunt_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = RuleServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.get_retrohunt in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.get_retrohunt] = mock_rpc
        request = {}
        client.get_retrohunt(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.get_retrohunt(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_get_retrohunt_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = RuleServiceAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.get_retrohunt
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.get_retrohunt
        ] = mock_rpc

        request = {}
        await client.get_retrohunt(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.get_retrohunt(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_get_retrohunt_async(
    transport: str = "grpc_asyncio", request_type=rule.GetRetrohuntRequest
):
    client = RuleServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_retrohunt), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            rule.Retrohunt(
                name="name_value",
                state=rule.Retrohunt.State.RUNNING,
                progress_percentage=0.2034,
            )
        )
        response = await client.get_retrohunt(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = rule.GetRetrohuntRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, rule.Retrohunt)
    assert response.name == "name_value"
    assert response.state == rule.Retrohunt.State.RUNNING
    assert math.isclose(response.progress_percentage, 0.2034, rel_tol=1e-6)


@pytest.mark.asyncio
async def test_get_retrohunt_async_from_dict():
    await test_get_retrohunt_async(request_type=dict)


def test_get_retrohunt_field_headers():
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = rule.GetRetrohuntRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_retrohunt), "__call__") as call:
        call.return_value = rule.Retrohunt()
        client.get_retrohunt(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_retrohunt_field_headers_async():
    client = RuleServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = rule.GetRetrohuntRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_retrohunt), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(rule.Retrohunt())
        await client.get_retrohunt(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


def test_get_retrohunt_flattened():
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_retrohunt), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = rule.Retrohunt()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_retrohunt(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_retrohunt_flattened_error():
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_retrohunt(
            rule.GetRetrohuntRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_retrohunt_flattened_async():
    client = RuleServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_retrohunt), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = rule.Retrohunt()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(rule.Retrohunt())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_retrohunt(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_get_retrohunt_flattened_error_async():
    client = RuleServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_retrohunt(
            rule.GetRetrohuntRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        rule.ListRetrohuntsRequest,
        dict,
    ],
)
def test_list_retrohunts(request_type, transport: str = "grpc"):
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_retrohunts), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = rule.ListRetrohuntsResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_retrohunts(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = rule.ListRetrohuntsRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListRetrohuntsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_retrohunts_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = rule.ListRetrohuntsRequest(
        parent="parent_value",
        page_token="page_token_value",
        filter="filter_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_retrohunts), "__call__") as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.list_retrohunts(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == rule.ListRetrohuntsRequest(
            parent="parent_value",
            page_token="page_token_value",
            filter="filter_value",
        )


def test_list_retrohunts_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = RuleServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.list_retrohunts in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.list_retrohunts] = mock_rpc
        request = {}
        client.list_retrohunts(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.list_retrohunts(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_list_retrohunts_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = RuleServiceAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.list_retrohunts
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.list_retrohunts
        ] = mock_rpc

        request = {}
        await client.list_retrohunts(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.list_retrohunts(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_list_retrohunts_async(
    transport: str = "grpc_asyncio", request_type=rule.ListRetrohuntsRequest
):
    client = RuleServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_retrohunts), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            rule.ListRetrohuntsResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_retrohunts(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = rule.ListRetrohuntsRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListRetrohuntsAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_retrohunts_async_from_dict():
    await test_list_retrohunts_async(request_type=dict)


def test_list_retrohunts_field_headers():
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = rule.ListRetrohuntsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_retrohunts), "__call__") as call:
        call.return_value = rule.ListRetrohuntsResponse()
        client.list_retrohunts(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_retrohunts_field_headers_async():
    client = RuleServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = rule.ListRetrohuntsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_retrohunts), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            rule.ListRetrohuntsResponse()
        )
        await client.list_retrohunts(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


def test_list_retrohunts_flattened():
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_retrohunts), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = rule.ListRetrohuntsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_retrohunts(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_retrohunts_flattened_error():
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_retrohunts(
            rule.ListRetrohuntsRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_retrohunts_flattened_async():
    client = RuleServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_retrohunts), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = rule.ListRetrohuntsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            rule.ListRetrohuntsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_retrohunts(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_list_retrohunts_flattened_error_async():
    client = RuleServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_retrohunts(
            rule.ListRetrohuntsRequest(),
            parent="parent_value",
        )


def test_list_retrohunts_pager(transport_name: str = "grpc"):
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_retrohunts), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            rule.ListRetrohuntsResponse(
                retrohunts=[
                    rule.Retrohunt(),
                    rule.Retrohunt(),
                    rule.Retrohunt(),
                ],
                next_page_token="abc",
            ),
            rule.ListRetrohuntsResponse(
                retrohunts=[],
                next_page_token="def",
            ),
            rule.ListRetrohuntsResponse(
                retrohunts=[
                    rule.Retrohunt(),
                ],
                next_page_token="ghi",
            ),
            rule.ListRetrohuntsResponse(
                retrohunts=[
                    rule.Retrohunt(),
                    rule.Retrohunt(),
                ],
            ),
            RuntimeError,
        )

        expected_metadata = ()
        retry = retries.Retry()
        timeout = 5
        expected_metadata = tuple(expected_metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_retrohunts(request={}, retry=retry, timeout=timeout)

        assert pager._metadata == expected_metadata
        assert pager._retry == retry
        assert pager._timeout == timeout

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, rule.Retrohunt) for i in results)


def test_list_retrohunts_pages(transport_name: str = "grpc"):
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_retrohunts), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            rule.ListRetrohuntsResponse(
                retrohunts=[
                    rule.Retrohunt(),
                    rule.Retrohunt(),
                    rule.Retrohunt(),
                ],
                next_page_token="abc",
            ),
            rule.ListRetrohuntsResponse(
                retrohunts=[],
                next_page_token="def",
            ),
            rule.ListRetrohuntsResponse(
                retrohunts=[
                    rule.Retrohunt(),
                ],
                next_page_token="ghi",
            ),
            rule.ListRetrohuntsResponse(
                retrohunts=[
                    rule.Retrohunt(),
                    rule.Retrohunt(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_retrohunts(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_retrohunts_async_pager():
    client = RuleServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_retrohunts), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            rule.ListRetrohuntsResponse(
                retrohunts=[
                    rule.Retrohunt(),
                    rule.Retrohunt(),
                    rule.Retrohunt(),
                ],
                next_page_token="abc",
            ),
            rule.ListRetrohuntsResponse(
                retrohunts=[],
                next_page_token="def",
            ),
            rule.ListRetrohuntsResponse(
                retrohunts=[
                    rule.Retrohunt(),
                ],
                next_page_token="ghi",
            ),
            rule.ListRetrohuntsResponse(
                retrohunts=[
                    rule.Retrohunt(),
                    rule.Retrohunt(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_retrohunts(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, rule.Retrohunt) for i in responses)


@pytest.mark.asyncio
async def test_list_retrohunts_async_pages():
    client = RuleServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_retrohunts), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            rule.ListRetrohuntsResponse(
                retrohunts=[
                    rule.Retrohunt(),
                    rule.Retrohunt(),
                    rule.Retrohunt(),
                ],
                next_page_token="abc",
            ),
            rule.ListRetrohuntsResponse(
                retrohunts=[],
                next_page_token="def",
            ),
            rule.ListRetrohuntsResponse(
                retrohunts=[
                    rule.Retrohunt(),
                ],
                next_page_token="ghi",
            ),
            rule.ListRetrohuntsResponse(
                retrohunts=[
                    rule.Retrohunt(),
                    rule.Retrohunt(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_retrohunts(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        rule.GetRuleDeploymentRequest,
        dict,
    ],
)
def test_get_rule_deployment(request_type, transport: str = "grpc"):
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_rule_deployment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = rule.RuleDeployment(
            name="name_value",
            enabled=True,
            alerting=True,
            archived=True,
            run_frequency=rule.RunFrequency.LIVE,
            execution_state=rule.RuleDeployment.ExecutionState.DEFAULT,
            producer_rules=["producer_rules_value"],
            consumer_rules=["consumer_rules_value"],
        )
        response = client.get_rule_deployment(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = rule.GetRuleDeploymentRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, rule.RuleDeployment)
    assert response.name == "name_value"
    assert response.enabled is True
    assert response.alerting is True
    assert response.archived is True
    assert response.run_frequency == rule.RunFrequency.LIVE
    assert response.execution_state == rule.RuleDeployment.ExecutionState.DEFAULT
    assert response.producer_rules == ["producer_rules_value"]
    assert response.consumer_rules == ["consumer_rules_value"]


def test_get_rule_deployment_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = rule.GetRuleDeploymentRequest(
        name="name_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_rule_deployment), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.get_rule_deployment(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == rule.GetRuleDeploymentRequest(
            name="name_value",
        )


def test_get_rule_deployment_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = RuleServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.get_rule_deployment in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.get_rule_deployment
        ] = mock_rpc
        request = {}
        client.get_rule_deployment(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.get_rule_deployment(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_get_rule_deployment_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = RuleServiceAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.get_rule_deployment
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.get_rule_deployment
        ] = mock_rpc

        request = {}
        await client.get_rule_deployment(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.get_rule_deployment(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_get_rule_deployment_async(
    transport: str = "grpc_asyncio", request_type=rule.GetRuleDeploymentRequest
):
    client = RuleServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_rule_deployment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            rule.RuleDeployment(
                name="name_value",
                enabled=True,
                alerting=True,
                archived=True,
                run_frequency=rule.RunFrequency.LIVE,
                execution_state=rule.RuleDeployment.ExecutionState.DEFAULT,
                producer_rules=["producer_rules_value"],
                consumer_rules=["consumer_rules_value"],
            )
        )
        response = await client.get_rule_deployment(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = rule.GetRuleDeploymentRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, rule.RuleDeployment)
    assert response.name == "name_value"
    assert response.enabled is True
    assert response.alerting is True
    assert response.archived is True
    assert response.run_frequency == rule.RunFrequency.LIVE
    assert response.execution_state == rule.RuleDeployment.ExecutionState.DEFAULT
    assert response.producer_rules == ["producer_rules_value"]
    assert response.consumer_rules == ["consumer_rules_value"]


@pytest.mark.asyncio
async def test_get_rule_deployment_async_from_dict():
    await test_get_rule_deployment_async(request_type=dict)


def test_get_rule_deployment_field_headers():
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = rule.GetRuleDeploymentRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_rule_deployment), "__call__"
    ) as call:
        call.return_value = rule.RuleDeployment()
        client.get_rule_deployment(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_rule_deployment_field_headers_async():
    client = RuleServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = rule.GetRuleDeploymentRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_rule_deployment), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(rule.RuleDeployment())
        await client.get_rule_deployment(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


def test_get_rule_deployment_flattened():
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_rule_deployment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = rule.RuleDeployment()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_rule_deployment(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_rule_deployment_flattened_error():
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_rule_deployment(
            rule.GetRuleDeploymentRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_rule_deployment_flattened_async():
    client = RuleServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_rule_deployment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = rule.RuleDeployment()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(rule.RuleDeployment())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_rule_deployment(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_get_rule_deployment_flattened_error_async():
    client = RuleServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_rule_deployment(
            rule.GetRuleDeploymentRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        rule.ListRuleDeploymentsRequest,
        dict,
    ],
)
def test_list_rule_deployments(request_type, transport: str = "grpc"):
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_rule_deployments), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = rule.ListRuleDeploymentsResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_rule_deployments(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = rule.ListRuleDeploymentsRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListRuleDeploymentsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_rule_deployments_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = rule.ListRuleDeploymentsRequest(
        parent="parent_value",
        page_token="page_token_value",
        filter="filter_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_rule_deployments), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.list_rule_deployments(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == rule.ListRuleDeploymentsRequest(
            parent="parent_value",
            page_token="page_token_value",
            filter="filter_value",
        )


def test_list_rule_deployments_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = RuleServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.list_rule_deployments
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.list_rule_deployments
        ] = mock_rpc
        request = {}
        client.list_rule_deployments(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.list_rule_deployments(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_list_rule_deployments_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = RuleServiceAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.list_rule_deployments
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.list_rule_deployments
        ] = mock_rpc

        request = {}
        await client.list_rule_deployments(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.list_rule_deployments(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_list_rule_deployments_async(
    transport: str = "grpc_asyncio", request_type=rule.ListRuleDeploymentsRequest
):
    client = RuleServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_rule_deployments), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            rule.ListRuleDeploymentsResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_rule_deployments(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = rule.ListRuleDeploymentsRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListRuleDeploymentsAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_rule_deployments_async_from_dict():
    await test_list_rule_deployments_async(request_type=dict)


def test_list_rule_deployments_field_headers():
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = rule.ListRuleDeploymentsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_rule_deployments), "__call__"
    ) as call:
        call.return_value = rule.ListRuleDeploymentsResponse()
        client.list_rule_deployments(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_rule_deployments_field_headers_async():
    client = RuleServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = rule.ListRuleDeploymentsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_rule_deployments), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            rule.ListRuleDeploymentsResponse()
        )
        await client.list_rule_deployments(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


def test_list_rule_deployments_flattened():
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_rule_deployments), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = rule.ListRuleDeploymentsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_rule_deployments(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_rule_deployments_flattened_error():
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_rule_deployments(
            rule.ListRuleDeploymentsRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_rule_deployments_flattened_async():
    client = RuleServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_rule_deployments), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = rule.ListRuleDeploymentsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            rule.ListRuleDeploymentsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_rule_deployments(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_list_rule_deployments_flattened_error_async():
    client = RuleServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_rule_deployments(
            rule.ListRuleDeploymentsRequest(),
            parent="parent_value",
        )


def test_list_rule_deployments_pager(transport_name: str = "grpc"):
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_rule_deployments), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            rule.ListRuleDeploymentsResponse(
                rule_deployments=[
                    rule.RuleDeployment(),
                    rule.RuleDeployment(),
                    rule.RuleDeployment(),
                ],
                next_page_token="abc",
            ),
            rule.ListRuleDeploymentsResponse(
                rule_deployments=[],
                next_page_token="def",
            ),
            rule.ListRuleDeploymentsResponse(
                rule_deployments=[
                    rule.RuleDeployment(),
                ],
                next_page_token="ghi",
            ),
            rule.ListRuleDeploymentsResponse(
                rule_deployments=[
                    rule.RuleDeployment(),
                    rule.RuleDeployment(),
                ],
            ),
            RuntimeError,
        )

        expected_metadata = ()
        retry = retries.Retry()
        timeout = 5
        expected_metadata = tuple(expected_metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_rule_deployments(request={}, retry=retry, timeout=timeout)

        assert pager._metadata == expected_metadata
        assert pager._retry == retry
        assert pager._timeout == timeout

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, rule.RuleDeployment) for i in results)


def test_list_rule_deployments_pages(transport_name: str = "grpc"):
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_rule_deployments), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            rule.ListRuleDeploymentsResponse(
                rule_deployments=[
                    rule.RuleDeployment(),
                    rule.RuleDeployment(),
                    rule.RuleDeployment(),
                ],
                next_page_token="abc",
            ),
            rule.ListRuleDeploymentsResponse(
                rule_deployments=[],
                next_page_token="def",
            ),
            rule.ListRuleDeploymentsResponse(
                rule_deployments=[
                    rule.RuleDeployment(),
                ],
                next_page_token="ghi",
            ),
            rule.ListRuleDeploymentsResponse(
                rule_deployments=[
                    rule.RuleDeployment(),
                    rule.RuleDeployment(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_rule_deployments(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_rule_deployments_async_pager():
    client = RuleServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_rule_deployments),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            rule.ListRuleDeploymentsResponse(
                rule_deployments=[
                    rule.RuleDeployment(),
                    rule.RuleDeployment(),
                    rule.RuleDeployment(),
                ],
                next_page_token="abc",
            ),
            rule.ListRuleDeploymentsResponse(
                rule_deployments=[],
                next_page_token="def",
            ),
            rule.ListRuleDeploymentsResponse(
                rule_deployments=[
                    rule.RuleDeployment(),
                ],
                next_page_token="ghi",
            ),
            rule.ListRuleDeploymentsResponse(
                rule_deployments=[
                    rule.RuleDeployment(),
                    rule.RuleDeployment(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_rule_deployments(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, rule.RuleDeployment) for i in responses)


@pytest.mark.asyncio
async def test_list_rule_deployments_async_pages():
    client = RuleServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_rule_deployments),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            rule.ListRuleDeploymentsResponse(
                rule_deployments=[
                    rule.RuleDeployment(),
                    rule.RuleDeployment(),
                    rule.RuleDeployment(),
                ],
                next_page_token="abc",
            ),
            rule.ListRuleDeploymentsResponse(
                rule_deployments=[],
                next_page_token="def",
            ),
            rule.ListRuleDeploymentsResponse(
                rule_deployments=[
                    rule.RuleDeployment(),
                ],
                next_page_token="ghi",
            ),
            rule.ListRuleDeploymentsResponse(
                rule_deployments=[
                    rule.RuleDeployment(),
                    rule.RuleDeployment(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_rule_deployments(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        rule.UpdateRuleDeploymentRequest,
        dict,
    ],
)
def test_update_rule_deployment(request_type, transport: str = "grpc"):
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_rule_deployment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = rule.RuleDeployment(
            name="name_value",
            enabled=True,
            alerting=True,
            archived=True,
            run_frequency=rule.RunFrequency.LIVE,
            execution_state=rule.RuleDeployment.ExecutionState.DEFAULT,
            producer_rules=["producer_rules_value"],
            consumer_rules=["consumer_rules_value"],
        )
        response = client.update_rule_deployment(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = rule.UpdateRuleDeploymentRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, rule.RuleDeployment)
    assert response.name == "name_value"
    assert response.enabled is True
    assert response.alerting is True
    assert response.archived is True
    assert response.run_frequency == rule.RunFrequency.LIVE
    assert response.execution_state == rule.RuleDeployment.ExecutionState.DEFAULT
    assert response.producer_rules == ["producer_rules_value"]
    assert response.consumer_rules == ["consumer_rules_value"]


def test_update_rule_deployment_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = rule.UpdateRuleDeploymentRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_rule_deployment), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.update_rule_deployment(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == rule.UpdateRuleDeploymentRequest()


def test_update_rule_deployment_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = RuleServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.update_rule_deployment
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.update_rule_deployment
        ] = mock_rpc
        request = {}
        client.update_rule_deployment(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.update_rule_deployment(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_update_rule_deployment_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = RuleServiceAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.update_rule_deployment
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.update_rule_deployment
        ] = mock_rpc

        request = {}
        await client.update_rule_deployment(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.update_rule_deployment(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_update_rule_deployment_async(
    transport: str = "grpc_asyncio", request_type=rule.UpdateRuleDeploymentRequest
):
    client = RuleServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_rule_deployment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            rule.RuleDeployment(
                name="name_value",
                enabled=True,
                alerting=True,
                archived=True,
                run_frequency=rule.RunFrequency.LIVE,
                execution_state=rule.RuleDeployment.ExecutionState.DEFAULT,
                producer_rules=["producer_rules_value"],
                consumer_rules=["consumer_rules_value"],
            )
        )
        response = await client.update_rule_deployment(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = rule.UpdateRuleDeploymentRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, rule.RuleDeployment)
    assert response.name == "name_value"
    assert response.enabled is True
    assert response.alerting is True
    assert response.archived is True
    assert response.run_frequency == rule.RunFrequency.LIVE
    assert response.execution_state == rule.RuleDeployment.ExecutionState.DEFAULT
    assert response.producer_rules == ["producer_rules_value"]
    assert response.consumer_rules == ["consumer_rules_value"]


@pytest.mark.asyncio
async def test_update_rule_deployment_async_from_dict():
    await test_update_rule_deployment_async(request_type=dict)


def test_update_rule_deployment_field_headers():
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = rule.UpdateRuleDeploymentRequest()

    request.rule_deployment.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_rule_deployment), "__call__"
    ) as call:
        call.return_value = rule.RuleDeployment()
        client.update_rule_deployment(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "rule_deployment.name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_rule_deployment_field_headers_async():
    client = RuleServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = rule.UpdateRuleDeploymentRequest()

    request.rule_deployment.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_rule_deployment), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(rule.RuleDeployment())
        await client.update_rule_deployment(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "rule_deployment.name=name_value",
    ) in kw["metadata"]


def test_update_rule_deployment_flattened():
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_rule_deployment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = rule.RuleDeployment()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_rule_deployment(
            rule_deployment=rule.RuleDeployment(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].rule_deployment
        mock_val = rule.RuleDeployment(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


def test_update_rule_deployment_flattened_error():
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_rule_deployment(
            rule.UpdateRuleDeploymentRequest(),
            rule_deployment=rule.RuleDeployment(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_rule_deployment_flattened_async():
    client = RuleServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_rule_deployment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = rule.RuleDeployment()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(rule.RuleDeployment())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_rule_deployment(
            rule_deployment=rule.RuleDeployment(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].rule_deployment
        mock_val = rule.RuleDeployment(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_rule_deployment_flattened_error_async():
    client = RuleServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_rule_deployment(
            rule.UpdateRuleDeploymentRequest(),
            rule_deployment=rule.RuleDeployment(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


def test_create_rule_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = RuleServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.create_rule in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.create_rule] = mock_rpc

        request = {}
        client.create_rule(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.create_rule(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_create_rule_rest_required_fields(request_type=gcc_rule.CreateRuleRequest):
    transport_class = transports.RuleServiceRestTransport

    request_init = {}
    request_init["parent"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_rule._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_rule._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"

    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = gcc_rule.Rule()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "post",
                "query_params": pb_request,
            }
            transcode_result["body"] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = gcc_rule.Rule.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value
            req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

            response = client.create_rule(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_create_rule_rest_unset_required_fields():
    transport = transports.RuleServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.create_rule._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(())
        & set(
            (
                "parent",
                "rule",
            )
        )
    )


def test_create_rule_rest_flattened():
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = gcc_rule.Rule()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "parent": "projects/sample1/locations/sample2/instances/sample3"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
            rule=gcc_rule.Rule(name="name_value"),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = gcc_rule.Rule.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

        client.create_rule(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*/instances/*}/rules"
            % client.transport._host,
            args[1],
        )


def test_create_rule_rest_flattened_error(transport: str = "rest"):
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_rule(
            gcc_rule.CreateRuleRequest(),
            parent="parent_value",
            rule=gcc_rule.Rule(name="name_value"),
        )


def test_get_rule_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = RuleServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.get_rule in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.get_rule] = mock_rpc

        request = {}
        client.get_rule(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.get_rule(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_get_rule_rest_required_fields(request_type=rule.GetRuleRequest):
    transport_class = transports.RuleServiceRestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_rule._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_rule._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("view",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = rule.Rule()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "get",
                "query_params": pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = rule.Rule.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value
            req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

            response = client.get_rule(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_rule_rest_unset_required_fields():
    transport = transports.RuleServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get_rule._get_unset_required_fields({})
    assert set(unset_fields) == (set(("view",)) & set(("name",)))


def test_get_rule_rest_flattened():
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = rule.Rule()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/instances/sample3/rules/sample4"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = rule.Rule.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

        client.get_rule(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/instances/*/rules/*}"
            % client.transport._host,
            args[1],
        )


def test_get_rule_rest_flattened_error(transport: str = "rest"):
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_rule(
            rule.GetRuleRequest(),
            name="name_value",
        )


def test_list_rules_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = RuleServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.list_rules in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.list_rules] = mock_rpc

        request = {}
        client.list_rules(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.list_rules(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_list_rules_rest_required_fields(request_type=rule.ListRulesRequest):
    transport_class = transports.RuleServiceRestTransport

    request_init = {}
    request_init["parent"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_rules._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_rules._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "filter",
            "page_size",
            "page_token",
            "view",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"

    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = rule.ListRulesResponse()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "get",
                "query_params": pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = rule.ListRulesResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value
            req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

            response = client.list_rules(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_rules_rest_unset_required_fields():
    transport = transports.RuleServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_rules._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "filter",
                "pageSize",
                "pageToken",
                "view",
            )
        )
        & set(("parent",))
    )


def test_list_rules_rest_flattened():
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = rule.ListRulesResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "parent": "projects/sample1/locations/sample2/instances/sample3"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = rule.ListRulesResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

        client.list_rules(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*/instances/*}/rules"
            % client.transport._host,
            args[1],
        )


def test_list_rules_rest_flattened_error(transport: str = "rest"):
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_rules(
            rule.ListRulesRequest(),
            parent="parent_value",
        )


def test_list_rules_rest_pager(transport: str = "rest"):
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            rule.ListRulesResponse(
                rules=[
                    rule.Rule(),
                    rule.Rule(),
                    rule.Rule(),
                ],
                next_page_token="abc",
            ),
            rule.ListRulesResponse(
                rules=[],
                next_page_token="def",
            ),
            rule.ListRulesResponse(
                rules=[
                    rule.Rule(),
                ],
                next_page_token="ghi",
            ),
            rule.ListRulesResponse(
                rules=[
                    rule.Rule(),
                    rule.Rule(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(rule.ListRulesResponse.to_json(x) for x in response)
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {
            "parent": "projects/sample1/locations/sample2/instances/sample3"
        }

        pager = client.list_rules(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, rule.Rule) for i in results)

        pages = list(client.list_rules(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_update_rule_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = RuleServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.update_rule in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.update_rule] = mock_rpc

        request = {}
        client.update_rule(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.update_rule(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_update_rule_rest_required_fields(request_type=gcc_rule.UpdateRuleRequest):
    transport_class = transports.RuleServiceRestTransport

    request_init = {}
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).update_rule._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).update_rule._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("update_mask",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone

    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = gcc_rule.Rule()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "patch",
                "query_params": pb_request,
            }
            transcode_result["body"] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = gcc_rule.Rule.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value
            req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

            response = client.update_rule(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_update_rule_rest_unset_required_fields():
    transport = transports.RuleServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.update_rule._get_unset_required_fields({})
    assert set(unset_fields) == (set(("updateMask",)) & set(("rule",)))


def test_update_rule_rest_flattened():
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = gcc_rule.Rule()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "rule": {
                "name": "projects/sample1/locations/sample2/instances/sample3/rules/sample4"
            }
        }

        # get truthy value for each flattened field
        mock_args = dict(
            rule=gcc_rule.Rule(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = gcc_rule.Rule.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

        client.update_rule(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{rule.name=projects/*/locations/*/instances/*/rules/*}"
            % client.transport._host,
            args[1],
        )


def test_update_rule_rest_flattened_error(transport: str = "rest"):
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_rule(
            gcc_rule.UpdateRuleRequest(),
            rule=gcc_rule.Rule(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


def test_delete_rule_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = RuleServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.delete_rule in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.delete_rule] = mock_rpc

        request = {}
        client.delete_rule(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.delete_rule(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_delete_rule_rest_required_fields(request_type=rule.DeleteRuleRequest):
    transport_class = transports.RuleServiceRestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete_rule._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete_rule._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("force",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = None
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "delete",
                "query_params": pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = ""

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value
            req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

            response = client.delete_rule(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_delete_rule_rest_unset_required_fields():
    transport = transports.RuleServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.delete_rule._get_unset_required_fields({})
    assert set(unset_fields) == (set(("force",)) & set(("name",)))


def test_delete_rule_rest_flattened():
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = None

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/instances/sample3/rules/sample4"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = ""
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

        client.delete_rule(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/instances/*/rules/*}"
            % client.transport._host,
            args[1],
        )


def test_delete_rule_rest_flattened_error(transport: str = "rest"):
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_rule(
            rule.DeleteRuleRequest(),
            name="name_value",
        )


def test_list_rule_revisions_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = RuleServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.list_rule_revisions in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.list_rule_revisions
        ] = mock_rpc

        request = {}
        client.list_rule_revisions(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.list_rule_revisions(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_list_rule_revisions_rest_required_fields(
    request_type=rule.ListRuleRevisionsRequest,
):
    transport_class = transports.RuleServiceRestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_rule_revisions._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_rule_revisions._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "page_size",
            "page_token",
            "view",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = rule.ListRuleRevisionsResponse()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "get",
                "query_params": pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = rule.ListRuleRevisionsResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value
            req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

            response = client.list_rule_revisions(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_rule_revisions_rest_unset_required_fields():
    transport = transports.RuleServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_rule_revisions._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "pageSize",
                "pageToken",
                "view",
            )
        )
        & set(("name",))
    )


def test_list_rule_revisions_rest_flattened():
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = rule.ListRuleRevisionsResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/instances/sample3/rules/sample4"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = rule.ListRuleRevisionsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

        client.list_rule_revisions(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/instances/*/rules/*}:listRevisions"
            % client.transport._host,
            args[1],
        )


def test_list_rule_revisions_rest_flattened_error(transport: str = "rest"):
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_rule_revisions(
            rule.ListRuleRevisionsRequest(),
            name="name_value",
        )


def test_list_rule_revisions_rest_pager(transport: str = "rest"):
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            rule.ListRuleRevisionsResponse(
                rules=[
                    rule.Rule(),
                    rule.Rule(),
                    rule.Rule(),
                ],
                next_page_token="abc",
            ),
            rule.ListRuleRevisionsResponse(
                rules=[],
                next_page_token="def",
            ),
            rule.ListRuleRevisionsResponse(
                rules=[
                    rule.Rule(),
                ],
                next_page_token="ghi",
            ),
            rule.ListRuleRevisionsResponse(
                rules=[
                    rule.Rule(),
                    rule.Rule(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(rule.ListRuleRevisionsResponse.to_json(x) for x in response)
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {
            "name": "projects/sample1/locations/sample2/instances/sample3/rules/sample4"
        }

        pager = client.list_rule_revisions(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, rule.Rule) for i in results)

        pages = list(client.list_rule_revisions(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_create_retrohunt_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = RuleServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.create_retrohunt in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.create_retrohunt
        ] = mock_rpc

        request = {}
        client.create_retrohunt(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        # Operation methods build a cached wrapper on first rpc call
        # subsequent calls should use the cached wrapper
        wrapper_fn.reset_mock()

        client.create_retrohunt(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_create_retrohunt_rest_required_fields(
    request_type=rule.CreateRetrohuntRequest,
):
    transport_class = transports.RuleServiceRestTransport

    request_init = {}
    request_init["parent"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_retrohunt._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_retrohunt._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"

    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = operations_pb2.Operation(name="operations/spam")
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "post",
                "query_params": pb_request,
            }
            transcode_result["body"] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value
            req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

            response = client.create_retrohunt(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_create_retrohunt_rest_unset_required_fields():
    transport = transports.RuleServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.create_retrohunt._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(())
        & set(
            (
                "parent",
                "retrohunt",
            )
        )
    )


def test_create_retrohunt_rest_flattened():
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "parent": "projects/sample1/locations/sample2/instances/sample3/rules/sample4"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
            retrohunt=rule.Retrohunt(name="name_value"),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

        client.create_retrohunt(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*/instances/*/rules/*}/retrohunts"
            % client.transport._host,
            args[1],
        )


def test_create_retrohunt_rest_flattened_error(transport: str = "rest"):
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_retrohunt(
            rule.CreateRetrohuntRequest(),
            parent="parent_value",
            retrohunt=rule.Retrohunt(name="name_value"),
        )


def test_get_retrohunt_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = RuleServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.get_retrohunt in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.get_retrohunt] = mock_rpc

        request = {}
        client.get_retrohunt(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.get_retrohunt(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_get_retrohunt_rest_required_fields(request_type=rule.GetRetrohuntRequest):
    transport_class = transports.RuleServiceRestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_retrohunt._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_retrohunt._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = rule.Retrohunt()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "get",
                "query_params": pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = rule.Retrohunt.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value
            req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

            response = client.get_retrohunt(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_retrohunt_rest_unset_required_fields():
    transport = transports.RuleServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get_retrohunt._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


def test_get_retrohunt_rest_flattened():
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = rule.Retrohunt()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/instances/sample3/rules/sample4/retrohunts/sample5"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = rule.Retrohunt.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

        client.get_retrohunt(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/instances/*/rules/*/retrohunts/*}"
            % client.transport._host,
            args[1],
        )


def test_get_retrohunt_rest_flattened_error(transport: str = "rest"):
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_retrohunt(
            rule.GetRetrohuntRequest(),
            name="name_value",
        )


def test_list_retrohunts_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = RuleServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.list_retrohunts in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.list_retrohunts] = mock_rpc

        request = {}
        client.list_retrohunts(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.list_retrohunts(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_list_retrohunts_rest_required_fields(request_type=rule.ListRetrohuntsRequest):
    transport_class = transports.RuleServiceRestTransport

    request_init = {}
    request_init["parent"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_retrohunts._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_retrohunts._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "filter",
            "page_size",
            "page_token",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"

    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = rule.ListRetrohuntsResponse()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "get",
                "query_params": pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = rule.ListRetrohuntsResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value
            req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

            response = client.list_retrohunts(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_retrohunts_rest_unset_required_fields():
    transport = transports.RuleServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_retrohunts._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "filter",
                "pageSize",
                "pageToken",
            )
        )
        & set(("parent",))
    )


def test_list_retrohunts_rest_flattened():
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = rule.ListRetrohuntsResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "parent": "projects/sample1/locations/sample2/instances/sample3/rules/sample4"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = rule.ListRetrohuntsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

        client.list_retrohunts(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*/instances/*/rules/*}/retrohunts"
            % client.transport._host,
            args[1],
        )


def test_list_retrohunts_rest_flattened_error(transport: str = "rest"):
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_retrohunts(
            rule.ListRetrohuntsRequest(),
            parent="parent_value",
        )


def test_list_retrohunts_rest_pager(transport: str = "rest"):
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            rule.ListRetrohuntsResponse(
                retrohunts=[
                    rule.Retrohunt(),
                    rule.Retrohunt(),
                    rule.Retrohunt(),
                ],
                next_page_token="abc",
            ),
            rule.ListRetrohuntsResponse(
                retrohunts=[],
                next_page_token="def",
            ),
            rule.ListRetrohuntsResponse(
                retrohunts=[
                    rule.Retrohunt(),
                ],
                next_page_token="ghi",
            ),
            rule.ListRetrohuntsResponse(
                retrohunts=[
                    rule.Retrohunt(),
                    rule.Retrohunt(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(rule.ListRetrohuntsResponse.to_json(x) for x in response)
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {
            "parent": "projects/sample1/locations/sample2/instances/sample3/rules/sample4"
        }

        pager = client.list_retrohunts(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, rule.Retrohunt) for i in results)

        pages = list(client.list_retrohunts(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_get_rule_deployment_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = RuleServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.get_rule_deployment in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.get_rule_deployment
        ] = mock_rpc

        request = {}
        client.get_rule_deployment(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.get_rule_deployment(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_get_rule_deployment_rest_required_fields(
    request_type=rule.GetRuleDeploymentRequest,
):
    transport_class = transports.RuleServiceRestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_rule_deployment._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_rule_deployment._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = rule.RuleDeployment()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "get",
                "query_params": pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = rule.RuleDeployment.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value
            req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

            response = client.get_rule_deployment(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_rule_deployment_rest_unset_required_fields():
    transport = transports.RuleServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get_rule_deployment._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


def test_get_rule_deployment_rest_flattened():
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = rule.RuleDeployment()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/instances/sample3/rules/sample4/deployment"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = rule.RuleDeployment.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

        client.get_rule_deployment(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/instances/*/rules/*/deployment}"
            % client.transport._host,
            args[1],
        )


def test_get_rule_deployment_rest_flattened_error(transport: str = "rest"):
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_rule_deployment(
            rule.GetRuleDeploymentRequest(),
            name="name_value",
        )


def test_list_rule_deployments_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = RuleServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.list_rule_deployments
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.list_rule_deployments
        ] = mock_rpc

        request = {}
        client.list_rule_deployments(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.list_rule_deployments(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_list_rule_deployments_rest_required_fields(
    request_type=rule.ListRuleDeploymentsRequest,
):
    transport_class = transports.RuleServiceRestTransport

    request_init = {}
    request_init["parent"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_rule_deployments._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_rule_deployments._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "filter",
            "page_size",
            "page_token",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"

    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = rule.ListRuleDeploymentsResponse()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "get",
                "query_params": pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = rule.ListRuleDeploymentsResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value
            req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

            response = client.list_rule_deployments(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_rule_deployments_rest_unset_required_fields():
    transport = transports.RuleServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_rule_deployments._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "filter",
                "pageSize",
                "pageToken",
            )
        )
        & set(("parent",))
    )


def test_list_rule_deployments_rest_flattened():
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = rule.ListRuleDeploymentsResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "parent": "projects/sample1/locations/sample2/instances/sample3/rules/sample4"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = rule.ListRuleDeploymentsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

        client.list_rule_deployments(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*/instances/*/rules/*}/deployments"
            % client.transport._host,
            args[1],
        )


def test_list_rule_deployments_rest_flattened_error(transport: str = "rest"):
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_rule_deployments(
            rule.ListRuleDeploymentsRequest(),
            parent="parent_value",
        )


def test_list_rule_deployments_rest_pager(transport: str = "rest"):
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            rule.ListRuleDeploymentsResponse(
                rule_deployments=[
                    rule.RuleDeployment(),
                    rule.RuleDeployment(),
                    rule.RuleDeployment(),
                ],
                next_page_token="abc",
            ),
            rule.ListRuleDeploymentsResponse(
                rule_deployments=[],
                next_page_token="def",
            ),
            rule.ListRuleDeploymentsResponse(
                rule_deployments=[
                    rule.RuleDeployment(),
                ],
                next_page_token="ghi",
            ),
            rule.ListRuleDeploymentsResponse(
                rule_deployments=[
                    rule.RuleDeployment(),
                    rule.RuleDeployment(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(rule.ListRuleDeploymentsResponse.to_json(x) for x in response)
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {
            "parent": "projects/sample1/locations/sample2/instances/sample3/rules/sample4"
        }

        pager = client.list_rule_deployments(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, rule.RuleDeployment) for i in results)

        pages = list(client.list_rule_deployments(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_update_rule_deployment_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = RuleServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.update_rule_deployment
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.update_rule_deployment
        ] = mock_rpc

        request = {}
        client.update_rule_deployment(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.update_rule_deployment(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_update_rule_deployment_rest_required_fields(
    request_type=rule.UpdateRuleDeploymentRequest,
):
    transport_class = transports.RuleServiceRestTransport

    request_init = {}
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).update_rule_deployment._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).update_rule_deployment._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("update_mask",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone

    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = rule.RuleDeployment()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "patch",
                "query_params": pb_request,
            }
            transcode_result["body"] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = rule.RuleDeployment.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value
            req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

            response = client.update_rule_deployment(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_update_rule_deployment_rest_unset_required_fields():
    transport = transports.RuleServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.update_rule_deployment._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(("updateMask",))
        & set(
            (
                "ruleDeployment",
                "updateMask",
            )
        )
    )


def test_update_rule_deployment_rest_flattened():
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = rule.RuleDeployment()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "rule_deployment": {
                "name": "projects/sample1/locations/sample2/instances/sample3/rules/sample4/deployment"
            }
        }

        # get truthy value for each flattened field
        mock_args = dict(
            rule_deployment=rule.RuleDeployment(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = rule.RuleDeployment.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

        client.update_rule_deployment(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{rule_deployment.name=projects/*/locations/*/instances/*/rules/*/deployment}"
            % client.transport._host,
            args[1],
        )


def test_update_rule_deployment_rest_flattened_error(transport: str = "rest"):
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_rule_deployment(
            rule.UpdateRuleDeploymentRequest(),
            rule_deployment=rule.RuleDeployment(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.RuleServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = RuleServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.RuleServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = RuleServiceClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide an api_key and a transport instance.
    transport = transports.RuleServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    options = client_options.ClientOptions()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = RuleServiceClient(
            client_options=options,
            transport=transport,
        )

    # It is an error to provide an api_key and a credential.
    options = client_options.ClientOptions()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = RuleServiceClient(
            client_options=options, credentials=ga_credentials.AnonymousCredentials()
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.RuleServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = RuleServiceClient(
            client_options={"scopes": ["1", "2"]},
            transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.RuleServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    client = RuleServiceClient(transport=transport)
    assert client.transport is transport


def test_transport_get_channel():
    # A client may be instantiated with a custom transport instance.
    transport = transports.RuleServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

    transport = transports.RuleServiceGrpcAsyncIOTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.RuleServiceGrpcTransport,
        transports.RuleServiceGrpcAsyncIOTransport,
        transports.RuleServiceRestTransport,
    ],
)
def test_transport_adc(transport_class):
    # Test default credentials are used if not provided.
    with mock.patch.object(google.auth, "default") as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport_class()
        adc.assert_called_once()


def test_transport_kind_grpc():
    transport = RuleServiceClient.get_transport_class("grpc")(
        credentials=ga_credentials.AnonymousCredentials()
    )
    assert transport.kind == "grpc"


def test_initialize_client_w_grpc():
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc"
    )
    assert client is not None


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_create_rule_empty_call_grpc():
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.create_rule), "__call__") as call:
        call.return_value = gcc_rule.Rule()
        client.create_rule(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = gcc_rule.CreateRuleRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_get_rule_empty_call_grpc():
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.get_rule), "__call__") as call:
        call.return_value = rule.Rule()
        client.get_rule(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = rule.GetRuleRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_list_rules_empty_call_grpc():
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.list_rules), "__call__") as call:
        call.return_value = rule.ListRulesResponse()
        client.list_rules(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = rule.ListRulesRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_update_rule_empty_call_grpc():
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.update_rule), "__call__") as call:
        call.return_value = gcc_rule.Rule()
        client.update_rule(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = gcc_rule.UpdateRuleRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_delete_rule_empty_call_grpc():
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.delete_rule), "__call__") as call:
        call.return_value = None
        client.delete_rule(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = rule.DeleteRuleRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_list_rule_revisions_empty_call_grpc():
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.list_rule_revisions), "__call__"
    ) as call:
        call.return_value = rule.ListRuleRevisionsResponse()
        client.list_rule_revisions(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = rule.ListRuleRevisionsRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_create_retrohunt_empty_call_grpc():
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.create_retrohunt), "__call__") as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.create_retrohunt(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = rule.CreateRetrohuntRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_get_retrohunt_empty_call_grpc():
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.get_retrohunt), "__call__") as call:
        call.return_value = rule.Retrohunt()
        client.get_retrohunt(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = rule.GetRetrohuntRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_list_retrohunts_empty_call_grpc():
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.list_retrohunts), "__call__") as call:
        call.return_value = rule.ListRetrohuntsResponse()
        client.list_retrohunts(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = rule.ListRetrohuntsRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_get_rule_deployment_empty_call_grpc():
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.get_rule_deployment), "__call__"
    ) as call:
        call.return_value = rule.RuleDeployment()
        client.get_rule_deployment(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = rule.GetRuleDeploymentRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_list_rule_deployments_empty_call_grpc():
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.list_rule_deployments), "__call__"
    ) as call:
        call.return_value = rule.ListRuleDeploymentsResponse()
        client.list_rule_deployments(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = rule.ListRuleDeploymentsRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_update_rule_deployment_empty_call_grpc():
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.update_rule_deployment), "__call__"
    ) as call:
        call.return_value = rule.RuleDeployment()
        client.update_rule_deployment(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = rule.UpdateRuleDeploymentRequest()

        assert args[0] == request_msg


def test_transport_kind_grpc_asyncio():
    transport = RuleServiceAsyncClient.get_transport_class("grpc_asyncio")(
        credentials=async_anonymous_credentials()
    )
    assert transport.kind == "grpc_asyncio"


def test_initialize_client_w_grpc_asyncio():
    client = RuleServiceAsyncClient(
        credentials=async_anonymous_credentials(), transport="grpc_asyncio"
    )
    assert client is not None


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_create_rule_empty_call_grpc_asyncio():
    client = RuleServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.create_rule), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gcc_rule.Rule(
                name="name_value",
                revision_id="revision_id_value",
                display_name="display_name_value",
                text="text_value",
                author="author_value",
                compilation_state=gcc_rule.Rule.CompilationState.SUCCEEDED,
                type_=gcc_rule.RuleType.SINGLE_EVENT,
                reference_lists=["reference_lists_value"],
                allowed_run_frequencies=[gcc_rule.RunFrequency.LIVE],
                etag="etag_value",
                scope="scope_value",
                near_real_time_live_rule_eligible=True,
            )
        )
        await client.create_rule(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = gcc_rule.CreateRuleRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_get_rule_empty_call_grpc_asyncio():
    client = RuleServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.get_rule), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            rule.Rule(
                name="name_value",
                revision_id="revision_id_value",
                display_name="display_name_value",
                text="text_value",
                author="author_value",
                compilation_state=rule.Rule.CompilationState.SUCCEEDED,
                type_=rule.RuleType.SINGLE_EVENT,
                reference_lists=["reference_lists_value"],
                allowed_run_frequencies=[rule.RunFrequency.LIVE],
                etag="etag_value",
                scope="scope_value",
                near_real_time_live_rule_eligible=True,
            )
        )
        await client.get_rule(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = rule.GetRuleRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_list_rules_empty_call_grpc_asyncio():
    client = RuleServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.list_rules), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            rule.ListRulesResponse(
                next_page_token="next_page_token_value",
            )
        )
        await client.list_rules(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = rule.ListRulesRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_update_rule_empty_call_grpc_asyncio():
    client = RuleServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.update_rule), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gcc_rule.Rule(
                name="name_value",
                revision_id="revision_id_value",
                display_name="display_name_value",
                text="text_value",
                author="author_value",
                compilation_state=gcc_rule.Rule.CompilationState.SUCCEEDED,
                type_=gcc_rule.RuleType.SINGLE_EVENT,
                reference_lists=["reference_lists_value"],
                allowed_run_frequencies=[gcc_rule.RunFrequency.LIVE],
                etag="etag_value",
                scope="scope_value",
                near_real_time_live_rule_eligible=True,
            )
        )
        await client.update_rule(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = gcc_rule.UpdateRuleRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_delete_rule_empty_call_grpc_asyncio():
    client = RuleServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.delete_rule), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.delete_rule(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = rule.DeleteRuleRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_list_rule_revisions_empty_call_grpc_asyncio():
    client = RuleServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.list_rule_revisions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            rule.ListRuleRevisionsResponse(
                next_page_token="next_page_token_value",
            )
        )
        await client.list_rule_revisions(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = rule.ListRuleRevisionsRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_create_retrohunt_empty_call_grpc_asyncio():
    client = RuleServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.create_retrohunt), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        await client.create_retrohunt(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = rule.CreateRetrohuntRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_get_retrohunt_empty_call_grpc_asyncio():
    client = RuleServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.get_retrohunt), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            rule.Retrohunt(
                name="name_value",
                state=rule.Retrohunt.State.RUNNING,
                progress_percentage=0.2034,
            )
        )
        await client.get_retrohunt(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = rule.GetRetrohuntRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_list_retrohunts_empty_call_grpc_asyncio():
    client = RuleServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.list_retrohunts), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            rule.ListRetrohuntsResponse(
                next_page_token="next_page_token_value",
            )
        )
        await client.list_retrohunts(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = rule.ListRetrohuntsRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_get_rule_deployment_empty_call_grpc_asyncio():
    client = RuleServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.get_rule_deployment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            rule.RuleDeployment(
                name="name_value",
                enabled=True,
                alerting=True,
                archived=True,
                run_frequency=rule.RunFrequency.LIVE,
                execution_state=rule.RuleDeployment.ExecutionState.DEFAULT,
                producer_rules=["producer_rules_value"],
                consumer_rules=["consumer_rules_value"],
            )
        )
        await client.get_rule_deployment(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = rule.GetRuleDeploymentRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_list_rule_deployments_empty_call_grpc_asyncio():
    client = RuleServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.list_rule_deployments), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            rule.ListRuleDeploymentsResponse(
                next_page_token="next_page_token_value",
            )
        )
        await client.list_rule_deployments(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = rule.ListRuleDeploymentsRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_update_rule_deployment_empty_call_grpc_asyncio():
    client = RuleServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.update_rule_deployment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            rule.RuleDeployment(
                name="name_value",
                enabled=True,
                alerting=True,
                archived=True,
                run_frequency=rule.RunFrequency.LIVE,
                execution_state=rule.RuleDeployment.ExecutionState.DEFAULT,
                producer_rules=["producer_rules_value"],
                consumer_rules=["consumer_rules_value"],
            )
        )
        await client.update_rule_deployment(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = rule.UpdateRuleDeploymentRequest()

        assert args[0] == request_msg


def test_transport_kind_rest():
    transport = RuleServiceClient.get_transport_class("rest")(
        credentials=ga_credentials.AnonymousCredentials()
    )
    assert transport.kind == "rest"


def test_create_rule_rest_bad_request(request_type=gcc_rule.CreateRuleRequest):
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2/instances/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        json_return_value = ""
        response_value.json = mock.Mock(return_value={})
        response_value.status_code = 400
        response_value.request = mock.Mock()
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        client.create_rule(request)


@pytest.mark.parametrize(
    "request_type",
    [
        gcc_rule.CreateRuleRequest,
        dict,
    ],
)
def test_create_rule_rest_call_success(request_type):
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2/instances/sample3"}
    request_init["rule"] = {
        "name": "name_value",
        "revision_id": "revision_id_value",
        "display_name": "display_name_value",
        "text": "text_value",
        "author": "author_value",
        "severity": {"display_name": "display_name_value"},
        "metadata": {},
        "create_time": {"seconds": 751, "nanos": 543},
        "revision_create_time": {},
        "compilation_state": 1,
        "type_": 1,
        "reference_lists": ["reference_lists_value1", "reference_lists_value2"],
        "allowed_run_frequencies": [1],
        "etag": "etag_value",
        "scope": "scope_value",
        "compilation_diagnostics": [
            {
                "message": "message_value",
                "position": {
                    "start_line": 1077,
                    "start_column": 1307,
                    "end_line": 830,
                    "end_column": 1060,
                },
                "severity": 1,
                "uri": "uri_value",
            }
        ],
        "near_real_time_live_rule_eligible": True,
        "inputs_used": {"uses_udm": True, "uses_entity": True, "uses_detection": True},
    }
    # The version of a generated dependency at test runtime may differ from the version used during generation.
    # Delete any fields which are not present in the current runtime dependency
    # See https://github.com/googleapis/gapic-generator-python/issues/1748

    # Determine if the message type is proto-plus or protobuf
    test_field = gcc_rule.CreateRuleRequest.meta.fields["rule"]

    def get_message_fields(field):
        # Given a field which is a message (composite type), return a list with
        # all the fields of the message.
        # If the field is not a composite type, return an empty list.
        message_fields = []

        if hasattr(field, "message") and field.message:
            is_field_type_proto_plus_type = not hasattr(field.message, "DESCRIPTOR")

            if is_field_type_proto_plus_type:
                message_fields = field.message.meta.fields.values()
            # Add `# pragma: NO COVER` because there may not be any `*_pb2` field types
            else:  # pragma: NO COVER
                message_fields = field.message.DESCRIPTOR.fields
        return message_fields

    runtime_nested_fields = [
        (field.name, nested_field.name)
        for field in get_message_fields(test_field)
        for nested_field in get_message_fields(field)
    ]

    subfields_not_in_runtime = []

    # For each item in the sample request, create a list of sub fields which are not present at runtime
    # Add `# pragma: NO COVER` because this test code will not run if all subfields are present at runtime
    for field, value in request_init["rule"].items():  # pragma: NO COVER
        result = None
        is_repeated = False
        # For repeated fields
        if isinstance(value, list) and len(value):
            is_repeated = True
            result = value[0]
        # For fields where the type is another message
        if isinstance(value, dict):
            result = value

        if result and hasattr(result, "keys"):
            for subfield in result.keys():
                if (field, subfield) not in runtime_nested_fields:
                    subfields_not_in_runtime.append(
                        {
                            "field": field,
                            "subfield": subfield,
                            "is_repeated": is_repeated,
                        }
                    )

    # Remove fields from the sample request which are not present in the runtime version of the dependency
    # Add `# pragma: NO COVER` because this test code will not run if all subfields are present at runtime
    for subfield_to_delete in subfields_not_in_runtime:  # pragma: NO COVER
        field = subfield_to_delete.get("field")
        field_repeated = subfield_to_delete.get("is_repeated")
        subfield = subfield_to_delete.get("subfield")
        if subfield:
            if field_repeated:
                for i in range(0, len(request_init["rule"][field])):
                    del request_init["rule"][field][i][subfield]
            else:
                del request_init["rule"][field][subfield]
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = gcc_rule.Rule(
            name="name_value",
            revision_id="revision_id_value",
            display_name="display_name_value",
            text="text_value",
            author="author_value",
            compilation_state=gcc_rule.Rule.CompilationState.SUCCEEDED,
            type_=gcc_rule.RuleType.SINGLE_EVENT,
            reference_lists=["reference_lists_value"],
            allowed_run_frequencies=[gcc_rule.RunFrequency.LIVE],
            etag="etag_value",
            scope="scope_value",
            near_real_time_live_rule_eligible=True,
        )

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200

        # Convert return value to protobuf type
        return_value = gcc_rule.Rule.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value.content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        response = client.create_rule(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, gcc_rule.Rule)
    assert response.name == "name_value"
    assert response.revision_id == "revision_id_value"
    assert response.display_name == "display_name_value"
    assert response.text == "text_value"
    assert response.author == "author_value"
    assert response.compilation_state == gcc_rule.Rule.CompilationState.SUCCEEDED
    assert response.type_ == gcc_rule.RuleType.SINGLE_EVENT
    assert response.reference_lists == ["reference_lists_value"]
    assert response.allowed_run_frequencies == [gcc_rule.RunFrequency.LIVE]
    assert response.etag == "etag_value"
    assert response.scope == "scope_value"
    assert response.near_real_time_live_rule_eligible is True


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_create_rule_rest_interceptors(null_interceptor):
    transport = transports.RuleServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.RuleServiceRestInterceptor(),
    )
    client = RuleServiceClient(transport=transport)

    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.RuleServiceRestInterceptor, "post_create_rule"
    ) as post, mock.patch.object(
        transports.RuleServiceRestInterceptor, "post_create_rule_with_metadata"
    ) as post_with_metadata, mock.patch.object(
        transports.RuleServiceRestInterceptor, "pre_create_rule"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        post_with_metadata.assert_not_called()
        pb_message = gcc_rule.CreateRuleRequest.pb(gcc_rule.CreateRuleRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = mock.Mock()
        req.return_value.status_code = 200
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        return_value = gcc_rule.Rule.to_json(gcc_rule.Rule())
        req.return_value.content = return_value

        request = gcc_rule.CreateRuleRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = gcc_rule.Rule()
        post_with_metadata.return_value = gcc_rule.Rule(), metadata

        client.create_rule(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()
        post_with_metadata.assert_called_once()


def test_get_rule_rest_bad_request(request_type=rule.GetRuleRequest):
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/instances/sample3/rules/sample4"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        json_return_value = ""
        response_value.json = mock.Mock(return_value={})
        response_value.status_code = 400
        response_value.request = mock.Mock()
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        client.get_rule(request)


@pytest.mark.parametrize(
    "request_type",
    [
        rule.GetRuleRequest,
        dict,
    ],
)
def test_get_rule_rest_call_success(request_type):
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/instances/sample3/rules/sample4"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = rule.Rule(
            name="name_value",
            revision_id="revision_id_value",
            display_name="display_name_value",
            text="text_value",
            author="author_value",
            compilation_state=rule.Rule.CompilationState.SUCCEEDED,
            type_=rule.RuleType.SINGLE_EVENT,
            reference_lists=["reference_lists_value"],
            allowed_run_frequencies=[rule.RunFrequency.LIVE],
            etag="etag_value",
            scope="scope_value",
            near_real_time_live_rule_eligible=True,
        )

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200

        # Convert return value to protobuf type
        return_value = rule.Rule.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value.content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        response = client.get_rule(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, rule.Rule)
    assert response.name == "name_value"
    assert response.revision_id == "revision_id_value"
    assert response.display_name == "display_name_value"
    assert response.text == "text_value"
    assert response.author == "author_value"
    assert response.compilation_state == rule.Rule.CompilationState.SUCCEEDED
    assert response.type_ == rule.RuleType.SINGLE_EVENT
    assert response.reference_lists == ["reference_lists_value"]
    assert response.allowed_run_frequencies == [rule.RunFrequency.LIVE]
    assert response.etag == "etag_value"
    assert response.scope == "scope_value"
    assert response.near_real_time_live_rule_eligible is True


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_rule_rest_interceptors(null_interceptor):
    transport = transports.RuleServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.RuleServiceRestInterceptor(),
    )
    client = RuleServiceClient(transport=transport)

    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.RuleServiceRestInterceptor, "post_get_rule"
    ) as post, mock.patch.object(
        transports.RuleServiceRestInterceptor, "post_get_rule_with_metadata"
    ) as post_with_metadata, mock.patch.object(
        transports.RuleServiceRestInterceptor, "pre_get_rule"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        post_with_metadata.assert_not_called()
        pb_message = rule.GetRuleRequest.pb(rule.GetRuleRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = mock.Mock()
        req.return_value.status_code = 200
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        return_value = rule.Rule.to_json(rule.Rule())
        req.return_value.content = return_value

        request = rule.GetRuleRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = rule.Rule()
        post_with_metadata.return_value = rule.Rule(), metadata

        client.get_rule(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()
        post_with_metadata.assert_called_once()


def test_list_rules_rest_bad_request(request_type=rule.ListRulesRequest):
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2/instances/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        json_return_value = ""
        response_value.json = mock.Mock(return_value={})
        response_value.status_code = 400
        response_value.request = mock.Mock()
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        client.list_rules(request)


@pytest.mark.parametrize(
    "request_type",
    [
        rule.ListRulesRequest,
        dict,
    ],
)
def test_list_rules_rest_call_success(request_type):
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2/instances/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = rule.ListRulesResponse(
            next_page_token="next_page_token_value",
        )

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200

        # Convert return value to protobuf type
        return_value = rule.ListRulesResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value.content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        response = client.list_rules(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListRulesPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_list_rules_rest_interceptors(null_interceptor):
    transport = transports.RuleServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.RuleServiceRestInterceptor(),
    )
    client = RuleServiceClient(transport=transport)

    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.RuleServiceRestInterceptor, "post_list_rules"
    ) as post, mock.patch.object(
        transports.RuleServiceRestInterceptor, "post_list_rules_with_metadata"
    ) as post_with_metadata, mock.patch.object(
        transports.RuleServiceRestInterceptor, "pre_list_rules"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        post_with_metadata.assert_not_called()
        pb_message = rule.ListRulesRequest.pb(rule.ListRulesRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = mock.Mock()
        req.return_value.status_code = 200
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        return_value = rule.ListRulesResponse.to_json(rule.ListRulesResponse())
        req.return_value.content = return_value

        request = rule.ListRulesRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = rule.ListRulesResponse()
        post_with_metadata.return_value = rule.ListRulesResponse(), metadata

        client.list_rules(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()
        post_with_metadata.assert_called_once()


def test_update_rule_rest_bad_request(request_type=gcc_rule.UpdateRuleRequest):
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    # send a request that will satisfy transcoding
    request_init = {
        "rule": {
            "name": "projects/sample1/locations/sample2/instances/sample3/rules/sample4"
        }
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        json_return_value = ""
        response_value.json = mock.Mock(return_value={})
        response_value.status_code = 400
        response_value.request = mock.Mock()
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        client.update_rule(request)


@pytest.mark.parametrize(
    "request_type",
    [
        gcc_rule.UpdateRuleRequest,
        dict,
    ],
)
def test_update_rule_rest_call_success(request_type):
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )

    # send a request that will satisfy transcoding
    request_init = {
        "rule": {
            "name": "projects/sample1/locations/sample2/instances/sample3/rules/sample4"
        }
    }
    request_init["rule"] = {
        "name": "projects/sample1/locations/sample2/instances/sample3/rules/sample4",
        "revision_id": "revision_id_value",
        "display_name": "display_name_value",
        "text": "text_value",
        "author": "author_value",
        "severity": {"display_name": "display_name_value"},
        "metadata": {},
        "create_time": {"seconds": 751, "nanos": 543},
        "revision_create_time": {},
        "compilation_state": 1,
        "type_": 1,
        "reference_lists": ["reference_lists_value1", "reference_lists_value2"],
        "allowed_run_frequencies": [1],
        "etag": "etag_value",
        "scope": "scope_value",
        "compilation_diagnostics": [
            {
                "message": "message_value",
                "position": {
                    "start_line": 1077,
                    "start_column": 1307,
                    "end_line": 830,
                    "end_column": 1060,
                },
                "severity": 1,
                "uri": "uri_value",
            }
        ],
        "near_real_time_live_rule_eligible": True,
        "inputs_used": {"uses_udm": True, "uses_entity": True, "uses_detection": True},
    }
    # The version of a generated dependency at test runtime may differ from the version used during generation.
    # Delete any fields which are not present in the current runtime dependency
    # See https://github.com/googleapis/gapic-generator-python/issues/1748

    # Determine if the message type is proto-plus or protobuf
    test_field = gcc_rule.UpdateRuleRequest.meta.fields["rule"]

    def get_message_fields(field):
        # Given a field which is a message (composite type), return a list with
        # all the fields of the message.
        # If the field is not a composite type, return an empty list.
        message_fields = []

        if hasattr(field, "message") and field.message:
            is_field_type_proto_plus_type = not hasattr(field.message, "DESCRIPTOR")

            if is_field_type_proto_plus_type:
                message_fields = field.message.meta.fields.values()
            # Add `# pragma: NO COVER` because there may not be any `*_pb2` field types
            else:  # pragma: NO COVER
                message_fields = field.message.DESCRIPTOR.fields
        return message_fields

    runtime_nested_fields = [
        (field.name, nested_field.name)
        for field in get_message_fields(test_field)
        for nested_field in get_message_fields(field)
    ]

    subfields_not_in_runtime = []

    # For each item in the sample request, create a list of sub fields which are not present at runtime
    # Add `# pragma: NO COVER` because this test code will not run if all subfields are present at runtime
    for field, value in request_init["rule"].items():  # pragma: NO COVER
        result = None
        is_repeated = False
        # For repeated fields
        if isinstance(value, list) and len(value):
            is_repeated = True
            result = value[0]
        # For fields where the type is another message
        if isinstance(value, dict):
            result = value

        if result and hasattr(result, "keys"):
            for subfield in result.keys():
                if (field, subfield) not in runtime_nested_fields:
                    subfields_not_in_runtime.append(
                        {
                            "field": field,
                            "subfield": subfield,
                            "is_repeated": is_repeated,
                        }
                    )

    # Remove fields from the sample request which are not present in the runtime version of the dependency
    # Add `# pragma: NO COVER` because this test code will not run if all subfields are present at runtime
    for subfield_to_delete in subfields_not_in_runtime:  # pragma: NO COVER
        field = subfield_to_delete.get("field")
        field_repeated = subfield_to_delete.get("is_repeated")
        subfield = subfield_to_delete.get("subfield")
        if subfield:
            if field_repeated:
                for i in range(0, len(request_init["rule"][field])):
                    del request_init["rule"][field][i][subfield]
            else:
                del request_init["rule"][field][subfield]
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = gcc_rule.Rule(
            name="name_value",
            revision_id="revision_id_value",
            display_name="display_name_value",
            text="text_value",
            author="author_value",
            compilation_state=gcc_rule.Rule.CompilationState.SUCCEEDED,
            type_=gcc_rule.RuleType.SINGLE_EVENT,
            reference_lists=["reference_lists_value"],
            allowed_run_frequencies=[gcc_rule.RunFrequency.LIVE],
            etag="etag_value",
            scope="scope_value",
            near_real_time_live_rule_eligible=True,
        )

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200

        # Convert return value to protobuf type
        return_value = gcc_rule.Rule.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value.content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        response = client.update_rule(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, gcc_rule.Rule)
    assert response.name == "name_value"
    assert response.revision_id == "revision_id_value"
    assert response.display_name == "display_name_value"
    assert response.text == "text_value"
    assert response.author == "author_value"
    assert response.compilation_state == gcc_rule.Rule.CompilationState.SUCCEEDED
    assert response.type_ == gcc_rule.RuleType.SINGLE_EVENT
    assert response.reference_lists == ["reference_lists_value"]
    assert response.allowed_run_frequencies == [gcc_rule.RunFrequency.LIVE]
    assert response.etag == "etag_value"
    assert response.scope == "scope_value"
    assert response.near_real_time_live_rule_eligible is True


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_update_rule_rest_interceptors(null_interceptor):
    transport = transports.RuleServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.RuleServiceRestInterceptor(),
    )
    client = RuleServiceClient(transport=transport)

    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.RuleServiceRestInterceptor, "post_update_rule"
    ) as post, mock.patch.object(
        transports.RuleServiceRestInterceptor, "post_update_rule_with_metadata"
    ) as post_with_metadata, mock.patch.object(
        transports.RuleServiceRestInterceptor, "pre_update_rule"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        post_with_metadata.assert_not_called()
        pb_message = gcc_rule.UpdateRuleRequest.pb(gcc_rule.UpdateRuleRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = mock.Mock()
        req.return_value.status_code = 200
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        return_value = gcc_rule.Rule.to_json(gcc_rule.Rule())
        req.return_value.content = return_value

        request = gcc_rule.UpdateRuleRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = gcc_rule.Rule()
        post_with_metadata.return_value = gcc_rule.Rule(), metadata

        client.update_rule(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()
        post_with_metadata.assert_called_once()


def test_delete_rule_rest_bad_request(request_type=rule.DeleteRuleRequest):
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/instances/sample3/rules/sample4"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        json_return_value = ""
        response_value.json = mock.Mock(return_value={})
        response_value.status_code = 400
        response_value.request = mock.Mock()
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        client.delete_rule(request)


@pytest.mark.parametrize(
    "request_type",
    [
        rule.DeleteRuleRequest,
        dict,
    ],
)
def test_delete_rule_rest_call_success(request_type):
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/instances/sample3/rules/sample4"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = None

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200
        json_return_value = ""
        response_value.content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        response = client.delete_rule(request)

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_delete_rule_rest_interceptors(null_interceptor):
    transport = transports.RuleServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.RuleServiceRestInterceptor(),
    )
    client = RuleServiceClient(transport=transport)

    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.RuleServiceRestInterceptor, "pre_delete_rule"
    ) as pre:
        pre.assert_not_called()
        pb_message = rule.DeleteRuleRequest.pb(rule.DeleteRuleRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = mock.Mock()
        req.return_value.status_code = 200
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

        request = rule.DeleteRuleRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata

        client.delete_rule(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()


def test_list_rule_revisions_rest_bad_request(
    request_type=rule.ListRuleRevisionsRequest,
):
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/instances/sample3/rules/sample4"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        json_return_value = ""
        response_value.json = mock.Mock(return_value={})
        response_value.status_code = 400
        response_value.request = mock.Mock()
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        client.list_rule_revisions(request)


@pytest.mark.parametrize(
    "request_type",
    [
        rule.ListRuleRevisionsRequest,
        dict,
    ],
)
def test_list_rule_revisions_rest_call_success(request_type):
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/instances/sample3/rules/sample4"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = rule.ListRuleRevisionsResponse(
            next_page_token="next_page_token_value",
        )

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200

        # Convert return value to protobuf type
        return_value = rule.ListRuleRevisionsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value.content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        response = client.list_rule_revisions(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListRuleRevisionsPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_list_rule_revisions_rest_interceptors(null_interceptor):
    transport = transports.RuleServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.RuleServiceRestInterceptor(),
    )
    client = RuleServiceClient(transport=transport)

    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.RuleServiceRestInterceptor, "post_list_rule_revisions"
    ) as post, mock.patch.object(
        transports.RuleServiceRestInterceptor, "post_list_rule_revisions_with_metadata"
    ) as post_with_metadata, mock.patch.object(
        transports.RuleServiceRestInterceptor, "pre_list_rule_revisions"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        post_with_metadata.assert_not_called()
        pb_message = rule.ListRuleRevisionsRequest.pb(rule.ListRuleRevisionsRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = mock.Mock()
        req.return_value.status_code = 200
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        return_value = rule.ListRuleRevisionsResponse.to_json(
            rule.ListRuleRevisionsResponse()
        )
        req.return_value.content = return_value

        request = rule.ListRuleRevisionsRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = rule.ListRuleRevisionsResponse()
        post_with_metadata.return_value = rule.ListRuleRevisionsResponse(), metadata

        client.list_rule_revisions(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()
        post_with_metadata.assert_called_once()


def test_create_retrohunt_rest_bad_request(request_type=rule.CreateRetrohuntRequest):
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    # send a request that will satisfy transcoding
    request_init = {
        "parent": "projects/sample1/locations/sample2/instances/sample3/rules/sample4"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        json_return_value = ""
        response_value.json = mock.Mock(return_value={})
        response_value.status_code = 400
        response_value.request = mock.Mock()
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        client.create_retrohunt(request)


@pytest.mark.parametrize(
    "request_type",
    [
        rule.CreateRetrohuntRequest,
        dict,
    ],
)
def test_create_retrohunt_rest_call_success(request_type):
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )

    # send a request that will satisfy transcoding
    request_init = {
        "parent": "projects/sample1/locations/sample2/instances/sample3/rules/sample4"
    }
    request_init["retrohunt"] = {
        "name": "name_value",
        "process_interval": {
            "start_time": {"seconds": 751, "nanos": 543},
            "end_time": {},
        },
        "execution_interval": {},
        "state": 1,
        "progress_percentage": 0.2034,
    }
    # The version of a generated dependency at test runtime may differ from the version used during generation.
    # Delete any fields which are not present in the current runtime dependency
    # See https://github.com/googleapis/gapic-generator-python/issues/1748

    # Determine if the message type is proto-plus or protobuf
    test_field = rule.CreateRetrohuntRequest.meta.fields["retrohunt"]

    def get_message_fields(field):
        # Given a field which is a message (composite type), return a list with
        # all the fields of the message.
        # If the field is not a composite type, return an empty list.
        message_fields = []

        if hasattr(field, "message") and field.message:
            is_field_type_proto_plus_type = not hasattr(field.message, "DESCRIPTOR")

            if is_field_type_proto_plus_type:
                message_fields = field.message.meta.fields.values()
            # Add `# pragma: NO COVER` because there may not be any `*_pb2` field types
            else:  # pragma: NO COVER
                message_fields = field.message.DESCRIPTOR.fields
        return message_fields

    runtime_nested_fields = [
        (field.name, nested_field.name)
        for field in get_message_fields(test_field)
        for nested_field in get_message_fields(field)
    ]

    subfields_not_in_runtime = []

    # For each item in the sample request, create a list of sub fields which are not present at runtime
    # Add `# pragma: NO COVER` because this test code will not run if all subfields are present at runtime
    for field, value in request_init["retrohunt"].items():  # pragma: NO COVER
        result = None
        is_repeated = False
        # For repeated fields
        if isinstance(value, list) and len(value):
            is_repeated = True
            result = value[0]
        # For fields where the type is another message
        if isinstance(value, dict):
            result = value

        if result and hasattr(result, "keys"):
            for subfield in result.keys():
                if (field, subfield) not in runtime_nested_fields:
                    subfields_not_in_runtime.append(
                        {
                            "field": field,
                            "subfield": subfield,
                            "is_repeated": is_repeated,
                        }
                    )

    # Remove fields from the sample request which are not present in the runtime version of the dependency
    # Add `# pragma: NO COVER` because this test code will not run if all subfields are present at runtime
    for subfield_to_delete in subfields_not_in_runtime:  # pragma: NO COVER
        field = subfield_to_delete.get("field")
        field_repeated = subfield_to_delete.get("is_repeated")
        subfield = subfield_to_delete.get("subfield")
        if subfield:
            if field_repeated:
                for i in range(0, len(request_init["retrohunt"][field])):
                    del request_init["retrohunt"][field][i][subfield]
            else:
                del request_init["retrohunt"][field][subfield]
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value.content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        response = client.create_retrohunt(request)

    # Establish that the response is the type that we expect.
    json_return_value = json_format.MessageToJson(return_value)


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_create_retrohunt_rest_interceptors(null_interceptor):
    transport = transports.RuleServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.RuleServiceRestInterceptor(),
    )
    client = RuleServiceClient(transport=transport)

    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.RuleServiceRestInterceptor, "post_create_retrohunt"
    ) as post, mock.patch.object(
        transports.RuleServiceRestInterceptor, "post_create_retrohunt_with_metadata"
    ) as post_with_metadata, mock.patch.object(
        transports.RuleServiceRestInterceptor, "pre_create_retrohunt"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        post_with_metadata.assert_not_called()
        pb_message = rule.CreateRetrohuntRequest.pb(rule.CreateRetrohuntRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = mock.Mock()
        req.return_value.status_code = 200
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        return_value = json_format.MessageToJson(operations_pb2.Operation())
        req.return_value.content = return_value

        request = rule.CreateRetrohuntRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()
        post_with_metadata.return_value = operations_pb2.Operation(), metadata

        client.create_retrohunt(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()
        post_with_metadata.assert_called_once()


def test_get_retrohunt_rest_bad_request(request_type=rule.GetRetrohuntRequest):
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/instances/sample3/rules/sample4/retrohunts/sample5"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        json_return_value = ""
        response_value.json = mock.Mock(return_value={})
        response_value.status_code = 400
        response_value.request = mock.Mock()
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        client.get_retrohunt(request)


@pytest.mark.parametrize(
    "request_type",
    [
        rule.GetRetrohuntRequest,
        dict,
    ],
)
def test_get_retrohunt_rest_call_success(request_type):
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/instances/sample3/rules/sample4/retrohunts/sample5"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = rule.Retrohunt(
            name="name_value",
            state=rule.Retrohunt.State.RUNNING,
            progress_percentage=0.2034,
        )

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200

        # Convert return value to protobuf type
        return_value = rule.Retrohunt.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value.content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        response = client.get_retrohunt(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, rule.Retrohunt)
    assert response.name == "name_value"
    assert response.state == rule.Retrohunt.State.RUNNING
    assert math.isclose(response.progress_percentage, 0.2034, rel_tol=1e-6)


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_retrohunt_rest_interceptors(null_interceptor):
    transport = transports.RuleServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.RuleServiceRestInterceptor(),
    )
    client = RuleServiceClient(transport=transport)

    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.RuleServiceRestInterceptor, "post_get_retrohunt"
    ) as post, mock.patch.object(
        transports.RuleServiceRestInterceptor, "post_get_retrohunt_with_metadata"
    ) as post_with_metadata, mock.patch.object(
        transports.RuleServiceRestInterceptor, "pre_get_retrohunt"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        post_with_metadata.assert_not_called()
        pb_message = rule.GetRetrohuntRequest.pb(rule.GetRetrohuntRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = mock.Mock()
        req.return_value.status_code = 200
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        return_value = rule.Retrohunt.to_json(rule.Retrohunt())
        req.return_value.content = return_value

        request = rule.GetRetrohuntRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = rule.Retrohunt()
        post_with_metadata.return_value = rule.Retrohunt(), metadata

        client.get_retrohunt(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()
        post_with_metadata.assert_called_once()


def test_list_retrohunts_rest_bad_request(request_type=rule.ListRetrohuntsRequest):
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    # send a request that will satisfy transcoding
    request_init = {
        "parent": "projects/sample1/locations/sample2/instances/sample3/rules/sample4"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        json_return_value = ""
        response_value.json = mock.Mock(return_value={})
        response_value.status_code = 400
        response_value.request = mock.Mock()
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        client.list_retrohunts(request)


@pytest.mark.parametrize(
    "request_type",
    [
        rule.ListRetrohuntsRequest,
        dict,
    ],
)
def test_list_retrohunts_rest_call_success(request_type):
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )

    # send a request that will satisfy transcoding
    request_init = {
        "parent": "projects/sample1/locations/sample2/instances/sample3/rules/sample4"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = rule.ListRetrohuntsResponse(
            next_page_token="next_page_token_value",
        )

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200

        # Convert return value to protobuf type
        return_value = rule.ListRetrohuntsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value.content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        response = client.list_retrohunts(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListRetrohuntsPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_list_retrohunts_rest_interceptors(null_interceptor):
    transport = transports.RuleServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.RuleServiceRestInterceptor(),
    )
    client = RuleServiceClient(transport=transport)

    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.RuleServiceRestInterceptor, "post_list_retrohunts"
    ) as post, mock.patch.object(
        transports.RuleServiceRestInterceptor, "post_list_retrohunts_with_metadata"
    ) as post_with_metadata, mock.patch.object(
        transports.RuleServiceRestInterceptor, "pre_list_retrohunts"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        post_with_metadata.assert_not_called()
        pb_message = rule.ListRetrohuntsRequest.pb(rule.ListRetrohuntsRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = mock.Mock()
        req.return_value.status_code = 200
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        return_value = rule.ListRetrohuntsResponse.to_json(
            rule.ListRetrohuntsResponse()
        )
        req.return_value.content = return_value

        request = rule.ListRetrohuntsRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = rule.ListRetrohuntsResponse()
        post_with_metadata.return_value = rule.ListRetrohuntsResponse(), metadata

        client.list_retrohunts(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()
        post_with_metadata.assert_called_once()


def test_get_rule_deployment_rest_bad_request(
    request_type=rule.GetRuleDeploymentRequest,
):
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/instances/sample3/rules/sample4/deployment"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        json_return_value = ""
        response_value.json = mock.Mock(return_value={})
        response_value.status_code = 400
        response_value.request = mock.Mock()
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        client.get_rule_deployment(request)


@pytest.mark.parametrize(
    "request_type",
    [
        rule.GetRuleDeploymentRequest,
        dict,
    ],
)
def test_get_rule_deployment_rest_call_success(request_type):
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/instances/sample3/rules/sample4/deployment"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = rule.RuleDeployment(
            name="name_value",
            enabled=True,
            alerting=True,
            archived=True,
            run_frequency=rule.RunFrequency.LIVE,
            execution_state=rule.RuleDeployment.ExecutionState.DEFAULT,
            producer_rules=["producer_rules_value"],
            consumer_rules=["consumer_rules_value"],
        )

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200

        # Convert return value to protobuf type
        return_value = rule.RuleDeployment.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value.content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        response = client.get_rule_deployment(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, rule.RuleDeployment)
    assert response.name == "name_value"
    assert response.enabled is True
    assert response.alerting is True
    assert response.archived is True
    assert response.run_frequency == rule.RunFrequency.LIVE
    assert response.execution_state == rule.RuleDeployment.ExecutionState.DEFAULT
    assert response.producer_rules == ["producer_rules_value"]
    assert response.consumer_rules == ["consumer_rules_value"]


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_rule_deployment_rest_interceptors(null_interceptor):
    transport = transports.RuleServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.RuleServiceRestInterceptor(),
    )
    client = RuleServiceClient(transport=transport)

    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.RuleServiceRestInterceptor, "post_get_rule_deployment"
    ) as post, mock.patch.object(
        transports.RuleServiceRestInterceptor, "post_get_rule_deployment_with_metadata"
    ) as post_with_metadata, mock.patch.object(
        transports.RuleServiceRestInterceptor, "pre_get_rule_deployment"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        post_with_metadata.assert_not_called()
        pb_message = rule.GetRuleDeploymentRequest.pb(rule.GetRuleDeploymentRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = mock.Mock()
        req.return_value.status_code = 200
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        return_value = rule.RuleDeployment.to_json(rule.RuleDeployment())
        req.return_value.content = return_value

        request = rule.GetRuleDeploymentRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = rule.RuleDeployment()
        post_with_metadata.return_value = rule.RuleDeployment(), metadata

        client.get_rule_deployment(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()
        post_with_metadata.assert_called_once()


def test_list_rule_deployments_rest_bad_request(
    request_type=rule.ListRuleDeploymentsRequest,
):
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    # send a request that will satisfy transcoding
    request_init = {
        "parent": "projects/sample1/locations/sample2/instances/sample3/rules/sample4"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        json_return_value = ""
        response_value.json = mock.Mock(return_value={})
        response_value.status_code = 400
        response_value.request = mock.Mock()
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        client.list_rule_deployments(request)


@pytest.mark.parametrize(
    "request_type",
    [
        rule.ListRuleDeploymentsRequest,
        dict,
    ],
)
def test_list_rule_deployments_rest_call_success(request_type):
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )

    # send a request that will satisfy transcoding
    request_init = {
        "parent": "projects/sample1/locations/sample2/instances/sample3/rules/sample4"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = rule.ListRuleDeploymentsResponse(
            next_page_token="next_page_token_value",
        )

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200

        # Convert return value to protobuf type
        return_value = rule.ListRuleDeploymentsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value.content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        response = client.list_rule_deployments(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListRuleDeploymentsPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_list_rule_deployments_rest_interceptors(null_interceptor):
    transport = transports.RuleServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.RuleServiceRestInterceptor(),
    )
    client = RuleServiceClient(transport=transport)

    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.RuleServiceRestInterceptor, "post_list_rule_deployments"
    ) as post, mock.patch.object(
        transports.RuleServiceRestInterceptor,
        "post_list_rule_deployments_with_metadata",
    ) as post_with_metadata, mock.patch.object(
        transports.RuleServiceRestInterceptor, "pre_list_rule_deployments"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        post_with_metadata.assert_not_called()
        pb_message = rule.ListRuleDeploymentsRequest.pb(
            rule.ListRuleDeploymentsRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = mock.Mock()
        req.return_value.status_code = 200
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        return_value = rule.ListRuleDeploymentsResponse.to_json(
            rule.ListRuleDeploymentsResponse()
        )
        req.return_value.content = return_value

        request = rule.ListRuleDeploymentsRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = rule.ListRuleDeploymentsResponse()
        post_with_metadata.return_value = rule.ListRuleDeploymentsResponse(), metadata

        client.list_rule_deployments(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()
        post_with_metadata.assert_called_once()


def test_update_rule_deployment_rest_bad_request(
    request_type=rule.UpdateRuleDeploymentRequest,
):
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    # send a request that will satisfy transcoding
    request_init = {
        "rule_deployment": {
            "name": "projects/sample1/locations/sample2/instances/sample3/rules/sample4/deployment"
        }
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        json_return_value = ""
        response_value.json = mock.Mock(return_value={})
        response_value.status_code = 400
        response_value.request = mock.Mock()
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        client.update_rule_deployment(request)


@pytest.mark.parametrize(
    "request_type",
    [
        rule.UpdateRuleDeploymentRequest,
        dict,
    ],
)
def test_update_rule_deployment_rest_call_success(request_type):
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )

    # send a request that will satisfy transcoding
    request_init = {
        "rule_deployment": {
            "name": "projects/sample1/locations/sample2/instances/sample3/rules/sample4/deployment"
        }
    }
    request_init["rule_deployment"] = {
        "name": "projects/sample1/locations/sample2/instances/sample3/rules/sample4/deployment",
        "enabled": True,
        "alerting": True,
        "archived": True,
        "archive_time": {"seconds": 751, "nanos": 543},
        "run_frequency": 1,
        "execution_state": 1,
        "producer_rules": ["producer_rules_value1", "producer_rules_value2"],
        "consumer_rules": ["consumer_rules_value1", "consumer_rules_value2"],
        "last_alert_status_change_time": {},
    }
    # The version of a generated dependency at test runtime may differ from the version used during generation.
    # Delete any fields which are not present in the current runtime dependency
    # See https://github.com/googleapis/gapic-generator-python/issues/1748

    # Determine if the message type is proto-plus or protobuf
    test_field = rule.UpdateRuleDeploymentRequest.meta.fields["rule_deployment"]

    def get_message_fields(field):
        # Given a field which is a message (composite type), return a list with
        # all the fields of the message.
        # If the field is not a composite type, return an empty list.
        message_fields = []

        if hasattr(field, "message") and field.message:
            is_field_type_proto_plus_type = not hasattr(field.message, "DESCRIPTOR")

            if is_field_type_proto_plus_type:
                message_fields = field.message.meta.fields.values()
            # Add `# pragma: NO COVER` because there may not be any `*_pb2` field types
            else:  # pragma: NO COVER
                message_fields = field.message.DESCRIPTOR.fields
        return message_fields

    runtime_nested_fields = [
        (field.name, nested_field.name)
        for field in get_message_fields(test_field)
        for nested_field in get_message_fields(field)
    ]

    subfields_not_in_runtime = []

    # For each item in the sample request, create a list of sub fields which are not present at runtime
    # Add `# pragma: NO COVER` because this test code will not run if all subfields are present at runtime
    for field, value in request_init["rule_deployment"].items():  # pragma: NO COVER
        result = None
        is_repeated = False
        # For repeated fields
        if isinstance(value, list) and len(value):
            is_repeated = True
            result = value[0]
        # For fields where the type is another message
        if isinstance(value, dict):
            result = value

        if result and hasattr(result, "keys"):
            for subfield in result.keys():
                if (field, subfield) not in runtime_nested_fields:
                    subfields_not_in_runtime.append(
                        {
                            "field": field,
                            "subfield": subfield,
                            "is_repeated": is_repeated,
                        }
                    )

    # Remove fields from the sample request which are not present in the runtime version of the dependency
    # Add `# pragma: NO COVER` because this test code will not run if all subfields are present at runtime
    for subfield_to_delete in subfields_not_in_runtime:  # pragma: NO COVER
        field = subfield_to_delete.get("field")
        field_repeated = subfield_to_delete.get("is_repeated")
        subfield = subfield_to_delete.get("subfield")
        if subfield:
            if field_repeated:
                for i in range(0, len(request_init["rule_deployment"][field])):
                    del request_init["rule_deployment"][field][i][subfield]
            else:
                del request_init["rule_deployment"][field][subfield]
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = rule.RuleDeployment(
            name="name_value",
            enabled=True,
            alerting=True,
            archived=True,
            run_frequency=rule.RunFrequency.LIVE,
            execution_state=rule.RuleDeployment.ExecutionState.DEFAULT,
            producer_rules=["producer_rules_value"],
            consumer_rules=["consumer_rules_value"],
        )

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200

        # Convert return value to protobuf type
        return_value = rule.RuleDeployment.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value.content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        response = client.update_rule_deployment(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, rule.RuleDeployment)
    assert response.name == "name_value"
    assert response.enabled is True
    assert response.alerting is True
    assert response.archived is True
    assert response.run_frequency == rule.RunFrequency.LIVE
    assert response.execution_state == rule.RuleDeployment.ExecutionState.DEFAULT
    assert response.producer_rules == ["producer_rules_value"]
    assert response.consumer_rules == ["consumer_rules_value"]


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_update_rule_deployment_rest_interceptors(null_interceptor):
    transport = transports.RuleServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.RuleServiceRestInterceptor(),
    )
    client = RuleServiceClient(transport=transport)

    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.RuleServiceRestInterceptor, "post_update_rule_deployment"
    ) as post, mock.patch.object(
        transports.RuleServiceRestInterceptor,
        "post_update_rule_deployment_with_metadata",
    ) as post_with_metadata, mock.patch.object(
        transports.RuleServiceRestInterceptor, "pre_update_rule_deployment"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        post_with_metadata.assert_not_called()
        pb_message = rule.UpdateRuleDeploymentRequest.pb(
            rule.UpdateRuleDeploymentRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = mock.Mock()
        req.return_value.status_code = 200
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        return_value = rule.RuleDeployment.to_json(rule.RuleDeployment())
        req.return_value.content = return_value

        request = rule.UpdateRuleDeploymentRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = rule.RuleDeployment()
        post_with_metadata.return_value = rule.RuleDeployment(), metadata

        client.update_rule_deployment(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()
        post_with_metadata.assert_called_once()


def test_cancel_operation_rest_bad_request(
    request_type=operations_pb2.CancelOperationRequest,
):
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type()
    request = json_format.ParseDict(
        {
            "name": "projects/sample1/locations/sample2/instances/sample3/operations/sample4"
        },
        request,
    )

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        json_return_value = ""
        response_value.json = mock.Mock(return_value={})
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        client.cancel_operation(request)


@pytest.mark.parametrize(
    "request_type",
    [
        operations_pb2.CancelOperationRequest,
        dict,
    ],
)
def test_cancel_operation_rest(request_type):
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    request_init = {
        "name": "projects/sample1/locations/sample2/instances/sample3/operations/sample4"
    }
    request = request_type(**request_init)
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = None

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200
        json_return_value = "{}"
        response_value.content = json_return_value.encode("UTF-8")

        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

        response = client.cancel_operation(request)

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_operation_rest_bad_request(
    request_type=operations_pb2.DeleteOperationRequest,
):
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type()
    request = json_format.ParseDict(
        {
            "name": "projects/sample1/locations/sample2/instances/sample3/operations/sample4"
        },
        request,
    )

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        json_return_value = ""
        response_value.json = mock.Mock(return_value={})
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        client.delete_operation(request)


@pytest.mark.parametrize(
    "request_type",
    [
        operations_pb2.DeleteOperationRequest,
        dict,
    ],
)
def test_delete_operation_rest(request_type):
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    request_init = {
        "name": "projects/sample1/locations/sample2/instances/sample3/operations/sample4"
    }
    request = request_type(**request_init)
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = None

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200
        json_return_value = "{}"
        response_value.content = json_return_value.encode("UTF-8")

        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

        response = client.delete_operation(request)

    # Establish that the response is the type that we expect.
    assert response is None


def test_get_operation_rest_bad_request(
    request_type=operations_pb2.GetOperationRequest,
):
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type()
    request = json_format.ParseDict(
        {
            "name": "projects/sample1/locations/sample2/instances/sample3/operations/sample4"
        },
        request,
    )

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        json_return_value = ""
        response_value.json = mock.Mock(return_value={})
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        client.get_operation(request)


@pytest.mark.parametrize(
    "request_type",
    [
        operations_pb2.GetOperationRequest,
        dict,
    ],
)
def test_get_operation_rest(request_type):
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    request_init = {
        "name": "projects/sample1/locations/sample2/instances/sample3/operations/sample4"
    }
    request = request_type(**request_init)
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation()

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value.content = json_return_value.encode("UTF-8")

        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

        response = client.get_operation(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, operations_pb2.Operation)


def test_list_operations_rest_bad_request(
    request_type=operations_pb2.ListOperationsRequest,
):
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type()
    request = json_format.ParseDict(
        {"name": "projects/sample1/locations/sample2/instances/sample3"}, request
    )

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        json_return_value = ""
        response_value.json = mock.Mock(return_value={})
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        client.list_operations(request)


@pytest.mark.parametrize(
    "request_type",
    [
        operations_pb2.ListOperationsRequest,
        dict,
    ],
)
def test_list_operations_rest(request_type):
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    request_init = {"name": "projects/sample1/locations/sample2/instances/sample3"}
    request = request_type(**request_init)
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.ListOperationsResponse()

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value.content = json_return_value.encode("UTF-8")

        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

        response = client.list_operations(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, operations_pb2.ListOperationsResponse)


def test_initialize_client_w_rest():
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    assert client is not None


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_create_rule_empty_call_rest():
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.create_rule), "__call__") as call:
        client.create_rule(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = gcc_rule.CreateRuleRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_get_rule_empty_call_rest():
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.get_rule), "__call__") as call:
        client.get_rule(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = rule.GetRuleRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_list_rules_empty_call_rest():
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.list_rules), "__call__") as call:
        client.list_rules(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = rule.ListRulesRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_update_rule_empty_call_rest():
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.update_rule), "__call__") as call:
        client.update_rule(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = gcc_rule.UpdateRuleRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_delete_rule_empty_call_rest():
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.delete_rule), "__call__") as call:
        client.delete_rule(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = rule.DeleteRuleRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_list_rule_revisions_empty_call_rest():
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.list_rule_revisions), "__call__"
    ) as call:
        client.list_rule_revisions(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = rule.ListRuleRevisionsRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_create_retrohunt_empty_call_rest():
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.create_retrohunt), "__call__") as call:
        client.create_retrohunt(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = rule.CreateRetrohuntRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_get_retrohunt_empty_call_rest():
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.get_retrohunt), "__call__") as call:
        client.get_retrohunt(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = rule.GetRetrohuntRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_list_retrohunts_empty_call_rest():
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.list_retrohunts), "__call__") as call:
        client.list_retrohunts(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = rule.ListRetrohuntsRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_get_rule_deployment_empty_call_rest():
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.get_rule_deployment), "__call__"
    ) as call:
        client.get_rule_deployment(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = rule.GetRuleDeploymentRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_list_rule_deployments_empty_call_rest():
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.list_rule_deployments), "__call__"
    ) as call:
        client.list_rule_deployments(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = rule.ListRuleDeploymentsRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_update_rule_deployment_empty_call_rest():
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.update_rule_deployment), "__call__"
    ) as call:
        client.update_rule_deployment(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = rule.UpdateRuleDeploymentRequest()

        assert args[0] == request_msg


def test_rule_service_rest_lro_client():
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    transport = client.transport

    # Ensure that we have an api-core operations client.
    assert isinstance(
        transport.operations_client,
        operations_v1.AbstractOperationsClient,
    )

    # Ensure that subsequent calls to the property send the exact same object.
    assert transport.operations_client is transport.operations_client


def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert isinstance(
        client.transport,
        transports.RuleServiceGrpcTransport,
    )


def test_rule_service_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(core_exceptions.DuplicateCredentialArgs):
        transport = transports.RuleServiceTransport(
            credentials=ga_credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_rule_service_base_transport():
    # Instantiate the base transport.
    with mock.patch(
        "google.cloud.chronicle_v1.services.rule_service.transports.RuleServiceTransport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.RuleServiceTransport(
            credentials=ga_credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "create_rule",
        "get_rule",
        "list_rules",
        "update_rule",
        "delete_rule",
        "list_rule_revisions",
        "create_retrohunt",
        "get_retrohunt",
        "list_retrohunts",
        "get_rule_deployment",
        "list_rule_deployments",
        "update_rule_deployment",
        "get_operation",
        "cancel_operation",
        "delete_operation",
        "list_operations",
    )
    for method in methods:
        with pytest.raises(NotImplementedError):
            getattr(transport, method)(request=object())

    with pytest.raises(NotImplementedError):
        transport.close()

    # Additionally, the LRO client (a property) should
    # also raise NotImplementedError
    with pytest.raises(NotImplementedError):
        transport.operations_client

    # Catch all for all remaining methods and properties
    remainder = [
        "kind",
    ]
    for r in remainder:
        with pytest.raises(NotImplementedError):
            getattr(transport, r)()


def test_rule_service_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch(
        "google.cloud.chronicle_v1.services.rule_service.transports.RuleServiceTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.RuleServiceTransport(
            credentials_file="credentials.json",
            quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id="octopus",
        )


def test_rule_service_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(google.auth, "default", autospec=True) as adc, mock.patch(
        "google.cloud.chronicle_v1.services.rule_service.transports.RuleServiceTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.RuleServiceTransport()
        adc.assert_called_once()


def test_rule_service_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        RuleServiceClient()
        adc.assert_called_once_with(
            scopes=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id=None,
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.RuleServiceGrpcTransport,
        transports.RuleServiceGrpcAsyncIOTransport,
    ],
)
def test_rule_service_transport_auth_adc(transport_class):
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport_class(quota_project_id="octopus", scopes=["1", "2"])
        adc.assert_called_once_with(
            scopes=["1", "2"],
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id="octopus",
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.RuleServiceGrpcTransport,
        transports.RuleServiceGrpcAsyncIOTransport,
        transports.RuleServiceRestTransport,
    ],
)
def test_rule_service_transport_auth_gdch_credentials(transport_class):
    host = "https://language.com"
    api_audience_tests = [None, "https://language2.com"]
    api_audience_expect = [host, "https://language2.com"]
    for t, e in zip(api_audience_tests, api_audience_expect):
        with mock.patch.object(google.auth, "default", autospec=True) as adc:
            gdch_mock = mock.MagicMock()
            type(gdch_mock).with_gdch_audience = mock.PropertyMock(
                return_value=gdch_mock
            )
            adc.return_value = (gdch_mock, None)
            transport_class(host=host, api_audience=t)
            gdch_mock.with_gdch_audience.assert_called_once_with(e)


@pytest.mark.parametrize(
    "transport_class,grpc_helpers",
    [
        (transports.RuleServiceGrpcTransport, grpc_helpers),
        (transports.RuleServiceGrpcAsyncIOTransport, grpc_helpers_async),
    ],
)
def test_rule_service_transport_create_channel(transport_class, grpc_helpers):
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(
        google.auth, "default", autospec=True
    ) as adc, mock.patch.object(
        grpc_helpers, "create_channel", autospec=True
    ) as create_channel:
        creds = ga_credentials.AnonymousCredentials()
        adc.return_value = (creds, None)
        transport_class(quota_project_id="octopus", scopes=["1", "2"])

        create_channel.assert_called_with(
            "chronicle.googleapis.com:443",
            credentials=creds,
            credentials_file=None,
            quota_project_id="octopus",
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            scopes=["1", "2"],
            default_host="chronicle.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "transport_class",
    [transports.RuleServiceGrpcTransport, transports.RuleServiceGrpcAsyncIOTransport],
)
def test_rule_service_grpc_transport_client_cert_source_for_mtls(transport_class):
    cred = ga_credentials.AnonymousCredentials()

    # Check ssl_channel_credentials is used if provided.
    with mock.patch.object(transport_class, "create_channel") as mock_create_channel:
        mock_ssl_channel_creds = mock.Mock()
        transport_class(
            host="squid.clam.whelk",
            credentials=cred,
            ssl_channel_credentials=mock_ssl_channel_creds,
        )
        mock_create_channel.assert_called_once_with(
            "squid.clam.whelk:443",
            credentials=cred,
            credentials_file=None,
            scopes=None,
            ssl_credentials=mock_ssl_channel_creds,
            quota_project_id=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )

    # Check if ssl_channel_credentials is not provided, then client_cert_source_for_mtls
    # is used.
    with mock.patch.object(transport_class, "create_channel", return_value=mock.Mock()):
        with mock.patch("grpc.ssl_channel_credentials") as mock_ssl_cred:
            transport_class(
                credentials=cred,
                client_cert_source_for_mtls=client_cert_source_callback,
            )
            expected_cert, expected_key = client_cert_source_callback()
            mock_ssl_cred.assert_called_once_with(
                certificate_chain=expected_cert, private_key=expected_key
            )


def test_rule_service_http_transport_client_cert_source_for_mtls():
    cred = ga_credentials.AnonymousCredentials()
    with mock.patch(
        "google.auth.transport.requests.AuthorizedSession.configure_mtls_channel"
    ) as mock_configure_mtls_channel:
        transports.RuleServiceRestTransport(
            credentials=cred, client_cert_source_for_mtls=client_cert_source_callback
        )
        mock_configure_mtls_channel.assert_called_once_with(client_cert_source_callback)


@pytest.mark.parametrize(
    "transport_name",
    [
        "grpc",
        "grpc_asyncio",
        "rest",
    ],
)
def test_rule_service_host_no_port(transport_name):
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="chronicle.googleapis.com"
        ),
        transport=transport_name,
    )
    assert client.transport._host == (
        "chronicle.googleapis.com:443"
        if transport_name in ["grpc", "grpc_asyncio"]
        else "https://chronicle.googleapis.com"
    )


@pytest.mark.parametrize(
    "transport_name",
    [
        "grpc",
        "grpc_asyncio",
        "rest",
    ],
)
def test_rule_service_host_with_port(transport_name):
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="chronicle.googleapis.com:8000"
        ),
        transport=transport_name,
    )
    assert client.transport._host == (
        "chronicle.googleapis.com:8000"
        if transport_name in ["grpc", "grpc_asyncio"]
        else "https://chronicle.googleapis.com:8000"
    )


@pytest.mark.parametrize(
    "transport_name",
    [
        "rest",
    ],
)
def test_rule_service_client_transport_session_collision(transport_name):
    creds1 = ga_credentials.AnonymousCredentials()
    creds2 = ga_credentials.AnonymousCredentials()
    client1 = RuleServiceClient(
        credentials=creds1,
        transport=transport_name,
    )
    client2 = RuleServiceClient(
        credentials=creds2,
        transport=transport_name,
    )
    session1 = client1.transport.create_rule._session
    session2 = client2.transport.create_rule._session
    assert session1 != session2
    session1 = client1.transport.get_rule._session
    session2 = client2.transport.get_rule._session
    assert session1 != session2
    session1 = client1.transport.list_rules._session
    session2 = client2.transport.list_rules._session
    assert session1 != session2
    session1 = client1.transport.update_rule._session
    session2 = client2.transport.update_rule._session
    assert session1 != session2
    session1 = client1.transport.delete_rule._session
    session2 = client2.transport.delete_rule._session
    assert session1 != session2
    session1 = client1.transport.list_rule_revisions._session
    session2 = client2.transport.list_rule_revisions._session
    assert session1 != session2
    session1 = client1.transport.create_retrohunt._session
    session2 = client2.transport.create_retrohunt._session
    assert session1 != session2
    session1 = client1.transport.get_retrohunt._session
    session2 = client2.transport.get_retrohunt._session
    assert session1 != session2
    session1 = client1.transport.list_retrohunts._session
    session2 = client2.transport.list_retrohunts._session
    assert session1 != session2
    session1 = client1.transport.get_rule_deployment._session
    session2 = client2.transport.get_rule_deployment._session
    assert session1 != session2
    session1 = client1.transport.list_rule_deployments._session
    session2 = client2.transport.list_rule_deployments._session
    assert session1 != session2
    session1 = client1.transport.update_rule_deployment._session
    session2 = client2.transport.update_rule_deployment._session
    assert session1 != session2


def test_rule_service_grpc_transport_channel():
    channel = grpc.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.RuleServiceGrpcTransport(
        host="squid.clam.whelk",
        channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


def test_rule_service_grpc_asyncio_transport_channel():
    channel = aio.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.RuleServiceGrpcAsyncIOTransport(
        host="squid.clam.whelk",
        channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


# Remove this test when deprecated arguments (api_mtls_endpoint, client_cert_source) are
# removed from grpc/grpc_asyncio transport constructor.
@pytest.mark.parametrize(
    "transport_class",
    [transports.RuleServiceGrpcTransport, transports.RuleServiceGrpcAsyncIOTransport],
)
def test_rule_service_transport_channel_mtls_with_client_cert_source(transport_class):
    with mock.patch(
        "grpc.ssl_channel_credentials", autospec=True
    ) as grpc_ssl_channel_cred:
        with mock.patch.object(
            transport_class, "create_channel"
        ) as grpc_create_channel:
            mock_ssl_cred = mock.Mock()
            grpc_ssl_channel_cred.return_value = mock_ssl_cred

            mock_grpc_channel = mock.Mock()
            grpc_create_channel.return_value = mock_grpc_channel

            cred = ga_credentials.AnonymousCredentials()
            with pytest.warns(DeprecationWarning):
                with mock.patch.object(google.auth, "default") as adc:
                    adc.return_value = (cred, None)
                    transport = transport_class(
                        host="squid.clam.whelk",
                        api_mtls_endpoint="mtls.squid.clam.whelk",
                        client_cert_source=client_cert_source_callback,
                    )
                    adc.assert_called_once()

            grpc_ssl_channel_cred.assert_called_once_with(
                certificate_chain=b"cert bytes", private_key=b"key bytes"
            )
            grpc_create_channel.assert_called_once_with(
                "mtls.squid.clam.whelk:443",
                credentials=cred,
                credentials_file=None,
                scopes=None,
                ssl_credentials=mock_ssl_cred,
                quota_project_id=None,
                options=[
                    ("grpc.max_send_message_length", -1),
                    ("grpc.max_receive_message_length", -1),
                ],
            )
            assert transport.grpc_channel == mock_grpc_channel
            assert transport._ssl_channel_credentials == mock_ssl_cred


# Remove this test when deprecated arguments (api_mtls_endpoint, client_cert_source) are
# removed from grpc/grpc_asyncio transport constructor.
@pytest.mark.parametrize(
    "transport_class",
    [transports.RuleServiceGrpcTransport, transports.RuleServiceGrpcAsyncIOTransport],
)
def test_rule_service_transport_channel_mtls_with_adc(transport_class):
    mock_ssl_cred = mock.Mock()
    with mock.patch.multiple(
        "google.auth.transport.grpc.SslCredentials",
        __init__=mock.Mock(return_value=None),
        ssl_credentials=mock.PropertyMock(return_value=mock_ssl_cred),
    ):
        with mock.patch.object(
            transport_class, "create_channel"
        ) as grpc_create_channel:
            mock_grpc_channel = mock.Mock()
            grpc_create_channel.return_value = mock_grpc_channel
            mock_cred = mock.Mock()

            with pytest.warns(DeprecationWarning):
                transport = transport_class(
                    host="squid.clam.whelk",
                    credentials=mock_cred,
                    api_mtls_endpoint="mtls.squid.clam.whelk",
                    client_cert_source=None,
                )

            grpc_create_channel.assert_called_once_with(
                "mtls.squid.clam.whelk:443",
                credentials=mock_cred,
                credentials_file=None,
                scopes=None,
                ssl_credentials=mock_ssl_cred,
                quota_project_id=None,
                options=[
                    ("grpc.max_send_message_length", -1),
                    ("grpc.max_receive_message_length", -1),
                ],
            )
            assert transport.grpc_channel == mock_grpc_channel


def test_rule_service_grpc_lro_client():
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )
    transport = client.transport

    # Ensure that we have a api-core operations client.
    assert isinstance(
        transport.operations_client,
        operations_v1.OperationsClient,
    )

    # Ensure that subsequent calls to the property send the exact same object.
    assert transport.operations_client is transport.operations_client


def test_rule_service_grpc_lro_async_client():
    client = RuleServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )
    transport = client.transport

    # Ensure that we have a api-core operations client.
    assert isinstance(
        transport.operations_client,
        operations_v1.OperationsAsyncClient,
    )

    # Ensure that subsequent calls to the property send the exact same object.
    assert transport.operations_client is transport.operations_client


def test_data_access_scope_path():
    project = "squid"
    location = "clam"
    instance = "whelk"
    data_access_scope = "octopus"
    expected = "projects/{project}/locations/{location}/instances/{instance}/dataAccessScopes/{data_access_scope}".format(
        project=project,
        location=location,
        instance=instance,
        data_access_scope=data_access_scope,
    )
    actual = RuleServiceClient.data_access_scope_path(
        project, location, instance, data_access_scope
    )
    assert expected == actual


def test_parse_data_access_scope_path():
    expected = {
        "project": "oyster",
        "location": "nudibranch",
        "instance": "cuttlefish",
        "data_access_scope": "mussel",
    }
    path = RuleServiceClient.data_access_scope_path(**expected)

    # Check that the path construction is reversible.
    actual = RuleServiceClient.parse_data_access_scope_path(path)
    assert expected == actual


def test_reference_list_path():
    project = "winkle"
    location = "nautilus"
    instance = "scallop"
    reference_list = "abalone"
    expected = "projects/{project}/locations/{location}/instances/{instance}/referenceLists/{reference_list}".format(
        project=project,
        location=location,
        instance=instance,
        reference_list=reference_list,
    )
    actual = RuleServiceClient.reference_list_path(
        project, location, instance, reference_list
    )
    assert expected == actual


def test_parse_reference_list_path():
    expected = {
        "project": "squid",
        "location": "clam",
        "instance": "whelk",
        "reference_list": "octopus",
    }
    path = RuleServiceClient.reference_list_path(**expected)

    # Check that the path construction is reversible.
    actual = RuleServiceClient.parse_reference_list_path(path)
    assert expected == actual


def test_retrohunt_path():
    project = "oyster"
    location = "nudibranch"
    instance = "cuttlefish"
    rule = "mussel"
    retrohunt = "winkle"
    expected = "projects/{project}/locations/{location}/instances/{instance}/rules/{rule}/retrohunts/{retrohunt}".format(
        project=project,
        location=location,
        instance=instance,
        rule=rule,
        retrohunt=retrohunt,
    )
    actual = RuleServiceClient.retrohunt_path(
        project, location, instance, rule, retrohunt
    )
    assert expected == actual


def test_parse_retrohunt_path():
    expected = {
        "project": "nautilus",
        "location": "scallop",
        "instance": "abalone",
        "rule": "squid",
        "retrohunt": "clam",
    }
    path = RuleServiceClient.retrohunt_path(**expected)

    # Check that the path construction is reversible.
    actual = RuleServiceClient.parse_retrohunt_path(path)
    assert expected == actual


def test_rule_path():
    project = "whelk"
    location = "octopus"
    instance = "oyster"
    rule = "nudibranch"
    expected = "projects/{project}/locations/{location}/instances/{instance}/rules/{rule}".format(
        project=project,
        location=location,
        instance=instance,
        rule=rule,
    )
    actual = RuleServiceClient.rule_path(project, location, instance, rule)
    assert expected == actual


def test_parse_rule_path():
    expected = {
        "project": "cuttlefish",
        "location": "mussel",
        "instance": "winkle",
        "rule": "nautilus",
    }
    path = RuleServiceClient.rule_path(**expected)

    # Check that the path construction is reversible.
    actual = RuleServiceClient.parse_rule_path(path)
    assert expected == actual


def test_rule_deployment_path():
    project = "scallop"
    location = "abalone"
    instance = "squid"
    rule = "clam"
    expected = "projects/{project}/locations/{location}/instances/{instance}/rules/{rule}/deployment".format(
        project=project,
        location=location,
        instance=instance,
        rule=rule,
    )
    actual = RuleServiceClient.rule_deployment_path(project, location, instance, rule)
    assert expected == actual


def test_parse_rule_deployment_path():
    expected = {
        "project": "whelk",
        "location": "octopus",
        "instance": "oyster",
        "rule": "nudibranch",
    }
    path = RuleServiceClient.rule_deployment_path(**expected)

    # Check that the path construction is reversible.
    actual = RuleServiceClient.parse_rule_deployment_path(path)
    assert expected == actual


def test_common_billing_account_path():
    billing_account = "cuttlefish"
    expected = "billingAccounts/{billing_account}".format(
        billing_account=billing_account,
    )
    actual = RuleServiceClient.common_billing_account_path(billing_account)
    assert expected == actual


def test_parse_common_billing_account_path():
    expected = {
        "billing_account": "mussel",
    }
    path = RuleServiceClient.common_billing_account_path(**expected)

    # Check that the path construction is reversible.
    actual = RuleServiceClient.parse_common_billing_account_path(path)
    assert expected == actual


def test_common_folder_path():
    folder = "winkle"
    expected = "folders/{folder}".format(
        folder=folder,
    )
    actual = RuleServiceClient.common_folder_path(folder)
    assert expected == actual


def test_parse_common_folder_path():
    expected = {
        "folder": "nautilus",
    }
    path = RuleServiceClient.common_folder_path(**expected)

    # Check that the path construction is reversible.
    actual = RuleServiceClient.parse_common_folder_path(path)
    assert expected == actual


def test_common_organization_path():
    organization = "scallop"
    expected = "organizations/{organization}".format(
        organization=organization,
    )
    actual = RuleServiceClient.common_organization_path(organization)
    assert expected == actual


def test_parse_common_organization_path():
    expected = {
        "organization": "abalone",
    }
    path = RuleServiceClient.common_organization_path(**expected)

    # Check that the path construction is reversible.
    actual = RuleServiceClient.parse_common_organization_path(path)
    assert expected == actual


def test_common_project_path():
    project = "squid"
    expected = "projects/{project}".format(
        project=project,
    )
    actual = RuleServiceClient.common_project_path(project)
    assert expected == actual


def test_parse_common_project_path():
    expected = {
        "project": "clam",
    }
    path = RuleServiceClient.common_project_path(**expected)

    # Check that the path construction is reversible.
    actual = RuleServiceClient.parse_common_project_path(path)
    assert expected == actual


def test_common_location_path():
    project = "whelk"
    location = "octopus"
    expected = "projects/{project}/locations/{location}".format(
        project=project,
        location=location,
    )
    actual = RuleServiceClient.common_location_path(project, location)
    assert expected == actual


def test_parse_common_location_path():
    expected = {
        "project": "oyster",
        "location": "nudibranch",
    }
    path = RuleServiceClient.common_location_path(**expected)

    # Check that the path construction is reversible.
    actual = RuleServiceClient.parse_common_location_path(path)
    assert expected == actual


def test_client_with_default_client_info():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(
        transports.RuleServiceTransport, "_prep_wrapped_messages"
    ) as prep:
        client = RuleServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(
        transports.RuleServiceTransport, "_prep_wrapped_messages"
    ) as prep:
        transport_class = RuleServiceClient.get_transport_class()
        transport = transport_class(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)


def test_delete_operation(transport: str = "grpc"):
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = operations_pb2.DeleteOperationRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.delete_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_operation_async(transport: str = "grpc_asyncio"):
    client = RuleServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = operations_pb2.DeleteOperationRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.delete_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_operation_field_headers():
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = operations_pb2.DeleteOperationRequest()
    request.name = "locations"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_operation), "__call__") as call:
        call.return_value = None

        client.delete_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=locations",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_delete_operation_field_headers_async():
    client = RuleServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = operations_pb2.DeleteOperationRequest()
    request.name = "locations"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_operation), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.delete_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=locations",
    ) in kw["metadata"]


def test_delete_operation_from_dict():
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        response = client.delete_operation(
            request={
                "name": "locations",
            }
        )
        call.assert_called()


@pytest.mark.asyncio
async def test_delete_operation_from_dict_async():
    client = RuleServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.delete_operation(
            request={
                "name": "locations",
            }
        )
        call.assert_called()


def test_cancel_operation(transport: str = "grpc"):
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = operations_pb2.CancelOperationRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.cancel_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.cancel_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_cancel_operation_async(transport: str = "grpc_asyncio"):
    client = RuleServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = operations_pb2.CancelOperationRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.cancel_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.cancel_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None


def test_cancel_operation_field_headers():
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = operations_pb2.CancelOperationRequest()
    request.name = "locations"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.cancel_operation), "__call__") as call:
        call.return_value = None

        client.cancel_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=locations",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_cancel_operation_field_headers_async():
    client = RuleServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = operations_pb2.CancelOperationRequest()
    request.name = "locations"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.cancel_operation), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.cancel_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=locations",
    ) in kw["metadata"]


def test_cancel_operation_from_dict():
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.cancel_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        response = client.cancel_operation(
            request={
                "name": "locations",
            }
        )
        call.assert_called()


@pytest.mark.asyncio
async def test_cancel_operation_from_dict_async():
    client = RuleServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.cancel_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.cancel_operation(
            request={
                "name": "locations",
            }
        )
        call.assert_called()


def test_get_operation(transport: str = "grpc"):
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = operations_pb2.GetOperationRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation()
        response = client.get_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, operations_pb2.Operation)


@pytest.mark.asyncio
async def test_get_operation_async(transport: str = "grpc_asyncio"):
    client = RuleServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = operations_pb2.GetOperationRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation()
        )
        response = await client.get_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, operations_pb2.Operation)


def test_get_operation_field_headers():
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = operations_pb2.GetOperationRequest()
    request.name = "locations"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_operation), "__call__") as call:
        call.return_value = operations_pb2.Operation()

        client.get_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=locations",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_operation_field_headers_async():
    client = RuleServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = operations_pb2.GetOperationRequest()
    request.name = "locations"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_operation), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation()
        )
        await client.get_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=locations",
    ) in kw["metadata"]


def test_get_operation_from_dict():
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation()

        response = client.get_operation(
            request={
                "name": "locations",
            }
        )
        call.assert_called()


@pytest.mark.asyncio
async def test_get_operation_from_dict_async():
    client = RuleServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation()
        )
        response = await client.get_operation(
            request={
                "name": "locations",
            }
        )
        call.assert_called()


def test_list_operations(transport: str = "grpc"):
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = operations_pb2.ListOperationsRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_operations), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.ListOperationsResponse()
        response = client.list_operations(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, operations_pb2.ListOperationsResponse)


@pytest.mark.asyncio
async def test_list_operations_async(transport: str = "grpc_asyncio"):
    client = RuleServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = operations_pb2.ListOperationsRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_operations), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.ListOperationsResponse()
        )
        response = await client.list_operations(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, operations_pb2.ListOperationsResponse)


def test_list_operations_field_headers():
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = operations_pb2.ListOperationsRequest()
    request.name = "locations"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_operations), "__call__") as call:
        call.return_value = operations_pb2.ListOperationsResponse()

        client.list_operations(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=locations",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_operations_field_headers_async():
    client = RuleServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = operations_pb2.ListOperationsRequest()
    request.name = "locations"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_operations), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.ListOperationsResponse()
        )
        await client.list_operations(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=locations",
    ) in kw["metadata"]


def test_list_operations_from_dict():
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_operations), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.ListOperationsResponse()

        response = client.list_operations(
            request={
                "name": "locations",
            }
        )
        call.assert_called()


@pytest.mark.asyncio
async def test_list_operations_from_dict_async():
    client = RuleServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_operations), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.ListOperationsResponse()
        )
        response = await client.list_operations(
            request={
                "name": "locations",
            }
        )
        call.assert_called()


def test_transport_close_grpc():
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc"
    )
    with mock.patch.object(
        type(getattr(client.transport, "_grpc_channel")), "close"
    ) as close:
        with client:
            close.assert_not_called()
        close.assert_called_once()


@pytest.mark.asyncio
async def test_transport_close_grpc_asyncio():
    client = RuleServiceAsyncClient(
        credentials=async_anonymous_credentials(), transport="grpc_asyncio"
    )
    with mock.patch.object(
        type(getattr(client.transport, "_grpc_channel")), "close"
    ) as close:
        async with client:
            close.assert_not_called()
        close.assert_called_once()


def test_transport_close_rest():
    client = RuleServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    with mock.patch.object(
        type(getattr(client.transport, "_session")), "close"
    ) as close:
        with client:
            close.assert_not_called()
        close.assert_called_once()


def test_client_ctx():
    transports = [
        "rest",
        "grpc",
    ]
    for transport in transports:
        client = RuleServiceClient(
            credentials=ga_credentials.AnonymousCredentials(), transport=transport
        )
        # Test client calls underlying transport.
        with mock.patch.object(type(client.transport), "close") as close:
            close.assert_not_called()
            with client:
                pass
            close.assert_called()


@pytest.mark.parametrize(
    "client_class,transport_class",
    [
        (RuleServiceClient, transports.RuleServiceGrpcTransport),
        (RuleServiceAsyncClient, transports.RuleServiceGrpcAsyncIOTransport),
    ],
)
def test_api_key_credentials(client_class, transport_class):
    with mock.patch.object(
        google.auth._default, "get_api_key_credentials", create=True
    ) as get_api_key_credentials:
        mock_cred = mock.Mock()
        get_api_key_credentials.return_value = mock_cred
        options = client_options.ClientOptions()
        options.api_key = "api_key"
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class(client_options=options)
            patched.assert_called_once_with(
                credentials=mock_cred,
                credentials_file=None,
                host=client._DEFAULT_ENDPOINT_TEMPLATE.format(
                    UNIVERSE_DOMAIN=client._DEFAULT_UNIVERSE
                ),
                scopes=None,
                client_cert_source_for_mtls=None,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
                always_use_jwt_access=True,
                api_audience=None,
            )
