import os
from contextlib import contextmanager

from config.env import load_env
from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.trace import Tracer

load_env()

OTLP_ENDPOINT = os.environ.get("OTLP_ENDPOINT")


class NotSetSpan:
    def is_recording(self) -> bool:
        return False


class NotSetTracer:
    @contextmanager
    def start_as_current_span(self, name: str):
        print("Tracing is disabled.")
        yield NotSetSpan()


tracer: Tracer | NotSetTracer = NotSetTracer()


def enable_open_telemetry(endpoint: str) -> None:
    global tracer

    resource = Resource(attributes={SERVICE_NAME: "order-delivery-time-handler"})
    provider = TracerProvider(resource=resource)
    processor = BatchSpanProcessor(OTLPSpanExporter(endpoint=endpoint))
    provider.add_span_processor(processor)
    trace.set_tracer_provider(provider)

    tracer = trace.get_tracer(__name__)


if OTLP_ENDPOINT:
    enable_open_telemetry(OTLP_ENDPOINT)
