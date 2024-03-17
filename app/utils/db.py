import os
import pandas as pd
from sqlalchemy import create_engine, text


class Database:
    def __init__(self):
        self.db_user = os.environ.get("POSTGRES_USER")
        self.db_password = os.environ.get("POSTGRES_PASSWORD")
        self.db_host = "db"
        self.db_port = "5432"
        self.db_name = "music_metadata"

    def ingest_data(self, table, data):
        engine = create_engine(
            f"postgresql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"
        )
        df = pd.DataFrame(data)
        df.to_sql(table, engine, if_exists="append", index=False)
        engine.dispose()

    def query_to_html(self, query):
        engine = create_engine(
            f"postgresql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"
        )
        df = pd.read_sql(text(query), engine)
        engine.dispose()
        return df.to_html(justify="center", index=False)


def get_recordings_by_artist(artist):
    db = Database()
    query = f"""
    select 
        artist.name as "Artist", 
        album.name as "Album", 
        recording.name as "Song", 
        to_char(to_timestamp(recording.length/1000),'mi:ss') as "Length"
    from artist 

        join album 
        on artist.id = album.artist 

        join recording 
        on album.id = recording.album

    where artist.name = '{artist}'
    """
    return db.query_to_html(query)


def get_relevant_recording(keyword):
    db = Database()
    query = f"""
    select 
        artist.name as "Artist", 
        album.name as "Album", 
        recording.name as "Song", 
        to_char(to_timestamp(recording.length/1000),'mi:ss') as "Length"
    from recording

        join album 
        on album.id = recording.album
        
        join artist
        on artist.id = album.artist 
    
    where recording.name ilike '%{keyword}%'
    order by similarity(recording.name, '{keyword}') desc
    limit 1
    """
    return db.query_to_html(query)
