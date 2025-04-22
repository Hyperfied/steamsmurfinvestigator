from fastapi import FastAPI
from starlette.responses import FileResponse
import server.StatsProcessor as StatsProcessor
import server.smurfcalculation as smurfcalculation

app = FastAPI()

@app.get("/")
async def get_page():
    return FileResponse("./client/index.html")

@app.get("/style.css")
async def get_style():
    return FileResponse("./client/style.css")

@app.get("/script.js")
async def get_script():
    return FileResponse("./client/script.js")

@app.get("/profile/{steamid}")
async def profile(steamid: str):
    
    summary = await StatsProcessor.getPlayerSummary(steamid)
    
    requestString = f"https://api.steampowered.com/ISteamUser/GetFriendList/v1/?key={StatsProcessor.steamKey}&steamid={steamid}"
    ageRequest = f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/?key={StatsProcessor.steamKey}&steamids={steamid}"
    
    requestBanString = f"https://api.steampowered.com/ISteamUser/GetPlayerBans/v1/?key={StatsProcessor.steamKey}&steamids={steamid}"
    
    recentRequest = f"https://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v1/?key={StatsProcessor.steamKey}&steamid={steamid}"
    gamesRequest = f"https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/?key={StatsProcessor.steamKey}&steamid={steamid}&include_played_free_games=true"
    
    friendTotal = await StatsProcessor.friendTotal(requestString)
    friendTimestamps = await StatsProcessor.friendTime(requestString)
    accountAgeSeconds = await StatsProcessor.accountAge(ageRequest)
    
    banNumber = await StatsProcessor.getBanNumber(requestBanString)
    currentlyVACBanned = await StatsProcessor.currentlyVACBanned(requestBanString)
    
    recentPlayTimeHours = await StatsProcessor.recentPlayTime(recentRequest)
    numberOfGames = await StatsProcessor.numberOfGames(gamesRequest)
    
    totalPlaytimeHours, averagePlaytimeRecentHours = await StatsProcessor.totalPlayTime(gamesRequest)
    achievementPercentage, totalPossibleAchievements = await StatsProcessor.achievementCompletion(steamid, gamesRequest)
    
    accountValue = await StatsProcessor.accountValue(gamesRequest)
    
    response = {
        
        "personaName": StatsProcessor.personaName(summary),
        "realName": StatsProcessor.realName(summary),
        "avatar": StatsProcessor.profilePictureLink(summary),
        "avatarFull": StatsProcessor.profilePictureLinkFull(summary),
        "avatarMedium": StatsProcessor.profilePictureLinkMedium(summary),
        
        "friendTotal": friendTotal,
        "friendTimestamps": friendTimestamps,
        "accountAgeSeconds": accountAgeSeconds,
        
        "banNumber": banNumber,
        "currentlyVACBanned": currentlyVACBanned,
        
        "recentPlayTimeHours": recentPlayTimeHours,
        "numberOfGames": numberOfGames,
        "totalPlayTimeHours": totalPlaytimeHours,
        "averagePlaytimeRecentHours": averagePlaytimeRecentHours,
        "achievementCompletionPercentage": achievementPercentage,
        "totalPossibleAchievements": totalPossibleAchievements,
        "accountValue": accountValue
                
    }
    
    return response



@app.get("/smurf/accountAge/{days}")
async def api_score_account_age(days: float):
    return smurfcalculation.score_account_age(days)

@app.get("/smurf/accountGames/{numOfGames}")
async def api_score_account_games(numOfGames: int):
    return smurfcalculation.score_account_games(numOfGames)

@app.get("/smurf/accountBans/{numOfBans}")
async def api_score_account_bans(numOfBans: int):
    return smurfcalculation.score_account_bans(numOfBans)

@app.get("/smurf/totalPlaytime/{hours}")
async def api_score_total_playtime(hours: float):
    return smurfcalculation.score_total_playtime(hours)

@app.get("/smurf/last2Weeks/{last2Weeks}/{average2Weeks}")
async def api_score_last2Weeks(last2Weeks: float, average2Weeks: float):
    return smurfcalculation.score_last_2_weeks_versus_average(last2Weeks, average2Weeks)

@app.get("/smurf/accountValue/{value}")
async def api_score_account_value(value: float):
    return smurfcalculation.score_account_value(value)

@app.get("/smurf/accountFriends/{numOfFriends}")
async def api_score_account_friends(numOfFriends: int):
    return smurfcalculation.score_account_friends(numOfFriends)

@app.get("/smurf/achievementPercentage/{completed}/{total}")
async def api_score_achievement_percentage(completed: int, total: int):
    return smurfcalculation.score_average_achievement_percentage(completed, total)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)