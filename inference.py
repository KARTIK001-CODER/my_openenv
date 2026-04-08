import os
import json
import re
from openai import OpenAI
from env.environment import MeetingEnv
from tasks.tasks import TASKS

API_BASE_URL = os.getenv("API_BASE_URL")
MODEL_NAME = os.getenv("MODEL_NAME")
HF_TOKEN = os.getenv("HF_TOKEN")

if not HF_TOKEN:
    raise ValueError("HF_TOKEN environment variable is not set.")

client = OpenAI(base_url=API_BASE_URL, api_key=HF_TOKEN)

def get_action_from_llm(prompt: str) -> dict:
    fallback_action = {
        "summary": "Processing failure.",
        "action_items": []
    }
    
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        
        content = response.choices[0].message.content
        if not content:
            return fallback_action
        
        json_match = re.search(r"(\{.*\})", content, re.DOTALL)
        if json_match:
            content = json_match.group(1)
        
        return json.loads(content)
        
    except Exception:
        return fallback_action

def run_evaluation():
    print("[START]")
    total_reward = 0.0
    
    for i in range(len(TASKS)):
        env = MeetingEnv(task_idx=i)
        result = env.reset()
        observation = result["observation"]
        
        prompt = f"Process meeting notes:\n{observation['meeting_notes']}\nReturn JSON: summary (str), action_items (list of {{task: str, priority: str}})."
        
        action = get_action_from_llm(prompt)
        
        print("[STEP]")
        result = env.step(action)
        total_reward += result["reward"]
        
    final_score = total_reward / len(TASKS)
    print(f"Final Intelligence Score: {final_score:.2f}")
    print("[END]")

if __name__ == "__main__":
    run_evaluation()
