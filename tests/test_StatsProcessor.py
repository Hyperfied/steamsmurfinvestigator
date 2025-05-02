import pytest
import json
from unittest.mock import MagicMock, patch
from server.StatsProcessor import (
    getPlayerSummary,
    getFriendInfo,
    getBans,
    getRecentPlaytime,
    getAccountValue,
    getAccountAge,
    getGames,
    getNumOfGames,
    getTop25,
    getTotalPlaytime,
    getAchievementCompletion,
    profilePictureLink,
    profilePictureLinkFull,
    profilePictureLinkMedium,
    realName,
    personaName,
    tryVanityURL,
    steamKey
)

player_summary = {"response":{"players":[{"steamid":"76561198289757367","communityvisibilitystate":3,"profilestate":1,"personaname":"Hyperfied","profileurl":"https://steamcommunity.com/id/hyperfied/","avatar":"https://avatars.steamstatic.com/a39e04ddb906ebb951d0a8667411fbd2381c3d73.jpg","avatarmedium":"https://avatars.steamstatic.com/a39e04ddb906ebb951d0a8667411fbd2381c3d73_medium.jpg","avatarfull":"https://avatars.steamstatic.com/a39e04ddb906ebb951d0a8667411fbd2381c3d73_full.jpg","avatarhash":"a39e04ddb906ebb951d0a8667411fbd2381c3d73","lastlogoff":1746028824,"personastate":0,"realname":"Lewis","primaryclanid":"103582791429521408","timecreated":1457797045,"personastateflags":0,"loccountrycode":"GB"}]}}

@pytest.mark.asyncio
@patch("server.StatsProcessor.requests.get")
async def test_tryVanityURL(mock_get):
    mock_response = MagicMock()
    mock_response.json.return_value = {"response":{"steamid":"76561198289757367","success":1}}
    mock_response.status_code = 200
    
    
    mock_get.return_value = mock_response
    
    result = await tryVanityURL("hyperfied")
    
    assert result == "76561198289757367"
    mock_get.assert_called_once_with(f"https://api.steampowered.com/ISteamUser/ResolveVanityURL/v1/?key={steamKey}&vanityurl=hyperfied")
    
@pytest.mark.asyncio
@patch("server.StatsProcessor.requests.get")
async def test_getPlayerSummary(mock_get):
    mock_response = MagicMock()
    mock_response.json.return_value = player_summary
    mock_response.status_code = 200
    
    mock_get.return_value = mock_response
    
    result = await getPlayerSummary("76561198289757367")
    
    assert result["steamid"] == "76561198289757367"
    assert result["personaname"] == "Hyperfied"
    assert result["realname"] == "Lewis"
    assert result["profileurl"] == "https://steamcommunity.com/id/hyperfied/"
    assert result["avatar"] == "https://avatars.steamstatic.com/a39e04ddb906ebb951d0a8667411fbd2381c3d73.jpg"
    assert result["avatarmedium"] == "https://avatars.steamstatic.com/a39e04ddb906ebb951d0a8667411fbd2381c3d73_medium.jpg"
    assert result["avatarfull"] == "https://avatars.steamstatic.com/a39e04ddb906ebb951d0a8667411fbd2381c3d73_full.jpg"
    assert result["avatarhash"] == "a39e04ddb906ebb951d0a8667411fbd2381c3d73"
    assert result["lastlogoff"] == 1746028824
    assert result["personastate"] == 0
    assert result["primaryclanid"] == "103582791429521408"
    assert result["timecreated"] == 1457797045
    assert result["personastateflags"] == 0
    assert result["loccountrycode"] == "GB"
    assert result["communityvisibilitystate"] == 3
    assert result["profilestate"] == 1
    
