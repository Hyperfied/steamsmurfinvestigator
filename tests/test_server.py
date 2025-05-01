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
    
@pytest.mark.asyncio
@patch("server.StatsProcessor.getFriendInfo", new_callable=AsyncMock)
async def test_profile_friends(mock_getFriendInfo):
    mock_getFriendInfo.return_value = ( 44, [
            1722890042, 1696794666, 1575344111, 1659634210, 1715254172, 1471011336, 1698258492, 1704580544, 1517349295, 1716313665, 1659640441, 1705019120, 1742764749, 1696799182, 1679887631, 1467404312, 1460816733, 1659625082, 1666712802, 1484475753, 1659640493, 1745852132, 1541938707, 1516391227, 1695850055, 1731774124, 1733778626, 1695851748, 1652449456, 1515010543, 1685038867, 1712580558, 1733313313, 1681650303, 1651149342, 1650546489, 1730466947, 1742765385, 1706390795, 1704750556, 1672005341, 1704580557, 1722531455, 1705518715
        ]
    )
    
    response = client.get("/profile/friends/76561198289757367")
    
    assert response.status_code == 200
    
    response_json = response.json()
    
    assert response_json["friendTotal"] == 44
    assert len(response_json["friendTimestamps"]) == 44
    assert isinstance(response_json["friendTimestamps"], list)
    assert all(isinstance(ts, int) for ts in response_json["friendTimestamps"])
    
@pytest.mark.asyncio
@patch("server.StatsProcessor.getBans", new_callable=AsyncMock)
async def test_profile_bans(mock_getBans):
    mock_getBans.return_value = (0, 0)
    
    response = client.get("/profile/bans/76561198289757367")
    
    assert response.status_code == 200
    
    response_json = response.json()
    
    assert response_json["banNumber"] == 0
    assert response_json["currentlyVACBanned"] == 0
    
@pytest.mark.asyncio
@patch("server.StatsProcessor.getRecentPlaytime", new_callable=AsyncMock)
async def test_profile_recent(mock_getRecentPlaytime):
    mock_getRecentPlaytime.return_value = 14.783333333333333
    
    response = client.get("/profile/recent/76561198289757367")
    
    assert response.status_code == 200
    
    response_json = response.json()
    
    assert response_json["recentPlaytimeHours"] == 14.783333333333333
    
