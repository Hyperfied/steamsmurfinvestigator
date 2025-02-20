import requests

key = "APIKEY"

def friendTotal(requestString):
    x = requests.get(requestString)
    tally = 1
    s = x.text
    for i in range(len(s)):
        if s[i] == ",":
            tally = tally + 1
    return int(tally /3)

def friendTime(requestString):
    x = requests.get(requestString)
    text = x.text
    listOfTime = []
    tempstring = ""
    tempnum = 0
    for j in range(len(text)):
        j = tempnum
        if tempnum > len(text) -12:
            break
        i = lookForString(text, "friend_since", j)
        tempstring = ""
        for y in range(i + 2, i+12):
            tempstring = tempstring + text[y]
        listOfTime.append(tempstring)
        tempnum = i + 12

    return listOfTime


def lookForString(text, target, start = 0):
    for i in range(start, len(text)) :
        tempstring = ""
        for j in range(i,i + len(target)):
            tempstring = tempstring + text[j]
        if tempstring == target:
            return i + len(target)
            

def getBanNumber(requestString):
    x = requests.get(requestString)
    text = x.text
    tempstring = ""
    i = lookForString(text, "NumberOfGameBans")
    for y in range(i + 2, i + 4 ):
        if checkForNumber(text[y]):
            tempstring = tempstring + text[y]

    return tempstring

def currentlyBanned(requestString):
    x = requests.get(requestString)
    text = x.text
    tempstring = ""
    i = lookForString(text, "CommunityBanned")
    for y in range(i + 2, i + 6 ):
        tempstring = tempstring + text[y]
    if tempstring == "true":
        return "true"
    else:
        return "false"

def checkForNumber(text):
    if text == "1" or text == "2" or text == "3" or text == "4" or text == "5" or text == "6" or text == "7" or text == "8" or text == "9" or text == "0":
        return True
    else:
        return False

def menu():
    print("1. Number of friends")
    print("2. List friends timestamps")
    print("3. Number of bans")


def main():

    

    tempString = "0"
    while checkForNumber(tempString):
        steamId = input("Please enter a steam userId ")
        #steamId = "76561198880465660"

        menu()
        tempString = input("Pick a nummber: ")

        if tempString == "1":
            requestType = "https://api.steampowered.com/ISteamUser/GetFriendList/v1/?key="
            requestString = requestType + key + "&steamid=" + steamId
            print(friendTotal(requestString))
        elif tempString == "2":
            requestType = "https://api.steampowered.com/ISteamUser/GetFriendList/v1/?key="
            requestString = requestType + key + "&steamid=" + steamId
            print(friendTime(requestString))
        elif tempString == "3":
            requestType = "https://api.steampowered.com/ISteamUser/GetPlayerBans/v1/?key="
            requestString = requestType + key + "&steamids=" + steamId
            print(getBanNumber(requestString))
        elif tempString == "4":
            requestType = "https://api.steampowered.com/ISteamUser/GetPlayerBans/v1/?key="
            requestString = requestType + key + "&steamids=" + steamId
            print(currentlyBanned(requestString))
            


main()