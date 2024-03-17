from app.utils.musicbrainz import pagination_loop


class PaginationBuilder:
    def __init__(self, count):
        self.count = count
        self.array = [{"id": id, "name": f"value_{id}"} for id in range(count)]

    def get_page(self, limit, offset, entity_name):
        if offset > self.count:
            return {f"{entity_name}-list": []}
        else:
            return {f"{entity_name}-list": self.array[offset : offset + limit]}


def test_pagination_loop_0_items():
    count = 0
    fake_api_method = PaginationBuilder(count)
    array = pagination_loop(fake_api_method.get_page, {"entity_name": "test"})
    assert len(array) == count


def test_pagination_loop_1_items():
    count = 1
    fake_api_method = PaginationBuilder(count)
    array = pagination_loop(fake_api_method.get_page, {"entity_name": "test"})
    assert len(array) == count


def test_pagination_loop_10_items():
    count = 10
    fake_api_method = PaginationBuilder(count)
    array = pagination_loop(fake_api_method.get_page, {"entity_name": "test"})
    assert len(array) == count


def test_pagination_loop_101_items():
    count = 101
    fake_api_method = PaginationBuilder(count)
    array = pagination_loop(fake_api_method.get_page, {"entity_name": "test"})
    assert len(array) == count


def test_pagination_loop_324_items():
    count = 324
    fake_api_method = PaginationBuilder(count)
    array = pagination_loop(fake_api_method.get_page, {"entity_name": "test"})
    assert len(array) == count
