# LensOS Backend V2

FastAPI serves the API, Redis/RQ runs background jobs, PostgreSQL stores metadata, S3 stores original images, and Qdrant stores CLIP embeddings.

## Environment

Add these variables to `backend/.env`:

- `DB_USER`
- `DB_PASSWORD`
- `DB_HOST`
- `DB_PORT`
- `DB_NAME`
- `JWT_SECRET`
- `JWT_ALGORITHM`
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_REGION`
- `AWS_BUCKET_NAME`
- `HF_TOKEN`
- `VECTOR_DB_URL`
- `REDIS_URL=redis://localhost:6379/0`
- `RQ_QUEUE_NAME=asset-processing`
- `RQ_RETRY_MAX=3`
- `RQ_RETRY_INTERVAL=30`
- `RQ_JOB_TIMEOUT=900`

## Install

```bash
pip install -r requirements.txt
```

## Run API

```bash
uvicorn main:app --reload
```

## Run Worker

```bash
python worker_task.py
```

## Services Required

- PostgreSQL
- Redis
- Qdrant
- AWS S3 bucket
