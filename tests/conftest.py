import pytest
import requests


@pytest.fixture()
def get_rest():
    def get_response(url):
        return requests.get('http://localhost/api/v1/' + url)

    return get_response
