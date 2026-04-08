from fastapi import FastAPI, Body
from env.environment import MeetingEnv

app = FastAPI()
env = MeetingEnv()

@app.get("/")
async def root():
    return {"status": "Meeting Intelligence API is running", "endpoints": ["/reset", "/step"]}

@app.post("/reset")
async def reset():
    return env.reset()

@app.post("/step")
async def step(action: dict = Body(...)):
    return env.step(action)
