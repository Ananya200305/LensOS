import logging

from rq import Worker

from app.db.models.asset import Asset
from app.db.models.user import User

from app.core.database import SessionLocal
from app.core.queue import RQ_QUEUE_NAME, redis_connection
from app.service.assetProcessingService import AssetProcessingService

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def process_asset_job(asset_id: int, user_id: int, file_key: str):
    logger.info("Starting asset job asset_id=%s user_id=%s", asset_id, user_id)
    session = SessionLocal()

    try:
        AssetProcessingService(session=session).process_asset(
            asset_id=asset_id,
            user_id=user_id,
            file_key=file_key,
        )
        logger.info("Completed asset job asset_id=%s", asset_id)
    except Exception:
        logger.exception("Asset job failed asset_id=%s user_id=%s", asset_id, user_id)
        raise
    finally:
        session.close()


if __name__ == "__main__":
    worker = Worker([RQ_QUEUE_NAME], connection=redis_connection)
    worker.work()
