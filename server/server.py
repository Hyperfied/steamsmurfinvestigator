from fastapi import FastAPI
from starlette.responses import FileResponse
import StatsProcessor

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