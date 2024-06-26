import pytest
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


@pytest.mark.asyncio
async def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert "successful" in response.json()
