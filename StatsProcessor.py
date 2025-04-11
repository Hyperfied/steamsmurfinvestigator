import requests
import json
import time

with open("secrets.json", "r") as f:
    secrets = json.loads(f)
    steamKey = secrets["steamKey"]


def friendTotal(requestString):
    # finds the length of the nested dictionary "friends"
    response = requests.get(requestString)
    friendList = response.json()
    friendList = friendList["friendslist"]["friends"]
    return len(friendList)


def friendTime(requestString):
    # loops through the nested dictionary friends and adds each UNIX timestamp to a list then returns the list
    response = requests.get(requestString)
    friendList = response.json()
    friendList = friendList["friendslist"]["friends"]
    listOfTime = []
    for entry in friendList:
        time = entry.get("friend_since")
        listOfTime.append(int(time))
    return listOfTime
            

def getBanNumber(requestString):
    # Accesses the dictionary in the list in the dictionary then outputs the number of bans the player has
    response = requests.get(requestString)
    dictionary = response.json()
    dictionary = dictionary.get("players")
    dictionary = dictionary[0]
    numberOfBans = int(dictionary.get("NumberOfGameBans"))
    return numberOfBans

def currentlyVACBanned(requestString):
    # Accesses the dictionary in the list in the dictionary then outputs whether the user is currently VAC banned
    response = requests.get(requestString)
    dictionary = response.json()
    dictionary = dictionary.get("players")
    dictionary = dictionary[0]
    numberOfBans = dictionary.get("VACBanned")
    return numberOfBans

def accountAge(requestString):
    # Gets the time stamp when the account was created then subtracts it from the current UNIX timestamp to give account age
    response = requests.get(requestString)
    dictionary = response.json()
    dictionary = dictionary["response"]["players"]
    dictionary = dictionary[0]
    creationTimeStamp = int(dictionary.get("timecreated"))
    currentTime = int(time.time())
    return currentTime - creationTimeStamp

def numberOfGames(requestString):
    # Gets the list of games played then returns the game count from the dictionary
    response = requests.get(requestString)
    gameList = response.json()
    gameList = gameList.get("response")
    return gameList.get("game_count")

def recentPlayTime(requestString):
    # Gets total playtime in past 2 weeks from dictionary (in hour format, but you can change it to minutes below)
    # also please note it wont work if your profile has game details set to private / friends only, and / or total playtime is hidden
    response = requests.get(requestString)
    dictionary = response.json()
    playtime_total = 0 
    total_possible_playtime = 336 * 60 #converting possible playtime to minutes; 336 is from 24 (hours) x 14 (days); 336 needs to be in minutes so * 60

    if "response" in dictionary and "games" in dictionary["response"]:
        for game in dictionary["response"]["games"]:
            playtime_total += game.get("playtime_2weeks", 0)

    average_playtime_percentage = (playtime_total / total_possible_playtime) * 100 #calculate a percentage for time user played in 2 weeks (336)

    return playtime_total / 60, average_playtime_percentage # will return playtime total in hours, and average playtime as percentage

def totalPlayTime(requestString):
    #Same as above, but gets total playtime across whole account instead of 2 weeks. Same rules apply, you can change it to minutes
    response = requests.get(requestString)
    dictionary = response.json()
    playtime_total = 0

    if "response" in dictionary and "games" in dictionary["response"]:
        for game in dictionary["response"]["games"]:
            playtime_total += game.get("playtime_forever", 0)
    
    return playtime_total / 60 

def achievementCompletion(steamId, requestString):
    # Gets achievements completed and uses the number of completed achievements divided by total possible achievements available x 100 to get an average percentage
    # Pretty sure profiles have to be public for this one too
    # will have to use the get all games owned api 
    response = requests.get(requestString, timeout = 200) # I added a timeout with high value because this one seems to be particularly heavy, you do need to give it time
    dictionary = response.json()
    allGames = dictionary.get("response", {}).get("games", [])
    completion_percentage = 0
    valid_games = 0 
    total_possible_achievements = 0 #to list possible achievements as an integer as well

    for game in allGames:
        appId = game["appid"]
    
        requestType = "https://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v1/?key=" #Has to be in here, if you can think of a way to neaten it so its consistent feel free to modify
        requestString = requestType + steamKey + "&steamid=" + steamId + "&appid=" + str(appId)
        achievement_response = requests.get(requestString)
        achievement_data = achievement_response.json()
    
        achievement = achievement_data.get("playerstats", {}).get("achievements", [])
        possibleAchievements = len(achievement) #Used for counting over possible achievements in whole account
        completedAchievements = sum(1 for achieved in achievement if achieved.get("achieved", 0) == 1)  #Counting over actually completed / achieved ones
        if possibleAchievements > 0:
            completion_percentage += (completedAchievements / possibleAchievements) * 100 #Heres the formula used
            valid_games += 1 

        total_possible_achievements += possibleAchievements #just adding possible achivements to total

    avg_percentage = (completion_percentage / valid_games) if valid_games > 0 else 0 #If there arent any valid games it'll just return 0 instead
    return avg_percentage, total_possible_achievements  # return average percentage and total possible achievements; one is a percentage and the other an integer

