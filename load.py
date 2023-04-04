import sqlite3
import sqlalchemy

from extract import retrieve_data
from transform import verify_data, transform_data

DATABASE_URL = "sqlite:///my_played_tracks.sqlite"

if __name__ == "__main__":
    # Extract data from Spotify API respone
    load_df = retrieve_data()
    
    if verify_data(load_df) == False:
        raise Exception("Failed at data validation")
    
    transformed_df = transform_data(load_df)

    # Loading into database
    engine = sqlalchemy.create_engine(DATABASE_URL)
    conn = sqlite3.connect("my_played_tracks.sqlite")
    cursor = conn.cursor()

    # Sql query to create played song table
    stmt_my_played_tracks = """
        CREATE TABLE IF NOT EXISTS my_played_tracks (
            song_name VARCHAR(200),
            artist_name VARCHAR(200),
            played_at VARCHAR(200),
            timestamp TIMESTAMP,
            CONSTRAINT pk_played_at PRIMARY KEY (played_at)
        );
    """
    stmt_fav_artist = """
        CREATE TABLE IF NOT EXISTS fav_artist (
            id VARCHAR(200),
            timestamp TIMESTAMP,
            artist_name VARCHAR(200),
            count INTEGER,
            CONSTRAINT pk_fav_artist_id PRIMARY KEY (id)
        );
    """

    cursor.execute(stmt_my_played_tracks)
    cursor.execute(stmt_fav_artist)
    print("Opened database successfully")

    try:
        load_df.to_sql("my_played_tracks", engine, index=False, if_exists="append")
    except:
        print("Data already exists in the table 'my_played_tracks'")

    try:
        transformed_df.to_sql("fav_artist", engine, index=False, if_exists="append")
    except:
        print("Data already exists in the table 'fav_artist'")
    
    #cursor.execute('DROP TABLE my_played_tracks')
    #cursor.execute('DROP TABLE fav_artist')

    conn.close()
    print("Closed database successfully")
