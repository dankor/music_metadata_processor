from unittest.mock import patch
from app.utils import musicbrainz

mocked_data = [
    {
        "id": "eb5913a4-c8d6-4e1c-81e5-03fed0b6a8ee",
        "title": "Amsterdam",
        "length": "241426",
    },
    {
        "id": "4eb1b584-80be-493e-953e-a0c65c120b34",
        "title": "Bleeding Out",
        "length": "223106",
    },
    {
        "id": "54adc6e3-5d7f-4808-bdb6-ab7f3bf154ca",
        "title": "Cha‐Ching (Till We Grow Older)",
        "length": "249466",
    },
]


@patch.object(musicbrainz, "pagination_loop")
def test_get_recordings_by_release(mock_pagination_loop):
    mock_pagination_loop.return_value = mocked_data
    recordings = musicbrainz.get_recordings_by_release("1")
    assert len(recordings) == 3
    assert all(
        all(key in recording for key in ["id", "title", "length"])
        for recording in recordings
    )
