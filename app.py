from fastapi import FastAPI
from fastapi.responses import FileResponse

from main import Game

game = Game(5, 3)
app = FastAPI()


@app.get("/")
async def get_ui():
    return FileResponse("index.html")


@app.get("/styles.css")
async def get_styles():
    return FileResponse("styles.css")


@app.get("/script.js")
async def get_script():
    return FileResponse("script.js")


@app.post("/new_game")
async def new_game(troops, fields):
    global game
    game = Game(troops, fields)


@app.get("/solve_blotto")
async def solve_blotto():
    return game.solve_blotto()
