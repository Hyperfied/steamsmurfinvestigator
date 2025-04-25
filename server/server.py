from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse
import server.StatsProcessor as StatsProcessor
import server.smurfcalculation as smurfcalculation
import time

# FastAPI app instance

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_methods=["GET"],
    allow_origins=["*"]
)

# Static Files

@app.get("/")
async def get_page():
    return FileResponse("./client/index.html")

@app.get("/style.css")
async def get_style():
    return FileResponse("./client/style.css")

@app.get("/script.js")
async def get_script():
    return FileResponse("./client/script.js")

# Profile Endpoints

@app.get("/profile/vanityurl/{vanityurl}")
async def profile_vanityurl(vanityurl: str):
    steamid = await StatsProcessor.tryVanityURL(vanityurl)
    
    response = { "steamid": steamid }
    
    return response

@app.get("/profile/summary/{steamid}")
async def profile_summary(steamid: str):
    summary = await StatsProcessor.getPlayerSummary(steamid)
    
    response = {
        "personaName": StatsProcessor.personaName(summary),
        "realName": StatsProcessor.realName(summary),
        "avatar": StatsProcessor.profilePictureLink(summary),
        "avatarFull": StatsProcessor.profilePictureLinkFull(summary),
        "avatarMedium": StatsProcessor.profilePictureLinkMedium(summary),
        "accountAgeSeconds": StatsProcessor.getAccountAge(summary),
    }
    
    return response

@app.get("/profile/friends/{steamid}")
async def profile_friends(steamid: str):
    length, timestamps = await StatsProcessor.friendTotal(steamid)
    
    response = {
        "friendTotal": length,
        "friendTimestamps": timestamps
    }
    
    return response

@app.get("/profile/bans/{steamid}")
async def profile_bans(steamid: str):
    numberOfBans, currentlyVACBanned = await StatsProcessor.getBans(steamid)
    
    response = {
        "banNumber": numberOfBans,
        "currentlyVACBanned": currentlyVACBanned
    }
    
    return response

@app.get("/profile/recent/{steamid}")
async def profile_recent(steamid: str):
    recentPlaytime, averageRecentPlaytime = await StatsProcessor.getRecentPlaytime(steamid)
    
    response = { "recentPlaytimeHours": recentPlaytime,
                "averageRecentPlaytime":  averageRecentPlaytime }
    
    return response

@app.get("/profile/games/{steamid}")
async def profile_games(steamid: str):
    numOfGames, totalPlayTime, avgAchievementCompletion, totalPossibleAchievements = await StatsProcessor.getGames(steamid)
    
    response = {
        "numberOfGames": numOfGames,
        "totalPlaytimeHours": totalPlayTime,
        "achievementCompletionPercentage": avgAchievementCompletion,
        "totalPossibleAchievements": totalPossibleAchievements
    }
    
    return response

@app.get("/profile/value/{steamid}")
async def profile_value(steamid: str):
    accountValue = await StatsProcessor.getAccountValue(steamid)
    
    response = { "accountValue": accountValue }
    
    return response
    

# Smurf Calculation Endpoints

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