import logging

from rq import Worker, get_current_job

from app.db.models.asset import Asset
from app.db.models.user import User

from app.core.database import SessionLocal
from app.core.queue import RQ_QUEUE_NAME, redis_connection
from app.service.assetProcessingService import AssetProcessingService

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def process_asset_job(asset_id: int, user_id: int, file_key: str):
    job = get_current_job()
    job_id = job.id if job else None
    logger.info("Starting asset job job_id=%s asset_id=%s user_id=%s", job_id, asset_id, user_id)
    session = SessionLocal()

    try:
        if job:
            job.meta["asset_id"] = asset_id
            job.meta["user_id"] = user_id
            job.meta["status"] = "processing"
            job.save_meta()

        report = AssetProcessingService(session=session).process_asset(
            asset_id=asset_id,
            user_id=user_id,
            file_key=file_key,
        )
        if job:
            job.meta["status"] = report.status
            job.meta["completed_stages"] = report.completed_stages
            job.meta["warnings"] = [warning.model_dump() for warning in report.warnings]
            job.save_meta()
        logger.info(
            "Completed asset job job_id=%s asset_id=%s status=%s stages=%s warnings=%s",
            job_id,
            asset_id,
            report.status,
            report.completed_stages,
            len(report.warnings),
        )
    except Exception as error:
        if job:
            job.meta["status"] = "failed"
            job.meta["error"] = str(error)
            job.save_meta()
        logger.exception("Asset job failed job_id=%s asset_id=%s user_id=%s", job_id, asset_id, user_id)
        raise
    finally:
        session.close()


if __name__ == "__main__":
    worker = Worker([RQ_QUEUE_NAME], connection=redis_connection)
    worker.work()
