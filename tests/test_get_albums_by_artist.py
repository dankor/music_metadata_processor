from unittest.mock import patch
from app.utils import musicbrainz

mocked_data = [
    {
        "id": "caef5f01-8568-4573-8458-c9e99ff7c734",
        "type": "Album",
        "title": "Night Visions",
        "first-release-date": "2012-09-04",
        "primary-type": "Album",
    },
    {
        "id": "a186ae54-41a1-4b46-861c-c0d80c154556",
        "type": "Single",
        "title": "Smoke + Mirrors",
        "first-release-date": "2015-02-13",
        "primary-type": "Single",
    },
    {
        "id": "8341c952-694d-4866-870e-df48c9e10f17",
        "type": "Album",
        "title": "Evolve",
        "first-release-date": "2017-06-23",
        "primary-type": "Album",
    },
]


@patch.object(musicbrainz, "pagination_loop")
def test_get_albums_by_artist(mock_pagination_loop):
    mock_pagination_loop.return_value = mocked_data
    albums = musicbrainz.get_albums_by_artist("1")
    assert len(albums) == 2
    assert all(album["type"] == "Album" for album in albums)