@pytest.mark.asyncio
@patch("server.StatsProcessor.requests.get")
async def test_getFriendInfo(mock_get):
    mock_response = MagicMock()
    mock_response.json.return_value = {"friendslist":{"friends":[{"steamid":"76561198058529531","relationship":"friend","friend_since":1722890042},{"steamid":"76561198072684174","relationship":"friend","friend_since":1696794666},{"steamid":"76561198095367691","relationship":"friend","friend_since":1575344111},{"steamid":"76561198109177128","relationship":"friend","friend_since":1659634210},{"steamid":"76561198109610483","relationship":"friend","friend_since":1715254172},{"steamid":"76561198114505106","relationship":"friend","friend_since":1471011336},{"steamid":"76561198124555325","relationship":"friend","friend_since":1698258492},{"steamid":"76561198130952116","relationship":"friend","friend_since":1704580544},{"steamid":"76561198199731679","relationship":"friend","friend_since":1517349295},{"steamid":"76561198243893798","relationship":"friend","friend_since":1716313665},{"steamid":"76561198250430552","relationship":"friend","friend_since":1659640441},{"steamid":"76561198253545021","relationship":"friend","friend_since":1705019120},{"steamid":"76561198254307125","relationship":"friend","friend_since":1742764749},{"steamid":"76561198271805718","relationship":"friend","friend_since":1696799182},{"steamid":"76561198271933966","relationship":"friend","friend_since":1679887631},{"steamid":"76561198287330136","relationship":"friend","friend_since":1467404312},{"steamid":"76561198289832217","relationship":"friend","friend_since":1460816733},{"steamid":"76561198330673361","relationship":"friend","friend_since":1659625082},{"steamid":"76561198337016175","relationship":"friend","friend_since":1666712802},{"steamid":"76561198355010318","relationship":"friend","friend_since":1484475753},{"steamid":"76561198355452946","relationship":"friend","friend_since":1659640493},{"steamid":"76561198357489546","relationship":"friend","friend_since":1745852132},{"steamid":"76561198359012161","relationship":"friend","friend_since":1541938707},{"steamid":"76561198368771986","relationship":"friend","friend_since":1516391227},{"steamid":"76561198384064710","relationship":"friend","friend_since":1695850055},{"steamid":"76561198389978263","relationship":"friend","friend_since":1731774124},{"steamid":"76561198404047726","relationship":"friend","friend_since":1733778626},{"steamid":"76561198411207982","relationship":"friend","friend_since":1695851748},{"steamid":"76561198418796632","relationship":"friend","friend_since":1652449456},{"steamid":"76561198419176762","relationship":"friend","friend_since":1515010543},{"steamid":"76561198436951800","relationship":"friend","friend_since":1685038867},{"steamid":"76561198454531647","relationship":"friend","friend_since":1712580558},{"steamid":"76561198880187914","relationship":"friend","friend_since":1733313313},{"steamid":"76561198997115706","relationship":"friend","friend_since":1681650303},{"steamid":"76561199005518304","relationship":"friend","friend_since":1651149342},{"steamid":"76561199011784988","relationship":"friend","friend_since":1650546489},{"steamid":"76561199013449582","relationship":"friend","friend_since":1730466947},{"steamid":"76561199059902266","relationship":"friend","friend_since":1742765385},{"steamid":"76561199220224734","relationship":"friend","friend_since":1706390795},{"steamid":"76561199225322240","relationship":"friend","friend_since":1704750556},{"steamid":"76561199249394945","relationship":"friend","friend_since":1672005341},{"steamid":"76561199426801670","relationship":"friend","friend_since":1704580557},{"steamid":"76561199483427220","relationship":"friend","friend_since":1722531455},{"steamid":"76561199613373518","relationship":"friend","friend_since":1705518715}]}}
    mock_response.status_code = 200
    
    mock_get.return_value = mock_response
    
    result = await getFriendInfo("76561198289757367")
    
    assert result[0] == 44
    assert result[1] == [
            1722890042, 1696794666, 1575344111, 1659634210, 1715254172, 1471011336, 1698258492, 1704580544, 1517349295, 1716313665, 1659640441, 1705019120, 1742764749, 1696799182, 1679887631, 1467404312, 1460816733, 1659625082, 1666712802, 1484475753, 1659640493, 1745852132, 1541938707, 1516391227, 1695850055, 1731774124, 1733778626, 1695851748, 1652449456, 1515010543, 1685038867, 1712580558, 1733313313, 1681650303, 1651149342, 1650546489, 1730466947, 1742765385, 1706390795, 1704750556, 1672005341, 1704580557, 1722531455, 1705518715
        ]
    
