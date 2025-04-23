from io import StringIO
from typing import Optional

import pandas as pd
from fastapi import APIRouter, File, HTTPException, Query, UploadFile, status
from logger import logger
from models.transaction import Transaction
from tortoise.transactions import in_transaction

router = APIRouter()


@router.post("/upload-csv")
async def upload_csv(file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="File must be a CSV format."
        )

    contents = await file.read()
    try:
        df = pd.read_csv(StringIO(contents.decode("utf-8")))
        df.columns = df.columns.str.strip().str.lower()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"CSV parsing failed: {str(e)}",
        )

    required_columns = {
        "trans_date_trans_time",
        "cc_num",
        "merchant",
        "category",
        "amt",
        "first",
        "last",
        "gender",
        "street",
        "city",
        "state",
        "zip",
        "lat",
        "long",
        "city_pop",
        "job",
        "dob",
        "trans_num",
        "unix_time",
        "merch_lat",
        "merch_long",
        "is_fraud",
    }

    if not required_columns.issubset(df.columns):
        missing = required_columns - set(df.columns)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Missing columns in CSV: {', '.join(missing)}",
        )

    # Remove duplicates based on unique transaction number
    existing_trans_nums = await Transaction.filter(
        trans_num__in=df["trans_num"].tolist()
    ).values_list("trans_num", flat=True)

    df = df[~df["trans_num"].isin(existing_trans_nums)]

    # Convert and prepare Transaction objects
    try:
        transactions = [
            Transaction(
                trans_date_trans_time=row["trans_date_trans_time"],
                cc_num=str(row["cc_num"]),
                merchant=row["merchant"],
                category=row["category"],
                amt=float(row["amt"]),
                first=row["first"],
                last=row["last"],
                gender=row["gender"],
                street=row["street"],
                city=row["city"],
                state=row["state"],
                zip=str(row["zip"]),
                lat=float(row["lat"]),
                long=float(row["long"]),
                city_pop=int(row["city_pop"]),
                job=row["job"],
                dob=row["dob"],
                trans_num=row["trans_num"],
                unix_time=int(row["unix_time"]),
                merch_lat=float(row["merch_lat"]),
                merch_long=float(row["merch_long"]),
                is_fraud=bool(row["is_fraud"]),
            )
            for _, row in df.iterrows()
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Data conversion error: {str(e)}")

    try:
        async with in_transaction():
            # Clear transactions in the transactions table
            await Transaction.all().delete()

            # Insert in bulk inside transaction
            await Transaction.bulk_create(transactions)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to insert records: {str(e)}",
        )

    logger.info(
        f"Cleared old records and Inserted {len(transactions)} new transactions."
    )

    return {
        "message": f"CSV uploaded successfully. Inserted {len(transactions)} records."
    }


@router.get("/transactions")
async def get_transactions(
    limit: int = Query(10, ge=1),
    offset: int = Query(0, ge=0),
    is_fraud: Optional[bool] = Query(None),
):
    query = Transaction.all()

    if is_fraud is not None:
        query = query.filter(is_fraud=is_fraud)

    transactions = await query.offset(offset).limit(limit)
    total = await query.count()

    return {
        "transactions": [
            {
                "id": t.id,
                "merchant": t.merchant,
                "amt": t.amt,
                "category": t.category,
                "city": t.city,
                "is_fraud": bool(t.is_fraud),
                "trans_date_trans_time": t.trans_date_trans_time,
            }
            for t in transactions
        ],
        "total": total,
    }
