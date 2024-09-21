import uuid

from fastapi import status
from fastapi.testclient import TestClient

from . import api_client


def random_suffix():
    return uuid.uuid4().hex[:6]


def random_title(name=""):
    return f"i-{name}-{random_suffix()}"


def test_happy_path_returns_201(client: TestClient) -> None:
    r = api_client.post_to_add_image(
        client,
        random_title(),
        "desc",
        filename="tests/e2e/test.jpg",
    )

    assert r.status_code == status.HTTP_201_CREATED


def test_unhappy_path_returs_404(client: TestClient) -> None:
    r = api_client.get_image(client, 9999999)

    assert r.status_code == status.HTTP_404_NOT_FOUND
