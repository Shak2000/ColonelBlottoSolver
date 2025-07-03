from fastapi import FastAPI
from fastapi.responses import FileResponse
from main import Game

game = Game(5, 3)  # Initializing with default values
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
async def new_game(troops: int, fields: int): # Add type hints to automatically convert to int
    global game
    game = Game(troops, fields)
    return {"message": "Game initialized successfully"} # Return a success message


@app.get("/solve_blotto")
async def solve_blotto():
    # The solve_blotto method in Game class returns a tuple:
    # (solution_combo, win_prob, draw_prob, lose_prob, min_win_minus_lose_diff_for_solution)
    solution_data = game.solve_blotto()
    return solution_data
