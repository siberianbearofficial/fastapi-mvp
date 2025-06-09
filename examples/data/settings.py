from fastapi_mvp.metrics import MetricsSettings
from fastapi_mvp.storage.mongo_storage import MongoSettings


def get_mongo_settings() -> MongoSettings:
    return MongoSettings(
        name="mongo",
        user="mongo",
        password="mongo",  # noqa
        host="localhost",
        port=27017,
    )


def get_metrics_settings() -> MetricsSettings:
    return MetricsSettings(
        excluded_handlers=[
            "/healthz",
            "/docs",
            "/metrics",
            "/readyz",
            "/openapi.json",
        ],
        latency_lowr_buckets=[
            0.1,
            0.25,
            0.5,
            0.75,
            1.0,
            1.5,
            2.0,
            2.5,
            5.0,
            7.5,
            10.0,
            20.0,
            30.0,
        ],
    )
