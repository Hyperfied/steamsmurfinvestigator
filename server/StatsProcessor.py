import requests
import json
import time
import math

with open("secrets.json", "r") as f:
    secrets = json.load(f)
    steamKey = secrets["steamKey"]
    

    
async def tryVanityURL(steamid):
    request = f"https://api.steampowered.com/ISteamUser/ResolveVanityURL/v1/?key={steamKey}&vanityurl={steamid}"
    response = requests.get(request)
    
    if response.status_code != 200:
        print("Error: Unable to resolve vanity URL")
        return steamid
    
    if response.json().get("response").get("success") == 1:
        return response.json().get("response").get("steamid")
    else:
        return steamid

async def getPlayerSummary(steamid):
    requestString = f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/?key={steamKey}&steamids={steamid}"
    response = requests.get(requestString).json()
    return response.get("response").get("players")[0]

async def getFriendInfo(steamid):
    requestString = f"https://api.steampowered.com/ISteamUser/GetFriendList/v1/?key={steamKey}&steamid={steamid}"
    response = requests.get(requestString)
    response = response.json()
    
    if "friendslist" not in response:
        print("Error: Unable to retrieve friends list")
        return 0, []
    
    friendsList = response.get("friendslist").get("friends")
    
    length = len(friendsList)
    
    friendTimestamps = []
    
    for entry in friendsList:
        time = entry.get("friend_since")
        friendTimestamps.append(int(time))
    
    return length, friendTimestamps

async def getBans(steamid):
    requestString = f"https://api.steampowered.com/ISteamUser/GetPlayerBans/v1/?key={steamKey}&steamids={steamid}"
    response = requests.get(requestString).json()
    
    numberOfBans = int(response.get("players")[0].get("NumberOfGameBans"))
    currentlyVACBanned = int(response.get("players")[0].get("VACBanned"))
    
    return numberOfBans, currentlyVACBanned

async def getRecentPlaytime(steamid):
    # Gets total playtime in past 2 weeks from dictionary (in hour format, but you can change it to minutes below)
    # also please note it wont work if your profile has game details set to private / friends only, and / or total playtime is hidden
    requestString = f"https://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v1/?key={steamKey}&steamid={steamid}"
    response = requests.get(requestString).json()
    
    playtime_total_recent = 0

    if "response" in response and "games" in response["response"]:
        for game in response["response"]["games"]:
            playtime_total_recent += game.get("playtime_2weeks", 0)
            
    return playtime_total_recent / 60

async def getGames(steamid):
    requestString = f"https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/?key={steamKey}&steamid={steamid}&include_played_free_games=true&include_appinfo=true"
    response = requests.get(requestString)
    response = response.json()
    gamesResponse = response.get("response")
    
    numOfGames = getNumOfGames(gamesResponse)
    totalPlayTime, averagePlaytimeRecent = getTotalPlaytime(gamesResponse)
    avgAchievementCompletion, totalCompletedAchievements, totalPossibleAchievements = getAchievementCompletion(gamesResponse, steamid)
    top25names, top25pictureURL = getTop25(gamesResponse)
    
    return numOfGames, totalPlayTime, averagePlaytimeRecent, avgAchievementCompletion, totalCompletedAchievements, totalPossibleAchievements
    
async def getAccountValue(steamid):
    
    #Gets list of games, then gets each games price from steam store 
    requestString = f"https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/?key={steamKey}&steamid={steamid}&include_played_free_games=true"
    response = requests.get(requestString)
    dictionary = response.json()
    total_value = 0

    if "response" in dictionary and "games" in dictionary["response"]:
        appids = [] #List comprehension to get all appids from the games list
        for game in dictionary["response"]["games"]:
            appId = game.get ("appid")

            if not appId: #Skip if the appId is missing; theres probably better methods of implementation
                continue
            
            appids.append(appId)

        for i in range(math.ceil(len(appids)/100)):
            appids_string = ",".join(map(str, appids[i*100:(i+1)*100])) # Splitting the appids into chunks of 100 for the API request
            storeUrl = f"https://store.steampowered.com/api/appdetails?appids={appids_string}&cc=us&filters=price_overview" # querying steam store with 100 app ids
            
            storeResponse = requests.get(storeUrl)
            storeData = storeResponse.json()

            for appid in storeData.values():
                if appid.get("success") and "data" in appid and not appid.get("data") == []:
                    price_data = appid.get("data").get("price_overview")
                    if price_data:
                        price = price_data.get("final", 0)
                        total_value += price / 100
    
    return total_value

