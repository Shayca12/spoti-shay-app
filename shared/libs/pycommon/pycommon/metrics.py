from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from fastapi import Request, Response

REQ_COUNT = Counter("http_requests_total", "HTTP requests", ["service", "method", "path", "status"])
REQ_LAT = Histogram("http_request_duration_seconds", "Request latency", ["service", "path"])

def metrics_response() -> Response:
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

async def metrics_middleware(request: Request, call_next, service_name: str):
    path = request.url.path
    with REQ_LAT.labels(service=service_name, path=path).time():
        resp = await call_next(request)
    REQ_COUNT.labels(service=service_name, method=request.method, path=path, status=str(resp.status_code)).inc()
    return resp
