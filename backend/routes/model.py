from pathlib import Path

from fastapi import APIRouter, HTTPException, status
from ml.train_model import main as train_main

router = APIRouter()


@router.post("/train-model")
async def train_model_route():
    try:
        await train_main()
        if not Path("fraud_model.pkl").exists():
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Model training failed.",
            )
        return {"message": "Model trained and saved successfully."}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Training failed: {str(e)}",
        )
