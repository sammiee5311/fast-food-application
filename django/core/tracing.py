from contextlib import contextmanager

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.trace import Tracer


class NotSetSpan:
    def is_recording(self) -> bool:
        return False


class NotSetTracer:
    @contextmanager
    def start_as_current_span(self, name: str | None, context: dict[str, str] | None):
        print("Tracing is disabled.")
        yield NotSetSpan()


tracer: Tracer | NotSetTracer = NotSetTracer()


def enable_open_telemetry(endpoint: str) -> None:
    global tracer

    resource = Resource(attributes={SERVICE_NAME: "django-api"})
    provider = TracerProvider(resource=resource)
    processor = BatchSpanProcessor(OTLPSpanExporter(endpoint=endpoint))
    provider.add_span_processor(processor)
    trace.set_tracer_provider(provider)

    tracer = trace.get_tracer(__name__)
