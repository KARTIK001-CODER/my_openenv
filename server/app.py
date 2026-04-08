from fastapi import FastAPI, Body
from env.environment import MeetingEnv

app = FastAPI()
env = MeetingEnv()

@app.post("/reset")
async def reset():
    return env.reset()

@app.post("/step")
async def step(action: dict = Body(...)):
    return env.step(action)

def main():
    import uvicorn
    uvicorn.run("server.app:app", host="0.0.0.0", port=7860)

if __name__ == "__main__":
    main()