@pytest.mark.asyncio
@patch("server.StatsProcessor.requests.get")
async def test_getBans(mock_get):
    mock_response = MagicMock()
    mock_response.json.return_value = {"players":[{"SteamId":"76561198289757367","CommunityBanned":False,"VACBanned":False,"NumberOfVACBans":0,"DaysSinceLastBan":0,"NumberOfGameBans":0,"EconomyBan":"none"}]}
    mock_response.status_code = 200
    
    mock_get.return_value = mock_response
    
    result = await getBans("76561198289757367")
    
    assert result[0] == 0
    assert result[1] == 0
    
@pytest.mark.asyncio
@patch("server.StatsProcessor.requests.get")
async def test_getRecentPlaytime(mock_get):
    mock_response = MagicMock()
    mock_response.json.return_value = {"response":{"total_count":3,"games":[{"appid":2379780,"name":"Balatro","playtime_2weeks":845,"playtime_forever":5520,"img_icon_url":"b6018068070ab0e23561694c11f7950dd6f4c752","playtime_windows_forever":5520,"playtime_mac_forever":0,"playtime_linux_forever":0,"playtime_deck_forever":0},{"appid":2943650,"name":"FragPunk","playtime_2weeks":23,"playtime_forever":88,"img_icon_url":"7e4276d769044a725905fe72c2d78977fde908e2","playtime_windows_forever":88,"playtime_mac_forever":0,"playtime_linux_forever":0,"playtime_deck_forever":0},{"appid":105600,"name":"Terraria","playtime_2weeks":19,"playtime_forever":9308,"img_icon_url":"858961e95fbf869f136e1770d586e0caefd4cfac","playtime_windows_forever":8640,"playtime_mac_forever":0,"playtime_linux_forever":0,"playtime_deck_forever":0}]}}
    mock_response.status_code = 200
    
    mock_get.return_value = mock_response
    
    result = await getRecentPlaytime("76561198289757367")
    
    assert result == 14.783333333333333

@pytest.mark.asyncio
@patch("server.StatsProcessor.requests.get")
async def test_getGames(mock_get):
    mock_response = MagicMock()
    
    with open("tests/games_response.json", "r") as file:
        mock_response.json.return_value = json.load(file)

    mock_response.status_code = 200
    
    mock_get.return_value = mock_response
    
    result = await getGames("76561198289757367")
    
    assert result[0] == 126
    assert result[1] == 3047.65
    assert result[2] == 9.070386904761905
    
    # Achievements done in the achievement test
    #assert result[3] == 28.816360840370262
    #assert result[4] == 1442
    #assert result[5] == 7669
    
    assert len(result[6]) == 25
    assert len(result[7]) == 25
    assert len(result[8]) == 25
    assert isinstance(result[6], list)
    assert isinstance(result[7], list)
    assert isinstance(result[8], list)
    
