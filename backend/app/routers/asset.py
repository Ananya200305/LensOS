from fastapi import APIRouter, Depends, HTTPException, UploadFile
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.utils.protectRoute import get_current_user
from app.utils.fileValidator import validate_file
from app.service.assetService import AssetService

assetRouter = APIRouter()

@assetRouter.post("/upload", status_code=201)
async def upload_asset(file: UploadFile, session: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    try: 

        #1. Validate file
        file = await validate_file(file=file)

        #2. call service 
        asset = AssetService(session=session).upload_user_asset(user_id=current_user.id, file=file)

        return {
            "message": "Upload successful",
            "id": asset.id,
            "file_key": asset.file_key,
            "status": asset.status
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Upload endpoint failed: {str(e)}"
        )
    
@assetRouter.get("")
def get_user_asset(session: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    try: 
        assets = AssetService(session=session).get_asset_for_user(user_id=current_user.id)
        return assets
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Get asset endpoint failed: {str(e)}"
        )