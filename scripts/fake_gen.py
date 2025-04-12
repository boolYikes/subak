import pandas as pd
import numpy as np
from faker import Faker
from pathlib import Path

fake = Faker()
# this is lateral
Path("parquet_data").mkdir(exist_ok=True)

def create_users(n=100_000):
    return pd.DataFrame({
        "user_id": np.arange(n),
        "name": [fake.name() for _ in range(n)],
        "email": [fake.email() for _ in range(n)],
        "created": pd.date_range("2018-01-01", periods=n, freq="min"),
        "region": np.random.choice(["NA", "EU", "ASIA", "LATAM"], n)
    })

def create_transactions(n=1_000_000, user_count=100_000):
    return pd.DataFrame({
        "transaction_id": np.arange(n),
        "user_id":np.random.randint(0, user_count, n),
        "amount": np.random.lognormal(mean=3, sigma=1, size=n).round(2),
        "timestamp": pd.date_range("2019-01-01", periods=n, freq="s"),
        "product_category": np.random.choice(["books", "electronics", "fashion", "home"], n)
    })

df_users = create_users()
df_users.to_parquet("parquet_data/users.parquet", index=False, engine="pyarrow", coerce_timestamps="ms")

df_txns = create_transactions()
df_txns.to_parquet("parquet_data/transactions.parquet", index=False, engine="pyarrow", coerce_timestamps="ms")