from unittest.mock import patch
from app.utils.musicbrainz import get_artist_by_name

mocked_data = {
    "artist-list": [
        {
            "id": "aae96072-e23c-496a-9016-8637be8c67bc",
            "type": "Group",
            "ext:score": "100",
            "name": "Dragon",
            "sort-name": "Dragon",
            "country": "NZ",
            "area": {
                "id": "8524c7d9-f472-3890-a458-f28d5081d9c4",
                "type": "Country",
                "name": "New Zealand",
                "sort-name": "New Zealand",
                "life-span": {"ended": "false"},
            },
            "begin-area": {
                "id": "b2bc1294-77be-4c7b-af93-9868b83b1f34",
                "type": "City",
                "name": "Auckland",
                "sort-name": "Auckland",
                "life-span": {"ended": "false"},
            },
            "disambiguation": "NZ/Australian rock group",
            "isni-list": ["0000000103764725"],
            "life-span": {"begin": "1972-01", "ended": "false"},
            "alias-list": [{"sort-name": "Hunter", "alias": "Hunter"}],
            "tag-list": [
                {"count": "1", "name": "progressive rock"},
                {"count": "1", "name": "new wave"},
                {"count": "1", "name": "pop rock"},
                {"count": "1", "name": "aln-sh"},
            ],
        }
    ],
    "artist-count": 911,
}


@patch("musicbrainzngs.search_artists")
def test_get_artist_by_name(mock_search_artists):
    name = "Dragon"
    mock_search_artists.return_value = mocked_data
    artist = get_artist_by_name(name)
    assert "id" in artist
    assert artist["name"] == name
