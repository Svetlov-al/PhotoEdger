from fastapi.testclient import TestClient
from fastapi import Response
from src.image import config


def post_to_add_image(
    client: TestClient,
    title: str,
    desc: str,
    filename: str,
) -> Response:
    url = config.get_api_url()
    with open(filename, "rb") as f:
        r = client.post(
            f"{url}/api/images",
            data={
                "title": title,
                "description": desc,
            },
            files={"file": (filename, f, "image/jpeg")},
        )
    return r


def get_image(client: TestClient, image_id: int) -> Response:
    url = config.get_api_url()
    return client.get(f"{url}/api/images/{image_id}")
