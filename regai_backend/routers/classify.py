from fastapi import APIRouter, HTTPException
from models.schemas import DeviceClassificationRequest, DeviceClassificationResponse
from services.classification_service import ClassificationService

router = APIRouter()
classifier = ClassificationService()

@router.post("/classify", response_model=DeviceClassificationResponse)
async def classify_device(request: DeviceClassificationRequest):
    """
    Classifies a medical device based on its name and intended use.
    """
    try:
        result = classifier.classify_device(request.device_name, request.intended_use)
        return result
    except Exception as e:
        # LOG HERE in production
        raise HTTPException(status_code=500, detail=f"Classification failed: {str(e)}")

@router.get("/health")
async def health_check():
    return {"status": "healthy", "version": "1.0.0"}
