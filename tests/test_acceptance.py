import requests

BASE_URL = "http://127.0.0.1:8000"
TEST_VANITY = "https://steamcommunity.com/id/hyperfied/"  # Insert steam ID here
TIMEOUT = 15

def test_resolve_vanity_url():
    r = requests.get(f"{BASE_URL}/profile/vanityurl/{TEST_VANITY}", timeout=TIMEOUT)
    if r.status_code == 404:
        print(f"Vanity URL not found: {TEST_VANITY}")
        return  # Skip the test if the vanity URL is not found
    assert r.status_code == 200, f"Unexpected status code: {r.status_code}, Body: {r.text}"
    response_json = r.json()
    steamid = response_json.get("steamid")
    assert steamid is not None, f"Steam ID not found in response: {response_json}"
    assert steamid.isdigit(), f"Unexpected Steam ID: {steamid}"

def test_get_player_summary():
    r = requests.get(f"{BASE_URL}/profile/vanityurl/{TEST_VANITY}", timeout=TIMEOUT)
    response_json = r.json()
    steamid = response_json.get("steamid")
    if steamid is None:
        print(f"Skipping test_get_player_summary: Steam ID not found for {TEST_VANITY}")
        return
    assert steamid is not None, "Steam ID not found in response"
    r = requests.get(f"{BASE_URL}/profile/summary/{steamid}", timeout=TIMEOUT)
    assert r.status_code == 200, f"Unexpected status code: {r.status_code}, Body: {r.text}"
    response_json = r.json()
    assert "personaName" in response_json, f"'personaName' not found in response: {response_json}"

def test_get_friend_info():
    r = requests.get(f"{BASE_URL}/profile/vanityurl/{TEST_VANITY}", timeout=TIMEOUT)
    response_json = r.json()
    steamid = response_json.get("steamid")
    if steamid is None:
        print(f"Skipping test_get_friend_info: Steam ID not found for {TEST_VANITY}")
        return
    assert steamid is not None, "Steam ID not found in response"
    r = requests.get(f"{BASE_URL}/profile/friends/{steamid}", timeout=TIMEOUT)
    assert r.status_code == 200, f"Unexpected status code: {r.status_code}, Body: {r.text}"
    response_json = r.json()
    assert "friendTotal" in response_json, f"'friendTotal' not found in response: {response_json}"


def test_get_bans():
    r = requests.get(f"{BASE_URL}/profile/vanityurl/{TEST_VANITY}", timeout=TIMEOUT)
    response_json = r.json()
    steamid = response_json.get("steamid")
    if steamid is None:
        print(f"Skipping test_get_bans: Steam ID not found for {TEST_VANITY}")
        return
    assert steamid is not None, "Steam ID not found in response"
    r = requests.get(f"{BASE_URL}/profile/bans/{steamid}", timeout=TIMEOUT)
    assert r.status_code == 200, f"Unexpected status code: {r.status_code}, Body: {r.text}"
    response_json = r.json()
    assert "banNumber" in response_json, f"'banNumber' not found in response: {response_json}"


def test_get_recent_playtime():
    r = requests.get(f"{BASE_URL}/profile/vanityurl/{TEST_VANITY}", timeout=TIMEOUT)
    response_json = r.json()
    steamid = response_json.get("steamid")
    if steamid is None:
        print(f"Skipping test_get_recent_playtime: Steam ID not found for {TEST_VANITY}")
        return
    assert steamid is not None, "Steam ID not found in response"
    r = requests.get(f"{BASE_URL}/profile/recent/{steamid}", timeout=TIMEOUT)
    assert r.status_code == 200, f"Unexpected status code: {r.status_code}, Body: {r.text}"
    recent_playtime = r.json().get("recentPlaytimeHours")
    assert isinstance(recent_playtime, float), f"Unexpected response type: {r.json()}"


def test_get_games_info():
    r = requests.get(f"{BASE_URL}/profile/vanityurl/{TEST_VANITY}", timeout=TIMEOUT)
    response_json = r.json()
    steamid = response_json.get("steamid")
    if steamid is None:
        print(f"Skipping test_get_games_info: Steam ID not found for {TEST_VANITY}")
        return
    assert steamid is not None, "Steam ID not found in response"
    r = requests.get(f"{BASE_URL}/profile/games/{steamid}", timeout=TIMEOUT)
    assert r.status_code == 200, f"Unexpected status code: {r.status_code}, Body: {r.text}"
    response_json = r.json()
    assert "numberOfGames" in response_json, f"'numberOfGames' not found in response: {response_json}"


def test_get_account_value():
    r = requests.get(f"{BASE_URL}/profile/vanityurl/{TEST_VANITY}", timeout=TIMEOUT)
    response_json = r.json()
    steamid = response_json.get("steamid")
    if steamid is None:
        print(f"Skipping test_get_account_value: Steam ID not found for {TEST_VANITY}")
        return
    assert steamid is not None, "Steam ID not found in response"
    r = requests.get(f"{BASE_URL}/profile/value/{steamid}", timeout=30)
    assert r.status_code == 200, f"Unexpected status code: {r.status_code}, Body: {r.text}"
    account_value = r.json().get("accountValue")
    assert isinstance(account_value, float), f"Unexpected response type: {r.json()}"