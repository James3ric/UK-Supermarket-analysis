import pandas as pd 


def avg_price_by_retailer(df: pd.DataFrame) -> pd.DataFrame:
    """
    Q1 which retailer has the cheapest price per kg on average across all products?
    """
    result = (
        df.groupby("retailer")["price_gbp"]
        .agg(["mean","count","median"])
        .rename(columns={"mean": "avg_price", "count": "num_products", "median": "median_price"})
        .round(2)
        .sort_values("avg_price")
        .reset_index()
    )

    return result


def own_brand_vs_branded(df: pd.DataFrame) -> pd.DataFrame:
    """
    Q2 Do own brand products tend to be cheaper than branded products?
    """
    result = (
        df.groupby(["retailer", "own_brand"])["price_gbp"]
        .mean()
        .round(2)
        .unstack("own_brand")
    )

    # renaming columns to be more descriptive
    result.columns = [f"own_brand_avg" if c else "branded_avg" for c in result.columns]
    result = result.reset_index()

    # only calculate saving if both columns exist
    if "branded_avg" in result.columns and "own_brand_avg" in result.columns:
        result["saving"] = (result["branded_avg"] - result["own_brand_avg"]).round(2)
        result["saving_pct"] = ((result["saving"] / result["branded_avg"]) * 100).round(1)

    return result


def price_by_category(df: pd.DataFrame) -> pd.DataFrame:
    """
    Q3 Which product categories are the most expensive on average?
    """
    result = (
        df.groupby(["category", "retailer"])["price_gbp"].mean()
        .round(2)
        .reset_index()
        .rename(columns={"price_gbp": "avg_price"})
        .sort_values(["category","avg_price"], ascending=[True, False])

    )

    return result



def price_trends_over_time(df: pd.DataFrame) -> pd.DataFrame:
    """
    Q4 How have prices changed over time for different retailers?
    """

    df = df.copy()
    df["month"] = df["date"].dt.to_period("M")


    result = (
        df.groupby(["month", "retailer"])["price_gbp"].mean()
        .round(2)
        .reset_index()
        .rename(columns={"price_gbp": "avg_price"})
    )

    result["month"] = result["month"].astype(str)
    return result


def listings_over_time(df: pd.DataFrame) -> pd.DataFrame:
    """
    Q5 How has the number of products listed by each retailer changed over time?
    """

    df = df.copy()
    df["month"] = df["date"].dt.to_period("M")

    result = (
        df.groupby(["month", "retailer"])["product_name"]
        .count()
        .reset_index()
        .rename(columns={"product_names": "num_listings"})
    )

    result["month"] = result["month"].astype(str)
    return result   

