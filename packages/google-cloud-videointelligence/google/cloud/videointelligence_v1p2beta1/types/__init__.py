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
from .video_intelligence import (
    AnnotateVideoProgress,
    AnnotateVideoRequest,
    AnnotateVideoResponse,
    Entity,
    ExplicitContentAnnotation,
    ExplicitContentDetectionConfig,
    ExplicitContentFrame,
    Feature,
    LabelAnnotation,
    LabelDetectionConfig,
    LabelDetectionMode,
    LabelFrame,
    LabelSegment,
    Likelihood,
    NormalizedBoundingBox,
    NormalizedBoundingPoly,
    NormalizedVertex,
    ObjectTrackingAnnotation,
    ObjectTrackingFrame,
    ShotChangeDetectionConfig,
    TextAnnotation,
    TextDetectionConfig,
    TextFrame,
    TextSegment,
    VideoAnnotationProgress,
    VideoAnnotationResults,
    VideoContext,
    VideoSegment,
)

__all__ = (
    "AnnotateVideoProgress",
    "AnnotateVideoRequest",
    "AnnotateVideoResponse",
    "Entity",
    "ExplicitContentAnnotation",
    "ExplicitContentDetectionConfig",
    "ExplicitContentFrame",
    "LabelAnnotation",
    "LabelDetectionConfig",
    "LabelFrame",
    "LabelSegment",
    "NormalizedBoundingBox",
    "NormalizedBoundingPoly",
    "NormalizedVertex",
    "ObjectTrackingAnnotation",
    "ObjectTrackingFrame",
    "ShotChangeDetectionConfig",
    "TextAnnotation",
    "TextDetectionConfig",
    "TextFrame",
    "TextSegment",
    "VideoAnnotationProgress",
    "VideoAnnotationResults",
    "VideoContext",
    "VideoSegment",
    "Feature",
    "LabelDetectionMode",
    "Likelihood",
)
