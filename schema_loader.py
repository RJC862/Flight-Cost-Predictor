import pandas as pd

print("Libraries loaded successfully.")

SCHEMA = {
    "observed_date": "datetime64[us]",
    "departure_date": "datetime64[us]",
    "route": "string",
    "price": "float64",
    "airline":"category",
    "stops": "int8",
    "duration_min": "float32",
    "dest": "category",
    "itinerary_id": "string",
    "days_before_departure": "int16",
}

COLUMN_MAP = {
    "search_date": "observed_date",
    "destination": "dest",
    "departure_time": "departure_time",
    "duration_minutes": "duration_min",
    "price_usd": "price"
}

# Loads a dataframe with only the necessary columns
def load_flights(path: str) -> pd.DataFrame:
    df = pd.read_parquet(path)
    df = df.rename(columns=COLUMN_MAP)

    df["departure_date"] = pd.to_datetime(df["departure_date"])
    df["observed_date"] = pd.to_datetime(df["observed_date"])

    df = df[list(SCHEMA)].astype(SCHEMA)

    return df

# validates a dataframe's columns
def validate(df: pd.DataFrame) -> dict:
    computed_days = (df["departure_date"] - df["observed_date"]).dt.days
    return {
        "rows": len(df),
        "null_count": df.isna().sum().to_dict(),
        "duplicates": int(df.duplicated().sum()),
        "price_min_max": (df["price"].min(), df["price"].max()),
        "nonpositive_prices": int((df["price"] <= 0).sum()),
        "observed_after_departure": int((df["observed_date"]> df["departure_date"]).sum()),
        "days_mismatch": int((computed_days != df["days_before_departure"]).sum()),
    }