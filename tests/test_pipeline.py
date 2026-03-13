import pandas as pd 
import sys 
from pathlib import Path


sys.path.append(str(Path(__file__).parents[1]))


from src.clean import clean_data

def test_clean_data():
    ### test that clean_data function returns a cleaned dataframe with the expected columns and no missing values


    # creating a tiny mock data matching our data 

    raw = pd.DataFrame({
        "supermarket": ["Tesco", "ASDA"],
        "prices_(£)": [1.50,2.00],
        "prices_unit_(£)":[3.00, 4.00],
        "unit": ["kg", "kg"],
        "names": ["Product A", "Product B"],
        "date": ["20230101", "20230102"],
        "category": ["drinks", "drinks"],
        "own_brand": ["TRUE", "FALSE"],
        "source_file": ["test.csv", "test.csv"],
    })

    cleaned = clean_data(raw)


    # Assertions - these are what CI actually checks

    assert "price_gbp" in cleaned.columns, "price_gbp column is missing"
    assert "price_per_kg" in cleaned.columns, "price_per_kg column is missing"
    assert pd.api.types.is_datetime64_dtype(cleaned["date"]), "date column is not datetime"
    assert cleaned["own_brand"].dtype.name == "boolean", "own_brand not boolean"
    assert len(cleaned) == 2, "cleaned dataframe has incorrect number of rows"


    print("✅ All tests passed!")


if __name__== "__main__":
    test_clean_data()