@pytest.mark.asyncio
@patch("server.StatsProcessor.requests.get")
async def test_getAccountValue(mock_get):
    def mock_requests_side_effect(url, *args, **kwargs):
        if "GetOwnedGames" in url:
            # Mock response for the GetOwnedGames API call
            with open("tests/games_response.json", "r") as file:
                return_value = MagicMock()
                return_value.status_code = 200
                return_value.json.return_value = json.load(file)
                return return_value
        elif "api/appdetails" in url:
            # Mock response for the GetPlayerSummaries API call
            if "?appids=4000" in url:
                with open("tests/value_response_1.json", "r") as file:
                    return_value = MagicMock()
                    return_value.status_code = 200
                    
                    return_value.json.return_value = json.load(file)
                    return return_value
            else:
                with open("tests/value_response_2.json", "r") as file:
                    return_value = MagicMock()
                    return_value.status_code = 200
                    
                    return_value.json.return_value = json.load(file)
                    return return_value
        else:
            raise ValueError(f"Unexpected URL: {url}")

    mock_get.side_effect = mock_requests_side_effect
    
    result = await getAccountValue("76561198289757367")
    
    assert result == 1550.6800000000005
    
def test_personaName():
    assert personaName(player_summary.get("response").get("players")[0]) == "Hyperfied"
    
def test_realName():
    assert realName(player_summary.get("response").get("players")[0]) == "Lewis"
    
def test_profilePictureLink():
    assert profilePictureLink(player_summary.get("response").get("players")[0]) == "https://avatars.steamstatic.com/a39e04ddb906ebb951d0a8667411fbd2381c3d73.jpg"
    
def test_profilePictureLinkFull():
    assert profilePictureLinkFull(player_summary.get("response").get("players")[0]) == "https://avatars.steamstatic.com/a39e04ddb906ebb951d0a8667411fbd2381c3d73_full.jpg"
    
def test_profilePictureLinkMedium():
    assert profilePictureLinkMedium(player_summary.get("response").get("players")[0]) == "https://avatars.steamstatic.com/a39e04ddb906ebb951d0a8667411fbd2381c3d73_medium.jpg"

def test_getAccountAge():
    age = getAccountAge(player_summary.get("response").get("players")[0])
    
    assert isinstance(age, int)
    assert age > 0
    
    assert age < 1000000000  # Arbitrary large number to ensure it's a reasonable age
    
def test_getNumOfGames():
    with open("tests/games_response.json", "r") as file:
        games_response = json.load(file)
    
    num_of_games = getNumOfGames(games_response.get("response"))
    
    assert num_of_games == 126  # Adjust this based on the actual number of games in the mock response
    assert isinstance(num_of_games, int)
    
def test_getTop25():
    with open("tests/games_response.json", "r") as file:
        games_response = json.load(file)
    
    top25names, top25pictures, top25Playtime = getTop25(games_response.get("response"))
    
    assert len(top25names) == 25
    assert len(top25pictures) == 25
    assert len(top25Playtime) == 25
    
    assert isinstance(top25names, list)
    assert all(isinstance(name, str) for name in top25names)
    assert isinstance(top25pictures, list)
    assert all(isinstance(picture, str) for picture in top25pictures)
    assert isinstance(top25Playtime, list)
    assert all(isinstance(playtime, (int, float)) for playtime in top25Playtime)
    
def test_getTotalPlaytime():
    with open("tests/games_response.json", "r") as file:
        games_response = json.load(file)
    
    total_playtime, average_recent_playtime = getTotalPlaytime(games_response.get("response"))
    
    assert isinstance(total_playtime, (int, float))
    assert total_playtime == 3047.65
    
    assert isinstance(average_recent_playtime, (int, float))
    assert average_recent_playtime == 9.070386904761905

@pytest.mark.asyncio
@patch("server.StatsProcessor.requests.get")
def test_getAchievementCompletion(mock_get):
    with open("tests/games_response.json", "r") as file:
        games_response = json.load(file)
    
    with open("tests/achievement_response.json", "r", encoding="utf8") as file:
        mock_response = MagicMock()
        mock_response.json.return_value = json.load(file)
        mock_response.status_code = 200
    
    mock_get.return_value = mock_response
    
    result = getAchievementCompletion(games_response.get("response"), "76561198289757367")
    
    assert result[0] == 28.816360840370262 # Achievement completion percentage
    assert result[1] == 1442 # Total completed achievements
    assert result[2] == 7669 # Total possible achievements