def personaName(playerSummary):
    return playerSummary.get("personaname")

def realName(playerSummary):
    return playerSummary.get("realname")

def profilePictureLinkFull(playerSummary):
    return playerSummary.get("avatarfull")

def profilePictureLink(playerSummary):
    return playerSummary.get("avatar")

def profilePictureLinkMedium(playerSummary):
    return playerSummary.get("avatarmedium")

def getAccountAge(playerSummary):
    creationTimeStamp = int(playerSummary.get("timecreated"))
    currentTime = int(time.time())
    return currentTime - creationTimeStamp

def getNumOfGames(gamesResponse):
    return gamesResponse.get("game_count")

def getTop25(gamesResponse):
    top25names = []
    top25pictures = []
    for x in range(25):
        top25names.append(0)
        top25pictures.append(0)
    gamesList = gamesResponse.get("games")
    temp = top25names[0]
    totalList = []
    for x in gamesList:
        totalList.append(x)
    sorted = False
    while sorted == False:
        for x in range(len(totalList) - 2):
            if totalList[x].get("playtime_forever") < totalList[x + 1].get("playtime_forever"):
                temp = totalList[x]
                totalList[x] = totalList[x + 1]
                totalList[x + 1] = temp
        for x in range(len(totalList) - 2):
            if totalList[x].get("playtime_forever") >= totalList[x + 1].get("playtime_forever"):
                sorted = True
            else:
                sorted = False
                break
    for x in range(25):
        top25names[x] = totalList[x].get("name")
        top25pictures[x] = totalList[x].get("img_icon_url")
    return top25names, top25pictures
            
def getTotalPlaytime(gamesResponse):
    playtime_total = 0
    max_average_playtime_possible_recent = 336 * 60 #converting possible playtime to minutes; 336 is from 24 (hours) x 14 (days); 336 needs to be in minutes so * 60

    if "games" in gamesResponse:
        for game in gamesResponse["games"]:
            playtime_total += game.get("playtime_forever", 0)
            
    average_playtime_recent = (playtime_total / max_average_playtime_possible_recent) #calculate a percentage for time user played in 2 weeks (336)
    
    return playtime_total / 60, average_playtime_recent

def getAchievementCompletion(gamesResponse, steamid):
    allGames = gamesResponse.get("games", [])
    completion_percentage = 0
    valid_games = 0 
    total_completed_achievements = 0 #to list completed achievements as an integer as well
    total_possible_achievements = 0 #to list possible achievements as an integer as well

    request_string = f"https://api.steampowered.com/IPlayerService/GetTopAchievementsForGames/v1/?key={steamKey}&steamid={steamid}&language=en&max_achievements=10000"
    
    current_string = request_string

    for i, game in enumerate(allGames):
        appId = game["appid"]
        current_string += f"&appids%5B{i}%5D={appId}"

        if i % 100 == 99 or i == len(allGames) - 1:
            # Send the request for the current batch of appids
            response = requests.get(current_string)
            response = response.json()
            
            allGames = response.get("response", {}).get("games", [])
            
            for game in allGames:
                if "total_achievements" in game:
                    total_achievements = game["total_achievements"]
                    if "achievements" in game:
                        completed_achievements = len(game["achievements"])
                        total_completed_achievements += completed_achievements
                        completion_percentage += (completed_achievements / total_achievements) * 100 if total_achievements > 0 else 0
                        valid_games += 1
                    total_possible_achievements += total_achievements

            # Reset the request string for the next batch of appids
            current_string = request_string

    avg_percentage = (completion_percentage / valid_games) if valid_games > 0 else 0 
    return avg_percentage, total_completed_achievements, total_possible_achievements  # return average percentage and total possible achievements; one is a percentage and the other an integer
