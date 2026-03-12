import pandas as pd
import numpy as np
from pathlib import Path

# Data path 
RAW_DATA_DIR = Path(__file__).resolve().parents[1]/ "data" / "raw"


def load_data() -> pd.DataFrame:
    """Load and combines data from the raw data directory.

    Returns:
        pd.DataFrame: The loaded data.
    """
    # Load the data
    files = list(RAW_DATA_DIR.glob("*.csv"))

    if not files: # Check if any CSV files are found
        raise FileNotFoundError(f"No CSV files found in {RAW_DATA_DIR}")
    

    dfs = []
    for file in files:
            df = pd.read_csv(file,encoding="utf-8",parse_dates=False,dtype={"own_brand": str}) # Load the CSV file into a DataFrame
            df["source_file"] = file.name  # Add a column to identify the source file
            dfs.append(df)   # Append the DataFrame to the list 

    combined = pd.concat(dfs, ignore_index=True)  # Combine all DataFrames into a single DataFrame
    print(f"✅ Loaded {len(combined)} rows from {len(files)} files.")
    return combined




