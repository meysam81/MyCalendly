import logging
from collections import defaultdict

import uvicorn
from fastapi import APIRouter, FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware

from app import api, config
from app.common.metrics import Metrics

app = FastAPI(
    title=config.app_settings.NAME,
    description=config.app_settings.DESCRIPTION,
    servers=config.app_settings.SERVERS,
)

app_logger = logging.getLogger(config.app_settings.NAME)
app_logger.setLevel(config.global_settings.LOG_LEVEL)
logging.basicConfig(level=config.global_settings.LOG_LEVEL)


@app.on_event("startup")
async def startup():
    app_logger.info("App started.")


@app.on_event("shutdown")
async def shutdown():
    app_logger.info("App shutdown.")


# this is the index router and might not get a lot of endpoints
router = APIRouter()


@router.get("/")
def index():
    app_logger.info("A new request comes in, yaaay!")
    return "Hello from MyCalendly!"


# Set all CORS enabled origins
if config.api_settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            str(origin) for origin in config.api_settings.BACKEND_CORS_ORIGINS
        ],
        allow_credentials=True,
        allow_methods=config.api_settings.BACKEND_CORS_METHODS,
        allow_headers=config.api_settings.BACKEND_CORS_HEADERS,
    )
app.include_router(api.router, prefix=config.api_settings.API_STR)
app.include_router(router, tags=["Index"])


@app.middleware("http")
@Metrics.capture(logging.getLogger("LatencyMeasure"), with_duration=True)
async def calculate_latency(request: Request, call_next, metrics):
    return await call_next(request)


@app.middleware("http")
@Metrics.capture(logging.getLogger("Req&Resp"), with_duration=False)
async def log_request_and_response(request: Request, call_next, metrics):
    try:
        metrics.set(
            request={
                "method": request.method,
                "url": request.url,
                "headers": dict(request.headers),
                "source": request.client,
            },
        )
        response: Response = await call_next(request)
        metrics.set(
            response={
                "status": response.status_code,
                "headers": dict(response.headers),
            },
        )
        return response
    except Exception as exp:
        app_logger.error(
            f"Error occurred while handling a request: {exp}", exc_info=True
        )
        raise


def get_routes():
    routes = defaultdict(set)
    for r in app.routes:
        routes[r.path].update(r.methods)
    return "\n".join(sorted(map(str, routes.items())))


app_logger.info(f"App started with the following routes:\n{get_routes()}")


if __name__ == "__main__":
    is_dev = config.global_settings.ENV == config.Environment.DEV
    debug = is_dev
    uvicorn.run(
        "app.main:app",
        log_level=config.global_settings.LOG_LEVEL.lower(),
        port=config.app_settings.PORT,
        debug=debug,
        reload=is_dev,
        workers=config.global_settings.WORKERS,
    )
