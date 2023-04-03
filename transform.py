import pandas as pd

from extract import retrieve_data


def data_verify(df: pd.DataFrame) -> bool:
    """Used to check for empty data frame, enforce
    unique constraint, checking for null values.

    Args:
        df (pd.DataFrame): Data frame to check before
        transform

    Raises:
        Exception: Primary key exception, data might contain duplicates
        Exception: Null values found

    Returns:
        bool: False if df is empty else None
    """
    # Check whether the dataframe is empty
    if df.empty:
        print("No songs extracted")
        return False
    
    # Enforcing Primary keys since we don't need duplicates
    if pd.Series(df['played_at']).is_unique:
        pass
    else:
        # Immediately terminate the program and avoid further processing
        raise Exception("Primary key exception, data might contain duplicates")
    
    if df.isnull().values.any():
        raise Exception("Null values found")


def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    """Transformation to get the count of artist

    Args:
        df (pd.DataFrame): Data frame extract from Spotify API response

    Returns:
        pd.DataFrame: Data frame after transformation to get count of artist
    """
    # Applying transformation logic
    transformed_df = df.groupby(['timestamp', 'artist_name'], as_index=False).count()
    transformed_df.rename(columns={"played_at": "count"}, inplace=True)

    # Creating a Primary key based on timestamp and artist name
    transformed_df["id"] = transformed_df["timestamp"].astype(str) + "-" + transformed_df["artist_name"]
    transformed_df = transformed_df[["id", "timestamp", "artist_name", "count"]]

    return transformed_df


if __name__ == "__main__":
    load_df = retrieve_data()
    data_verify(load_df)
    transformed_df = transform_data(load_df)
    print(transformed_df)
