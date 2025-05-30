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

from google.apps.script.type.types import extension_point

__protobuf__ = proto.module(
    package="google.apps.script.type.sheets",
    manifest={
        "SheetsAddOnManifest",
        "SheetsExtensionPoint",
    },
)


class SheetsAddOnManifest(proto.Message):
    r"""Sheets add-on manifest.

    Attributes:
        homepage_trigger (google.apps.script.type.types.HomepageExtensionPoint):
            If present, this overrides the configuration from
            ``addOns.common.homepageTrigger``.
        on_file_scope_granted_trigger (google.apps.script.type.sheets.types.SheetsExtensionPoint):
            Endpoint to execute when file scope
            authorization is granted for this document/user
            pair.
    """

    homepage_trigger: extension_point.HomepageExtensionPoint = proto.Field(
        proto.MESSAGE,
        number=3,
        message=extension_point.HomepageExtensionPoint,
    )
    on_file_scope_granted_trigger: "SheetsExtensionPoint" = proto.Field(
        proto.MESSAGE,
        number=5,
        message="SheetsExtensionPoint",
    )


class SheetsExtensionPoint(proto.Message):
    r"""Common format for declaring a Sheets add-on's triggers.

    Attributes:
        run_function (str):
            Required. The endpoint to execute when this
            extension point is activated.
    """

    run_function: str = proto.Field(
        proto.STRING,
        number=1,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
