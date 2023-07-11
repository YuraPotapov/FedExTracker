import unittest
from unittest.mock import AsyncMock, patch

from fastapi import HTTPException
from httpx import Response

from main import get_access_token, track_package


class TestAccessToken(unittest.IsolatedAsyncioTestCase):
    @patch("app.AsyncClient")
    async def test_get_access_token_success(self, mock_async_client):
        mock_response = Response(200, json={"access_token": "test_token", "expires_in": 3600})
        mock_async_client.return_value.__aenter__.return_value.post = AsyncMock(return_value=mock_response)

        token = await get_access_token()

        mock_async_client.assert_called_once()
        mock_async_client.return_value.__aenter__.return_value.post.assert_called_once()
        self.assertEqual(token, "test_token")

    @patch("app.AsyncClient")
    async def test_get_access_token_failure(self, mock_async_client):
        mock_response = Response(500)
        mock_async_client.return_value.__aenter__.return_value.post = AsyncMock(return_value=mock_response)

        with self.assertRaises(HTTPException):
            await get_access_token()

        mock_async_client.assert_called_once()
        mock_async_client.return_value.__aenter__.return_value.post.assert_called_once()


class TestTrackPackage(unittest.IsolatedAsyncioTestCase):
    @patch("app.AsyncClient")
    async def test_track_package_success(self, mock_async_client):
        mock_response = Response(200, json={"tracking_status": "delivered"})
        mock_async_client.return_value.__aenter__.return_value.get = AsyncMock(return_value=mock_response)

        response = await track_package("123456789")

        mock_async_client.assert_called_once()
        mock_async_client.return_value.__aenter__.return_value.get.assert_called_once()
        self.assertEqual(response, {"tracking_status": "delivered"})

    @patch("app.AsyncClient")
    async def test_track_package_failure(self, mock_async_client):
        mock_response = Response(404)
        mock_async_client.return_value.__aenter__.return_value.get = AsyncMock(return_value=mock_response)

        with self.assertRaises(HTTPException):
            await track_package("123456789")

        mock_async_client.assert_called_once()
        mock_async_client.return_value.__aenter__.return_value.get.assert_called_once()


if __name__ == '__main__':
    unittest.main()