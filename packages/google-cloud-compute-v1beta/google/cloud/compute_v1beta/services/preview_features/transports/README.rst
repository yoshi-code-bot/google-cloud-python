
transport inheritance structure
_______________________________

`PreviewFeaturesTransport` is the ABC for all transports.
- public child `PreviewFeaturesGrpcTransport` for sync gRPC transport (defined in `grpc.py`).
- public child `PreviewFeaturesGrpcAsyncIOTransport` for async gRPC transport (defined in `grpc_asyncio.py`).
- private child `_BasePreviewFeaturesRestTransport` for base REST transport with inner classes `_BaseMETHOD` (defined in `rest_base.py`).
- public child `PreviewFeaturesRestTransport` for sync REST transport with inner classes `METHOD` derived from the parent's corresponding `_BaseMETHOD` classes (defined in `rest.py`).
