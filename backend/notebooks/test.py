import numpy as np
import pandas as pd

# Load the CSV
df = pd.read_csv("Dataset.csv")

# Split into 4 parts
chunks = np.array_split(df, 4)

# Save each part
for i, chunk in enumerate(chunks):
    chunk.to_csv(f"Dataset_{i + 1}.csv", index=False)
