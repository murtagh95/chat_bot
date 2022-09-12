from copy import copy

import pytest
from faker import Faker
from httpx import AsyncClient

from app.core.models.tortoise.message import MessageEnum


faker = Faker()

BASIC_DATA = {
    "text": faker.text(),
    "url": faker.image_url(),
    "list_card": [
        {
            "text": faker.text(),
            "url_image": faker.image_url(),
            "button_list_card": [
                {
                    "text": faker.text(max_nb_chars=10),
                    "value": faker.text(max_nb_chars=10)
                }
            ]
        }
    ],
    "list_button": [
        {
            "text": faker.text(max_nb_chars=10),
            "value": faker.text(max_nb_chars=10)
        },
        {
            "text": faker.text(max_nb_chars=10),
            "value": faker.text(max_nb_chars=10)
        }
    ]
}


@pytest.mark.anyio
class TestCreateMessageTextAndImage:
    url = "/messages/"
    data = {
        "type": MessageEnum.TEXT_AND_IMAGE.value,
        **BASIC_DATA
    }

    async def test_create_text_and_image__ok(self, client: AsyncClient):
        data = copy(self.data)
        data.pop("list_card")
        data.pop("list_button")

        response = await client.post(self.url, json=data)
        assert response.status_code == 201

    async def test_create_text_and_image__url_error(self, client: AsyncClient):
        data = copy(self.data)
        data.pop("list_button")
        data.pop("list_card")
        data.pop("url")

        response = await client.post(self.url, json=data)

        assert response.status_code == 422
        assert isinstance(
            response.json().get("detail", None),
            list
        )
        assert response.json().get("detail")[0]["msg"] == \
               "url is required for type text_and_image"

    async def test_create_text_and_image__list_button_error(
            self, client: AsyncClient):
        data = copy(self.data)
        data.pop("list_card")

        response = await client.post(self.url, json=data)

        assert response.status_code == 422
        assert isinstance(
            response.json().get("detail", None),
            list
        )
        assert response.json().get("detail")[0]["msg"] == \
               "list_button should not be sent when it is of type " \
               "text_and_image"

    async def test_create_text_and_image__list_card_error(
            self, client: AsyncClient):
        data = copy(self.data)
        data.pop("list_button")

        response = await client.post(self.url, json=data)

        assert response.status_code == 422
        assert isinstance(
            response.json().get("detail", None),
            list
        )
        assert response.json().get("detail")[0]["msg"] == \
               "list_card should not be sent when it is of type text_and_image"


@pytest.mark.anyio
class TestCreateMessageListOfButtons:
    url = "/messages/"
    data = {
        "type": MessageEnum.LIST_OF_BUTTONS.value,
        **BASIC_DATA
    }

    async def test_create_list_of_buttons__ok(self, client: AsyncClient):
        data = copy(self.data)
        data.pop("list_card")
        data.pop("url")

        response = await client.post(self.url, json=data)
        assert response.status_code == 201

    async def test_create_list_of_buttons__url_error(
            self, client: AsyncClient):
        data = copy(self.data)
        data.pop("list_card")

        response = await client.post(self.url, json=data)

        assert response.status_code == 422
        assert isinstance(
            response.json().get("detail", None),
            list
        )
        assert response.json().get("detail")[0]["msg"] == \
               "url should not be sent when it is of type list_of_buttons"

    async def test_create_list_of_buttons__list_button_error(
            self, client: AsyncClient):
        data = copy(self.data)
        data.pop("list_card")
        data.pop("list_button")
        data.pop("url")

        response = await client.post(self.url, json=data)

        assert response.status_code == 422
        assert isinstance(
            response.json().get("detail", None),
            list
        )
        assert response.json().get("detail")[0]["msg"] == \
               "list_button is required for type list_of_buttons"

    async def test_create_list_of_buttons__list_card_error(
            self, client: AsyncClient):
        data = copy(self.data)
        data.pop("url")

        response = await client.post(self.url, json=data)

        assert response.status_code == 422
        assert isinstance(
            response.json().get("detail", None),
            list
        )
        assert response.json().get("detail")[0]["msg"] == \
               "list_card should not be sent when it is of type " \
               "list_of_buttons"
