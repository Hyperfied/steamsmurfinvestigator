import requests
import json

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


def main():
    tempString = "0"
    while checkForNumber(tempString):
        # Asks user to input a steamID
        steamId = input("Please enter a steam userId ")
        #steamId = "76561198880465660" # My own steamID can be used if you can't be bothered finding another

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
            


main()