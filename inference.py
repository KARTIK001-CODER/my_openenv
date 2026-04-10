import os
import json
import asyncio
import sys
from openai import OpenAI
try:
    from openenv_core import MyEnv
except ImportError:
    MyEnv = None
from env.environment import MeetingEnv
from tasks.tasks import TASKS

API_BASE_URL = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4")
HF_TOKEN = os.getenv("HF_TOKEN", "")
IMAGE_NAME = os.getenv("IMAGE_NAME", "meeting-intel")

client = OpenAI(base_url=API_BASE_URL, api_key=HF_TOKEN)

async def run_evaluation():
    try:
        print("[START]")
        total_reward = 0.0
        max_total_reward = float(len(TASKS)) if len(TASKS) > 0 else 1.0
        
        for i in range(len(TASKS)):
            env = None
            try:
                if MyEnv:
                    env = await MyEnv.from_docker_image(IMAGE_NAME)
                else:
                    env = MeetingEnv(task_idx=i)
            except:
                try:
                    env = MeetingEnv(task_idx=i)
                except:
                    continue

            observation = {"echoed_message": "start"}
            try:
                res = env.reset()
                if asyncio.iscoroutine(res):
                    res = await res
                observation = res.get("observation", observation)
            except:
                pass

            done = False
            steps = 0
            task_reward = 0.0
            
            while not done and steps < 5:
                try:
                    notes = observation.get("meeting_notes", "")
                    prompt = f"Process meeting notes:\n{notes}"
                    completion = client.chat.completions.create(
                        model=MODEL_NAME,
                        messages=[{"role": "user", "content": prompt}]
                    )
                    content = completion.choices[0].message.content
                    if not content:
                        message = '{"summary": "basic summary", "action_items": []}'
                    else:
                        message = content
                except:
                    message = '{"summary": "basic summary", "action_items": []}'

                try:
                    action = json.loads(message)
                except:
                    action = {"summary": "basic summary", "action_items": []}

                print("[STEP]")
                try:
                    res = env.step(action)
                    if asyncio.iscoroutine(res):
                        res = await res
                    task_reward = res.get("reward", 0.0)
                    done = res.get("done", True)
                    observation = res.get("observation", observation)
                except:
                    task_reward = 0.0
                    done = True
                steps += 1
            
            total_reward += task_reward
            try:
                if env and hasattr(env, "close"):
                    res = env.close()
                    if asyncio.iscoroutine(res):
                        await res
            except:
                pass
        
        score = total_reward / max_total_reward
        score = min(max(score, 0.0), 1.0)
        print(f"Final Intelligence Score: {score:.2f}")
        print("[END]")
    except:
        print("[END]")

if __name__ == "__main__":
    try:
        asyncio.run(run_evaluation())
    except:
        pass
    sys.exit(0)
