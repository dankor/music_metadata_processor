import musicbrainzngs
from .db import Database

musicbrainzngs.set_useragent("ExampleApp", "0.1", "http://example.com")

"""
This is a function to pass musicbrainzngs method 
and params to perform an iteration agaist the whole 
dataset while there is a limit: maximum 100 records
per request
"""


def pagination_loop(method, params):
    result = []
    offset = 0
    list_key = None

    while True:
        page = method(**params, offset=offset, limit=100)
        # sort of an automation to get *-list key for different entities
        if not list_key:
            list_key = [item for item in list(page.keys()) if item.endswith("-list")][0]
        if page[list_key] == []:
            break

        result.extend(page[list_key])
        offset += 100
    return result


def get_artist_by_name(artist_name):
    artist_search_result = musicbrainzngs.search_artists(artist=artist_name, limit=1)
    try:
        return [
            artist
            for artist in artist_search_result["artist-list"]
            if artist["name"] == artist_name
        ][0]
    except:
        raise ValueError(f"Can't find any artist containing {artist_name}")


def get_albums_by_artist(artist_id):
    albums = pagination_loop(
        musicbrainzngs.browse_release_groups,
        {"artist": artist_id, "release_type": ["album"]},
    )
    return [album for album in albums if album["type"] == "Album"]


def get_most_relevant_releases(album_id):
    realeases = pagination_loop(
        musicbrainzngs.browse_releases, {"release_group": album_id}
    )
    # remove any releases contaning disambiguation, like remixes, editions, etc
    realeases_cleaned = [
        release for release in realeases if "disambiguation" not in release
    ]
    # let's say the most relevant release contaning the biggest release-event-count
    realeases_sorted = sorted(
        realeases_cleaned,
        key=lambda release: release.get("release-event-count", 0),
        reverse=True,
    )
    return realeases_sorted[0]


def get_recordings_by_release(release):
    recordings = pagination_loop(musicbrainzngs.browse_recordings, {"release": release})
    return recordings


def process_artist_data(artist_name):
    db = Database()
    artist = get_artist_by_name(artist_name)
    db.ingest_data("artist", [{key: artist[key] for key in ["id", "name"]}])
    albums = get_albums_by_artist(artist["id"])
    db.ingest_data(
        "album",
        [
            {"id": album["id"], "name": album["title"], "artist": artist["id"]}
            for album in albums
        ],
    )
    for album in albums:
        best_release = get_most_relevant_releases(album["id"])
        recordings = get_recordings_by_release(best_release["id"])
        db.ingest_data(
            "recording",
            [
                {
                    "id": recording["id"],
                    "name": recording["title"],
                    "album": album["id"],
                    "length": recording["length"],
                }
                for recording in recordings
            ],
        )
