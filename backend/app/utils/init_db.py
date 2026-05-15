from app.core.database import Base, engine
from app.db.models.user import User
from app.db.models.asset import Asset
from app.utils.migrate_asset_v3 import run_asset_v3_migration

def create_tables():
    Base.metadata.create_all(bind=engine)
    run_asset_v3_migration()
