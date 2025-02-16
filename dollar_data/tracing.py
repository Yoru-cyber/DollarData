from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.instrumentation.flask import FlaskInstrumentor

def configure_tracing(app):
    # Configure resource
    resource = Resource(attributes={
        "service.name": "your-flask-service",
        "service.version": "1.0.0"
    })

    # Set up tracer provider
    tracer_provider = TracerProvider(resource=resource)
    trace.set_tracer_provider(tracer_provider)

    # Configure OTLP exporter
    otlp_exporter = OTLPSpanExporter(endpoint="http://localhost:4317", insecure=True)
    span_processor = BatchSpanProcessor(otlp_exporter)
    tracer_provider.add_span_processor(span_processor)

    # Instrument Flask
    FlaskInstrumentor().instrument_app(app)