from fastapi import APIRouter, Depends, HTTPException, UploadFile
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.db.schema.asset import HybridSearchRequest
from app.utils.protectRoute import get_current_user
from app.utils.fileValidator import validate_file
from app.service.assetService import AssetService

assetRouter = APIRouter()

@assetRouter.post("/upload", status_code=201)
async def upload_asset(file: UploadFile, session: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    try: 
        file = await validate_file(file=file)
        asset = AssetService(session=session).upload_user_asset(user_id=current_user.id, file=file)

        return {
            "message": "Upload successful",
            "id": asset.id,
            "file_key": asset.file_key,
            "status": asset.status
        }
    except HTTPException as he:
        raise he
    
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
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Get asset endpoint failed: {str(e)}"
        )

@assetRouter.get("/{asset_id}/status")
def get_asset_status(asset_id: int, session: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    try:
        asset = AssetService(session=session).get_asset_status(user_id=current_user.id, asset_id=asset_id)
        return asset
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Get asset status endpoint failed: {str(e)}"
        )

@assetRouter.delete("/delete/{asset_id}")
def delete_user_asset(asset_id: int, session: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    try:
        asset = AssetService(session=session).delete_asset(user_id=current_user.id, asset_id=asset_id)
        return {"message": "Asset deleted successfully"}
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Delete asset endpoint failed: {str(e)}"
        )
    
@assetRouter.post("/search")
def search_assets(query: str, session: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    try: 
        result = AssetService(session=session).search_asset(user_id=current_user.id, query=query)
        return result
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Search asset endpoint failed: {str(e)}"
        )

@assetRouter.post("/search/hybrid")
def hybrid_search_assets(
    search_request: HybridSearchRequest,
    session: Session = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    try:
        result = AssetService(session=session).hybrid_search_assets(
            user_id=current_user.id,
            search_request=search_request,
        )
        return result
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Hybrid search endpoint failed: {str(e)}"
        )

@assetRouter.get("/filters")
def get_asset_filters(session: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    try:
        result = AssetService(session=session).get_asset_filters(user_id=current_user.id)
        return result
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Asset filters endpoint failed: {str(e)}"
        )

@assetRouter.get("/intelligence/{asset_id}")
def get_asset_intelligence(asset_id: int, session: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    try:
        result = AssetService(session=session).get_asset_intelligence(
            user_id=current_user.id,
            asset_id=asset_id,
        )
        return result
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Asset intelligence endpoint failed: {str(e)}"
        )

@assetRouter.patch("/reprocess/{asset_id}")
def reprocess_asset(asset_id: int, session: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    try:
        result = AssetService(session=session).reprocess_asset(
            user_id=current_user.id,
            asset_id=asset_id,
        )
        return result
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Asset reprocess endpoint failed: {str(e)}"
        )
