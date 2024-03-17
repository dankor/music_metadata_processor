from unittest.mock import patch
from app.utils import musicbrainz

mocked_data = [
    {
        "id": "bf028638-5789-46dc-8fcf-e9ac1ec8a61f",
        "title": "Night Visions",
        "status": "Official",
        "quality": "normal",
        "packaging": "None",
        "text-representation": {"language": "eng", "script": "Latn"},
        "date": "2012-09-04",
        "country": "DZ",
        "release-event-count": 166,
        "barcode": "00602537224227",
        "cover-art-archive": {
            "artwork": "true",
            "count": "1",
            "front": "true",
            "back": "false",
        },
    },
    {
        "id": "86351876-1cb2-489c-a85d-65026f6249e0",
        "title": "Night Visions",
        "status": "Official",
        "quality": "normal",
        "packaging": "None",
        "text-representation": {"language": "eng", "script": "Latn"},
        "date": "2012-09-04",
        "country": "CA",
        "release-event-count": 3,
        "barcode": "00602537150120",
        "cover-art-archive": {
            "artwork": "true",
            "count": "13",
            "front": "true",
            "back": "false",
        },
    },
    {
        "id": "fb44a782-9e6b-4af3-a634-76373cf42264",
        "title": "Night Visions",
        "status": "Official",
        "quality": "normal",
        "packaging": "None",
        "text-representation": {"language": "eng", "script": "Latn"},
        "date": "2012-09-04",
        "country": "CA",
        "release-event-count": 120,
        "barcode": "602537126835",
        "asin": "B0092MKTL2",
        "cover-art-archive": {
            "artwork": "true",
            "count": "1",
            "front": "true",
            "back": "false",
        },
    },
]


@patch.object(musicbrainz, "pagination_loop")
def test_get_albums_by_artist(mock_pagination_loop):
    mock_pagination_loop.return_value = mocked_data
    release = musicbrainz.get_most_relevant_releases("1")
    assert "id" in release
    assert release["release-event-count"] == 166
