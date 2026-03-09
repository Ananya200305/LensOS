from fastapi import UploadFile, HTTPException, status


ALLOWED_TYPES = ["image/jpeg", "image/png", "image/webp"]
ALLOWED_SIZE = 5 * 1024 * 1024  # 5 MB

async def validate_file(file: UploadFile) -> UploadFile:

    try:
        #filename check
        if not file.filename:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="File Must Have a name")
        
        #type check
        if file.content_type not in ALLOWED_TYPES:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid file type. Only JPEG, PNG, and WEBP are allowed.")
        
        #size check
        if file.size > ALLOWED_SIZE:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="File size exceeds the 5 MB limit.")
        
        return file
    except Exception as e:
        raise HTTPException(status_code=400, detail="File validation failed: " + str(e))
