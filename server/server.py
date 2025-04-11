from fastapi import FastAPI
from starlette.responses import FileResponse
import StatsProcessor
import smurfcalculation

app = FastAPI()

@app.get("/")
async def get_page():
    return FileResponse("../client/index.html")

@app.get("/style.css")
async def get_style():
    return FileResponse("../client/style.css")

@app.get("/script.js")
async def get_script():
    return FileResponse("../client/script.js")

@app.get("/profile/{steamid}")
async def profile(steamid: str):
    
    summary = StatsProcessor.getPlayerSummary(steamid)
    
    requestString = f"https://api.steampowered.com/ISteamUser/GetFriendList/v1/?key={StatsProcessor.steamKey}&steamid={steamid}"
    ageRequest = f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/?key={StatsProcessor.steamKey}&steamids={steamid}"
    
    requestBanString = f"https://api.steampowered.com/ISteamUser/GetPlayerBans/v1/?key={StatsProcessor.steamKey}&steamids={steamid}"
    
    recentRequest = f"https://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v1/?key={StatsProcessor.steamKey}&steamid={steamid}"
    gamesRequest = f"https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/?key={StatsProcessor.steamKey}&steamid={steamid}&include_played_free_games=true"
    
    response = {
        
        "personaName": StatsProcessor.personaName(summary),
        "realName": StatsProcessor.realName(summary),
        "avatar": StatsProcessor.profilePictureLink(summary),
        "avatarFull": StatsProcessor.profilePictureLinkFull(summary),
        "avatarMedium": StatsProcessor.profilePictureLinkMedium(summary),
        
        "friendTotal": StatsProcessor.friendTotal(requestString),
        "friendTimestamps": StatsProcessor.friendTime(requestString),
        "accountAgeSeconds": StatsProcessor.accountAge(ageRequest),
        
        "banNumber": StatsProcessor.getBanNumber(requestBanString),
        "currentlyVACBanned": StatsProcessor.currentlyVACBanned(requestBanString),
        
        "recentPlayTimeHours": StatsProcessor.recentPlayTime(recentRequest),
        "numberOfGames": StatsProcessor.numberOfGames(gamesRequest),
        "totalPlayTimeHours": StatsProcessor.totalPlayTime(gamesRequest),
        "achievementCompletionPercentage": StatsProcessor.achievementCompletion(steamid, gamesRequest)
                
    }
    
    return response



# @app.get("/smurf/accountAge/{days}")
# async def api_score_account_age(days: float):
#     return smurfcalculation.score_account_age(days)

# @app.get("/smurf/accountGames/{numOfGames}")
# async def api_score_account_games(numOfGames: int):
#     return smurfcalculation.score_account_games(numOfGames)

# @app.get("/smurf/accountBans/{numOfBans}")
# async def api_score_account_bans(numOfBans: int):
#     return smurfcalculation.score_account_bans(numOfBans)

# @app.get("/smurf/totalPlaytime/{hours}")
# async def api_score_total_playtime(hours: float):
#     return smurfcalculation.score_total_playtime(hours)

# @app.get("/smurf/last2Weeks/{last2Weeks}/{average2Weeks}")
# async def api_score_last2Weeks(last2Weeks: float, average2Weeks: float):
#     return smurfcalculation.score_last_2_weeks_versus_average(last2Weeks, average2Weeks)

# @app.get("/smurf/accountValue/{value}")
# async def api_score_account_value(value: float):
#     return smurfcalculation.score_account_value(value)

# @app.get("/smurf/accountFriends/{numOfFriends}")
# async def api_score_account_friends(numOfFriends: int):
#     return smurfcalculation.score_account_friends(numOfFriends)

# @app.get("/smurf/achievementPercentage/{completed}/{total}")
# async def api_score_achievement_percentage(completed: int, total: int):
#     return smurfcalculation.score_average_achievement_percentage(completed, total)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)