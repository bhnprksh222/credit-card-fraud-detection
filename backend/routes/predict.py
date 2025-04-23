import joblib
import numpy as np
import pandas as pd
from fastapi import APIRouter, HTTPException, status
from logger import logger
from models.transaction import Transaction

router = APIRouter()


@router.get("/predict-fraud")
async def predict_fraud():
    try:
        model = joblib.load("fraud_model.pkl")

        data = await Transaction.all().values()
        df = pd.DataFrame(data)

        if df.empty:
            return {"fraudulent": [], "all": []}

        df["distance"] = np.sqrt(
            (df["merch_lat"] - df["lat"]) ** 2 + (df["merch_long"] - df["long"]) ** 2
        )
        df["hour"] = pd.to_datetime(df["trans_date_trans_time"]).dt.hour
        df["day_of_week"] = pd.to_datetime(df["trans_date_trans_time"]).dt.dayofweek
        df["month"] = pd.to_datetime(df["trans_date_trans_time"]).dt.month
        drop_cols = [
            "id",
            "trans_date_trans_time",
            "first",
            "last",
            "street",
            "city",
            "state",
            "zip",
            "dob",
            "trans_num",
            "unix_time",
            "cc_num",
            "created_at",
        ]
        X = df.drop(
            columns=[col for col in drop_cols if col in df.columns], errors="ignore"
        )

        df["predicted_fraud"] = model.predict(X)

        fraud = df[df["predicted_fraud"] == 1].to_dict(orient="records")
        all_data = df.to_dict(orient="records")

        logger.info({"fraudulent": fraud})
        return {"fraudulent": fraud, "all": all_data}

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
