import pandas as pd 


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean the input DataFrame by performing various data cleaning operations.

    Args:
        df (pd.DataFrame): The input DataFrame to be cleaned.

    Returns:
        pd.DataFrame: The cleaned DataFrame.
    """
    
    # renaming columns 

    df = df.rename(columns={"prices_(£)": "price_gbp",
                            "prices_unit_(£)": "price_per_kg",
                           "names": "product_name",
                            "supermarket": "retailer"})  # Rename columns for consistency
    

    # fixing date format
    df["date"] = pd.to_datetime(df["date"], format="%Y%m%d")  # Convert to datetime, coerce errors to NaT


    # fixing own brand to boolean 
    df["own_brand"] = df["own_brand"].str.strip().str.upper().map({"TRUE": True, "FALSE": False}).astype("boolean")  # Convert to boolean

    # fixing retailers name
    df["retailer"] = df["retailer"].str.replace("Sains", "Sainsbury's", regex=False)  # Standardize retailer names

    # dropping nulls

    df = df.dropna(subset=["price_gbp", "product_name", "price_per_kg", "own_brand"])  # Drop rows with any null values

    # Remove duplicates
    df = df.drop_duplicates()
    
    # resetting index
    df = df.reset_index(drop=True)  # Reset index after dropping rows

    print (f"✅ Cleaned data: {len(df)} rows remaining after cleaning.")
    return df