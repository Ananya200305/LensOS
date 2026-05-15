from sqlalchemy import text

from app.core.database import engine


def run_asset_v3_migration():
    statements = [
        """
        ALTER TABLE assets
        ADD COLUMN IF NOT EXISTS detected_objects JSONB
        """,
        """
        ALTER TABLE assets
        ADD COLUMN IF NOT EXISTS scene_label VARCHAR(100)
        """,
        """
        ALTER TABLE assets
        ADD COLUMN IF NOT EXISTS time_label VARCHAR(100)
        """,
        """
        ALTER TABLE assets
        ADD COLUMN IF NOT EXISTS environment_label VARCHAR(100)
        """,
        """
        ALTER TABLE assets
        ADD COLUMN IF NOT EXISTS processed_at TIMESTAMPTZ
        """,
        """
        ALTER TABLE assets
        ADD COLUMN IF NOT EXISTS ranking_score DOUBLE PRECISION DEFAULT 0
        """,
        """
        UPDATE assets
        SET detected_objects = '[]'::jsonb
        WHERE detected_objects IS NULL
        """,
        """
        UPDATE assets
        SET ranking_score = 0
        WHERE ranking_score IS NULL
        """,
        """
ALTER TABLE assets
ALTER COLUMN tags TYPE JSONB
""",
    ]

    with engine.begin() as connection:
        for statement in statements:
            connection.execute(text(statement))
