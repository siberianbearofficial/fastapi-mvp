from src.core.settings import Settings


class MetricsSettings(Settings):
    excluded_handlers: list[str]
    latency_lowr_buckets: list[float]
