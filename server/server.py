from fastapi import FastAPI
import StatsProcessor

app = FastAPI()

@app.get("/")
async def hello_world():
    return {"response": "Hello World"}

@app.get("/profile/{steamid}")
async def profile(steamid: str):
    summary = StatsProcessor.getPlayerSummary(steamid)
    response = {
        "personaName": StatsProcessor.personaName(summary),
        "realName": StatsProcessor.realName(summary),
        "avatar": StatsProcessor.profilePictureLink(summary),
        "avatarFull": StatsProcessor.profilePictureLinkFull(summary),
        "avatarMedium": StatsProcessor.profilePictureLinkMedium(summary)
    }
    
    return response
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)