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
from __future__ import annotations

from typing import MutableMapping, MutableSequence

import proto  # type: ignore

__protobuf__ = proto.module(
    package="google.cloud.security.publicca.v1beta1",
    manifest={
        "ExternalAccountKey",
    },
)


class ExternalAccountKey(proto.Message):
    r"""A representation of an ExternalAccountKey used for `external account
    binding <https://tools.ietf.org/html/rfc8555#section-7.3.4>`__
    within ACME.

    Attributes:
        name (str):
            Output only. Resource name.
            projects/{project}/locations/{location}/externalAccountKeys/{key_id}
        key_id (str):
            Output only. Key ID.
            It is generated by the
            PublicCertificateAuthorityService when the
            ExternalAccountKey is created
        b64_mac_key (bytes):
            Output only. Base64-URL-encoded HS256 key.
            It is generated by the
            PublicCertificateAuthorityService when the
            ExternalAccountKey is created
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    key_id: str = proto.Field(
        proto.STRING,
        number=2,
    )
    b64_mac_key: bytes = proto.Field(
        proto.BYTES,
        number=3,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
