from fastapi import FastAPI
from API.showself import get_player_full_data
from API.rank_api import get_rank, get_group_rank
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Game Stats API")

@app.get("/player/{name}")
def player(name: str):
    return get_player_full_data(name)

@app.get("/rank")
def rank():
    return get_rank()

@app.get("/group-rank")
def group_rank():
    return get_group_rank()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://nevanyalab.com",
        "http://localhost:8000",
        "http://127.0.0.1:8000"
    ],  # 之後可改成你的網域
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)