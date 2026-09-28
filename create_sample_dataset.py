import pandas as pd
import numpy as np

np.random.seed(42)

# Create sample AIS points around Los Angeles / Long Beach
n = 500

data = {
    "latitude": np.random.uniform(33.60, 33.90, n),
    "longitude": np.random.uniform(-118.45, -118.05, n),
    "sog": np.random.uniform(8, 20, n)
}

df = pd.DataFrame(data)

df.to_parquet("ais_sample.parquet", index=False)

print("Sample AIS dataset created successfully!")
print(f"Rows: {len(df)}")
print("Columns:", list(df.columns))