import asyncio

import joblib
import numpy as np
import pandas as pd
from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline as imbpipeline
from models.transaction import Transaction
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler


# -----------------------------------------------
# 1. Fetch data from PostgreSQL (async)
# -----------------------------------------------
async def fetch_transactions():
    records = await Transaction.all().values()
    df = pd.DataFrame(records)
    return df


# -----------------------------------------------
# 2. Preprocess & Feature Engineering
# -----------------------------------------------
def preprocess_data(df: pd.DataFrame):
    # Convert to datetime
    df["trans_date_trans_time"] = pd.to_datetime(
        df["trans_date_trans_time"], dayfirst=True
    )

    # Extract date features
    df["hour"] = df["trans_date_trans_time"].dt.hour
    df["day_of_week"] = df["trans_date_trans_time"].dt.dayofweek
    df["month"] = df["trans_date_trans_time"].dt.month

    # Compute distance from merchant location
    df["distance"] = np.sqrt(
        (df["merch_lat"] - df["lat"]) ** 2 + (df["merch_long"] - df["long"]) ** 2
    )

    # Drop non-useful columns
    drop_cols = [
        "trans_date_trans_time",
        "first",
        "last",
        "street",
        "city",
        "state",
        "zip",
        "job",
        "dob",
        "trans_num",
        "unix_time",
        "cc_num",
        "id",
        "created_at",
    ]
    df.drop([col for col in drop_cols if col in df.columns], axis=1, inplace=True)

    return df


# -----------------------------------------------
# 3. Build Model Pipeline
# -----------------------------------------------
def build_pipeline(num_features, cat_features):
    num_transformer = StandardScaler()
    cat_transformer = OneHotEncoder(handle_unknown="ignore")

    preprocessor = ColumnTransformer(
        [("num", num_transformer, num_features), ("cat", cat_transformer, cat_features)]
    )

    model = imbpipeline(
        steps=[
            ("preprocessing", preprocessor),
            ("smote", SMOTE(random_state=42)),
            ("classifier", RandomForestClassifier(n_estimators=100, random_state=42)),
        ]
    )
    return model


# -----------------------------------------------
# 4. Main Training Routine
# -----------------------------------------------
async def main():
    print("Loading data from database...")
    df = await fetch_transactions()

    if df.empty:
        print("No data found in 'transactions' table.")
        return

    print(f"Loaded {len(df)} records.")

    df = preprocess_data(df)

    X = df.drop("is_fraud", axis=1)
    y = df["is_fraud"]

    num_features = [
        "amt",
        "lat",
        "long",
        "city_pop",
        "merch_lat",
        "merch_long",
        "distance",
        "hour",
        "day_of_week",
        "month",
    ]
    cat_features = ["category", "gender", "merchant"]

    # Remove any features that were dropped earlier
    num_features = [f for f in num_features if f in X.columns]
    cat_features = [f for f in cat_features if f in X.columns]

    print("Building model pipeline...")
    model = build_pipeline(num_features, cat_features)

    print("Splitting data...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, stratify=y, random_state=42
    )

    print("Training model...")
    model.fit(X_train, y_train)

    print("Saving model to fraud_model.pkl")
    joblib.dump(model, "fraud_model.pkl")

    print("Training complete. Model saved.")


# Run the pipeline
if __name__ == "__main__":
    asyncio.run(main())
