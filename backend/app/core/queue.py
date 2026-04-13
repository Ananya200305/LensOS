from decouple import config
from redis import Redis
from rq import Queue, Retry

REDIS_URL = config("REDIS_URL", default="redis://localhost:6379/0")
RQ_QUEUE_NAME = config("RQ_QUEUE_NAME", default="asset-processing")
RQ_RETRY_MAX = config("RQ_RETRY_MAX", cast=int, default=3)
RQ_RETRY_INTERVAL = config("RQ_RETRY_INTERVAL", cast=int, default=30)
RQ_JOB_TIMEOUT = config("RQ_JOB_TIMEOUT", cast=int, default=900)

redis_connection = Redis.from_url(REDIS_URL)
asset_queue = Queue(
    name=RQ_QUEUE_NAME,
    connection=redis_connection,
    default_timeout=RQ_JOB_TIMEOUT,
)


def enqueue_asset_processing(asset_id: int, user_id: int, file_key: str):
    return asset_queue.enqueue(
        "worker_task.process_asset_job",
        asset_id=asset_id,
        user_id=user_id,
        file_key=file_key,
        retry=Retry(max=RQ_RETRY_MAX, interval=[RQ_RETRY_INTERVAL] * RQ_RETRY_MAX),
        job_timeout=RQ_JOB_TIMEOUT,
    )
