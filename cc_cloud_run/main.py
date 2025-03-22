from fastapi import FastAPI, Form, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from google.cloud import firestore
from typing import Annotated
import datetime

app = FastAPI()

# mount static files
app.mount("/static", StaticFiles(directory="/app/static"), name="static")
templates = Jinja2Templates(directory="/app/template")

# init firestore client
db = firestore.Client()
votes_collection = db.collection("votes")


@app.get("/")
async def read_root(request: Request):


    tabs_count = 0
    space_count = 0
    recent_votes = []

    votes = votes_collection.stream()

    for vote in votes:
        recent_votes.append(vote)
        entry = vote.to_dict()
        if entry.get("team") == "TABS":
            tabs_count += 1
        elif entry.get("team") == "TABS":
            space_count += 1
            
     # ====================================
    # ++++ START CODE HERE ++++
    # ====================================

    # stream all votes; count tabs / spaces votes, and get recent votes

    # ====================================
    # ++++ STOP CODE ++++
    # ====================================
    return templates.TemplateResponse("index.html", {
        "request": request,
        "tabs_count": tabs_count,
        "spaces_count": space_count,
        "recent_votes": recent_votes
    })


@app.post("/")
async def create_vote(team: Annotated[str, Form()]):
    if team not in ["TABS", "SPACES"]:
        raise HTTPException(status_code=400, detail="Invalid vote")

    # ====================================
    # ++++ START CODE HERE ++++
    # ====================================  

    # create a new vote document in firestore
    votes_collection.add({
    "team": team,
    "time_cast": datetime.datetime.utcnow().isoformat()
    })
    return {"detail": "Vote recorded!"}

    # ====================================
    # ++++ STOP CODE ++++
    # ====================================
