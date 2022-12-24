from contextlib import contextmanager

from flask import Flask
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor


class NotSetSpan:
    def is_recording(self) -> bool:
        return False


class NotSetTracer:
    @contextmanager
    def start_as_current_span(self, name: str):
        print("Tracing is disabled.")
        yield NotSetSpan()


def enable_open_telemetry(app: Flask, endpoint) -> None:
    resource = Resource(attributes={SERVICE_NAME: "machine-learning-api"})
    provider = TracerProvider(resource=resource)
    processor = BatchSpanProcessor(OTLPSpanExporter(endpoint=endpoint))
    provider.add_span_processor(processor)
    trace.set_tracer_provider(provider)

    tracer = trace.get_tracer(__name__)
    FlaskInstrumentor().instrument_app(app)

    return tracer
