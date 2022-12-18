import { Resource } from "@opentelemetry/resources";
import { SemanticResourceAttributes } from "@opentelemetry/semantic-conventions";
import { SimpleSpanProcessor } from "@opentelemetry/sdk-trace-base";
import { NodeTracerProvider } from "@opentelemetry/sdk-trace-node";
import { trace } from "@opentelemetry/api";

import { JaegerExporter } from "@opentelemetry/exporter-jaeger";

import { ExpressInstrumentation } from "opentelemetry-instrumentation-express";
import { MongoDBInstrumentation } from "@opentelemetry/instrumentation-mongodb";
import { HttpInstrumentation } from "@opentelemetry/instrumentation-http";
import { registerInstrumentations } from "@opentelemetry/instrumentation";
import { diag, DiagConsoleLogger, DiagLogLevel } from "@opentelemetry/api";

const isTest = process.env.NODE_ENV === "test" ? true : false;

if (isTest) {
  diag.setLogger(new DiagConsoleLogger(), DiagLogLevel.DEBUG);
}

const tracing = (serviceName: string, jaeger_endpoint: string) => {
  const exporter = new JaegerExporter({
    endpoint: jaeger_endpoint,
  });
  const provider = new NodeTracerProvider({
    resource: new Resource({
      [SemanticResourceAttributes.SERVICE_NAME]: serviceName,
    }),
  });
  provider.addSpanProcessor(new SimpleSpanProcessor(exporter));
  provider.register();
  registerInstrumentations({
    instrumentations: [
      new HttpInstrumentation(),
      new ExpressInstrumentation(),
      new MongoDBInstrumentation(),
    ],
    tracerProvider: provider,
  });

  return trace.getTracer(serviceName);
};

export default tracing;
