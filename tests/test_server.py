import pytest
from fastapi.testclient import TestClient
from server.server import app
from unittest.mock import patch, AsyncMock

client = TestClient(app)

@pytest.mark.asyncio
@patch("server.StatsProcessor.tryVanityURL", new_callable=AsyncMock)
def test_profile_vanityurl(mock_tryVanityURL):
    # Mock the return value of tryVanityURL
    mock_tryVanityURL.return_value = "76561198289757367"

    # Make a request to the endpoint
    response = client.get("/profile/vanityurl/hyperfied")

    # Assert the response status code
    assert response.status_code == 200

    # Assert the response JSON
    assert response.json() == {"steamid": "76561198289757367"}

    # Assert the mock was called with the correct argument
    mock_tryVanityURL.assert_called_once_with("hyperfied")


@pytest.mark.asyncio
@patch("server.StatsProcessor.getPlayerSummary", new_callable=AsyncMock)
def test_profile_summary(mock_getPlayerSummary):
    mock_getPlayerSummary.return_value = {
            "steamid":"76561198289757367",
            "communityvisibilitystate":3,
            "profilestate":1,
            "personaname":"Hyperfied",
            "profileurl":"https://steamcommunity.com/id/hyperfied/",
            "avatar":"https://avatars.steamstatic.com/a39e04ddb906ebb951d0a8667411fbd2381c3d73.jpg",
            "avatarmedium":"https://avatars.steamstatic.com/a39e04ddb906ebb951d0a8667411fbd2381c3d73_medium.jpg",
            "avatarfull":"https://avatars.steamstatic.com/a39e04ddb906ebb951d0a8667411fbd2381c3d73_full.jpg",
            "avatarhash":"a39e04ddb906ebb951d0a8667411fbd2381c3d73",
            "lastlogoff":1746028824,
            "personastate":0,
            "realname":"Lewis",
            "primaryclanid":"103582791429521408",
            "timecreated":1457797045,
            "personastateflags":0,
            "loccountrycode":"GB"
        }
    
    # Make a request to the endpoint
    response = client.get("/profile/summary/76561198289757367")
    
    # Assert the response status code
    assert response.status_code == 200
    
    # Assert the response JSON
    response_json = response.json()
    
    # Assert fixed fields
    assert response_json["personaName"] == "Hyperfied"
    assert response_json["realName"] == "Lewis"
    assert response_json["avatar"] == "https://avatars.steamstatic.com/a39e04ddb906ebb951d0a8667411fbd2381c3d73.jpg"
    assert response_json["avatarFull"] == "https://avatars.steamstatic.com/a39e04ddb906ebb951d0a8667411fbd2381c3d73_full.jpg"
    assert response_json["avatarMedium"] == "https://avatars.steamstatic.com/a39e04ddb906ebb951d0a8667411fbd2381c3d73_medium.jpg"

     # Assert accountAgeSeconds is present and is an integer
    assert "accountAgeSeconds" in response_json
    assert isinstance(response_json["accountAgeSeconds"], int)
    