def accountValue(requestString):
    #Gets list of games, then gets each games price from steam store 
    response = requests.get(requestString)
    dictionary = response.json()
    total_value = 0

    if "response" in dictionary and "games" in dictionary["response"]:
        for game in dictionary["response"]["games"]:
            appId = game.get ("appid")

            if not appId: #Skip if the appId is missing; theres probably better methods of implementation
                continue

            storeUrl = f"https://store.steampowered.com/api/appdetails?appids={appId}&cc=us" #querying steam store (per app ID)
            storeResponse = requests.get(storeUrl)
            storeData = storeResponse.json()

            appData = storeData.get(str(appId), {}) #access nested data in the appId
            if appData.get("success") and "data" in appData:
                price_data = appData["data"].get("price_overview") #getting the price data
                if price_data:
                    price = price_data.get("final", 0)
                    total_value += price / 100  # converting to dollars; default is cents (delete /100 if you want)

    return total_value 

def checkForNumber(text):
    #Checks for if the input is a number between 0 and 9
    if text == "1" or text == "2" or text == "3" or text == "4" or text == "5" or text == "6" or text == "7" or text == "8" or text == "9" or text == "0":
        return True
    else:
        return False

def menu():
    print("1. Number of friends")
    print("2. List friends timestamps")
    print("3. Number of bans")
    print("4. Currently VAC banned")
    print("5. Account age")
    print("6. Number of games")
    print("7. Total Playtime (past 2 weeks)")
    print("8. Total Playtime (across all games on account)")
    print("9. Average achievement completion percentage")
    print("10. Account value ($) (Games)")

def main():
    tempString = "0"
    while checkForNumber(tempString):
        # Asks user to input a steamID
        #steamId = input("Please enter a steam userId ")
        steamId = "76561198880465660" # My own steamID can be used if you can't be bothered finding another
        # if you want to get total playtime make sure this ID is one that has game details public 

        menu()
        tempString = input("Pick a nummber: ")
        # requestType is the first part of the link which differs depending on which value you get
        # requestString is the requestType, steamKey and SteamId put together to form the full request 
        if tempString == "1":
            requestType = "https://api.steampowered.com/ISteamUser/GetFriendList/v1/?key="
            requestString = requestType + steamKey + "&steamid=" + steamId
            print(friendTotal(requestString))
        elif tempString == "2":
            requestType = "https://api.steampowered.com/ISteamUser/GetFriendList/v1/?key="
            requestString = requestType + steamKey + "&steamid=" + steamId
            print(friendTime(requestString))
        elif tempString == "3":
            requestType = "https://api.steampowered.com/ISteamUser/GetPlayerBans/v1/?key="
            requestString = requestType + steamKey + "&steamids=" + steamId
            print(getBanNumber(requestString))
        elif tempString == "4":
            requestType = "https://api.steampowered.com/ISteamUser/GetPlayerBans/v1/?key="
            requestString = requestType + steamKey + "&steamids=" + steamId
            print(currentlyVACBanned(requestString))
        elif tempString == "5":
            requestType = "https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/?key="
            requestString = requestType + steamKey + "&steamids=" + steamId
            print(accountAge(requestString))
        elif tempString == "6":
            requestType = "https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/?key="
            requestString = requestType + steamKey + "&steamid=" + steamId + "&include_played_free_games=true"
            print(numberOfGames(requestString))
        elif tempString == "7":
            requestType = "https://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v1/?key="
            requestString = requestType + steamKey + "&steamid=" + steamId
            print(recentPlayTime(requestString))
        elif tempString == "8":
            requestType = "https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/?key="
            requestString = requestType + steamKey + "&steamid=" + steamId + "&include_played_free_games=true"
            print(totalPlayTime(requestString))
        elif tempString == "9":
            requestType = "https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/?key="
            requestString = requestType + steamKey + "&steamid=" + steamId + "&include_played_free_games=true"
            print(*achievementCompletion(steamId, requestString))
        elif tempString == "10":
            requestType = "https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/?key="
            requestString = requestType + steamKey + "&steamid=" + steamId + "&include_played_free_games=true"
            print(accountValue(requestString))

main()