@pytest.mark.asyncio
@patch("server.StatsProcessor.getGames", new_callable=AsyncMock)
async def test_profile_games(mock_getGames):
    #{"numberOfGames":126,"totalPlaytimeHours":3047.65,"averageRecentPlaytime":9.070386904761905,"achievementCompletionPercentage":28.816360840370262,"totalCompletedAchievements":1442,"totalPossibleAchievements":7669,"top25GameNames":["Geometry Dash","Call of Duty®","Bloons TD 6","Terraria","Cookie Clicker","Overwatch® 2","NGU IDLE","Celeste","Balatro","Beat Saber","JellyCar Worlds","Hades","Stardew Valley","Aseprite","Forager","Antimatter Dimensions","Revolution Idle","Call of Duty®: Black Ops Cold War","Game Dev Tycoon","Increlution","tModLoader","Call of Duty: Black Ops III","NGU INDUSTRIES","Trimps","OMORI"],"top25GameURL":["https://steamcdn-a.akamaihd.net/steam/apps/322170/header.jpg","https://steamcdn-a.akamaihd.net/steam/apps/1938090/header.jpg","https://steamcdn-a.akamaihd.net/steam/apps/960090/header.jpg","https://steamcdn-a.akamaihd.net/steam/apps/105600/header.jpg","https://steamcdn-a.akamaihd.net/steam/apps/1454400/header.jpg","https://steamcdn-a.akamaihd.net/steam/apps/2357570/header.jpg","https://steamcdn-a.akamaihd.net/steam/apps/1147690/header.jpg","https://steamcdn-a.akamaihd.net/steam/apps/504230/header.jpg","https://steamcdn-a.akamaihd.net/steam/apps/2379780/header.jpg","https://steamcdn-a.akamaihd.net/steam/apps/620980/header.jpg","https://steamcdn-a.akamaihd.net/steam/apps/1740930/header.jpg","https://steamcdn-a.akamaihd.net/steam/apps/1145360/header.jpg","https://steamcdn-a.akamaihd.net/steam/apps/413150/header.jpg","https://steamcdn-a.akamaihd.net/steam/apps/431730/header.jpg","https://steamcdn-a.akamaihd.net/steam/apps/751780/header.jpg","https://steamcdn-a.akamaihd.net/steam/apps/1399720/header.jpg","https://steamcdn-a.akamaihd.net/steam/apps/2763740/header.jpg","https://steamcdn-a.akamaihd.net/steam/apps/1985810/header.jpg","https://steamcdn-a.akamaihd.net/steam/apps/239820/header.jpg","https://steamcdn-a.akamaihd.net/steam/apps/1593350/header.jpg","https://steamcdn-a.akamaihd.net/steam/apps/1281930/header.jpg","https://steamcdn-a.akamaihd.net/steam/apps/311210/header.jpg","https://steamcdn-a.akamaihd.net/steam/apps/1433990/header.jpg","https://steamcdn-a.akamaihd.net/steam/apps/1877960/header.jpg","https://steamcdn-a.akamaihd.net/steam/apps/1150690/header.jpg"],"top25Playtime":[1173.4166666666667,223.56666666666666,182.05,155.13333333333333,153.61666666666667,109.68333333333334,101.43333333333334,98.11666666666666,92.0,75.41666666666667,74.13333333333334,64.46666666666667,58.166666666666664,40.8,33.5,29.3,21.233333333333334,19.5,16.6,15.6,15.516666666666667,14.683333333333334,14.416666666666666,13.85,13.733333333333333]}
    mock_getGames.return_value = (
        126, 3047.65, 9.070386904761905, 28.816360840370262, 1442, 7669,
        ["Geometry Dash","Call of Duty®","Bloons TD 6","Terraria","Cookie Clicker","Overwatch® 2","NGU IDLE","Celeste","Balatro","Beat Saber","JellyCar Worlds","Hades","Stardew Valley","Aseprite","Forager","Antimatter Dimensions","Revolution Idle","Call of Duty®: Black Ops Cold War","Game Dev Tycoon","Increlution","tModLoader","Call of Duty: Black Ops III","NGU INDUSTRIES","Trimps","OMORI"], 
        ["https://steamcdn-a.akamaihd.net/steam/apps/322170/header.jpg","https://steamcdn-a.akamaihd.net/steam/apps/1938090/header.jpg","https://steamcdn-a.akamaihd.net/steam/apps/960090/header.jpg","https://steamcdn-a.akamaihd.net/steam/apps/105600/header.jpg","https://steamcdn-a.akamaihd.net/steam/apps/1454400/header.jpg","https://steamcdn-a.akamaihd.net/steam/apps/2357570/header.jpg","https://steamcdn-a.akamaihd.net/steam/apps/1147690/header.jpg","https://steamcdn-a.akamaihd.net/steam/apps/504230/header.jpg","https://steamcdn-a.akamaihd.net/steam/apps/2379780/header.jpg","https://steamcdn-a.akamaihd.net/steam/apps/620980/header.jpg","https://steamcdn-a.akamaihd.net/steam/apps/1740930/header.jpg","https://steamcdn-a.akamaihd.net/steam/apps/1145360/header.jpg","https://steamcdn-a.akamaihd.net/steam/apps/413150/header.jpg","https://steamcdn-a.akamaihd.net/steam/apps/431730/header.jpg","https://steamcdn-a.akamaihd.net/steam/apps/751780/header.jpg","https://steamcdn-a.akamaihd.net/steam/apps/1399720/header.jpg","https://steamcdn-a.akamaihd.net/steam/apps/2763740/header.jpg","https://steamcdn-a.akamaihd.net/steam/apps/1985810/header.jpg","https://steamcdn-a.akamaihd.net/steam/apps/239820/header.jpg","https://steamcdn-a.akamaihd.net/steam/apps/1593350/header.jpg","https://steamcdn-a.akamaihd.net/steam/apps/1281930/header.jpg","https://steamcdn-a.akamaihd.net/steam/apps/311210/header.jpg","https://steamcdn-a.akamaihd.net/steam/apps/1433990/header.jpg","https://steamcdn-a.akamaihd.net/steam/apps/1877960/header.jpg","https://steamcdn-a.akamaihd.net/steam/apps/1150690/header.jpg"], 
        [1173.4166666666667,223.56666666666666,182.05,155.13333333333333,153.61666666666667,109.68333333333334,101.43333333333334,98.11666666666666,92.0,75.41666666666667,74.13333333333334,64.46666666666667,58.166666666666664,40.8,33.5,29.3,21.233333333333334,19.5,16.6,15.6,15.516666666666667,14.683333333333334,14.416666666666666,13.85,13.733333333333333]
    )
    
    response = client.get("/profile/games/76561198289757367")
    
    assert response.status_code == 200
    
    response_json = response.json()
    
    assert response_json["numberOfGames"] == 126
    assert response_json["totalPlaytimeHours"] == 3047.65
    assert response_json["averageRecentPlaytime"] == 9.070386904761905
    assert response_json["achievementCompletionPercentage"] == 28.816360840370262
    assert response_json["totalCompletedAchievements"] == 1442
    assert response_json["totalPossibleAchievements"] == 7669
    assert len(response_json["top25GameNames"]) == 25
    assert len(response_json["top25GameURL"]) == 25
    assert len(response_json["top25Playtime"]) == 25
    assert all(isinstance(name, str) for name in response_json["top25GameNames"])
    assert all(isinstance(url, str) for url in response_json["top25GameURL"])
    assert all(isinstance(playtime, (int, float)) for playtime in response_json["top25Playtime"])
   
