#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

from core.settings import OTLP_ENDPOINT
from core.tracing import enable_open_telemetry
from opentelemetry.instrumentation.django import DjangoInstrumentor
from opentelemetry.instrumentation.psycopg2 import Psycopg2Instrumentor


def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

    if OTLP_ENDPOINT and not "test" in sys.argv:
        enable_open_telemetry(OTLP_ENDPOINT)
        DjangoInstrumentor().instrument()
        Psycopg2Instrumentor().instrument()

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
