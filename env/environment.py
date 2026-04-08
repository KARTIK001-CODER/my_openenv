from typing import Dict, Any, List, Tuple
from tasks.tasks import TASKS, Task
from grader.grader import compute_reward, generate_feedback

class MeetingEnv:
    def __init__(self, task_idx: int = 0):
        self.task: Task = TASKS[task_idx]
        self.meeting_notes = self.task.meeting_notes
        self.current_summary = ""
        self.action_items = []
        self.feedback = ""
        self.expected_count = self.task.expected_action_items_count
        self.done = False

    def reset(self) -> Dict[str, Any]:
        self.current_summary = ""
        self.action_items = []
        self.feedback = "Initialized."
        self.done = False
        return {"observation": self.state()}

    def step(self, action: Dict[str, Any]) -> Dict[str, Any]:
        if self.done:
            return {
                "observation": self.state(),
                "reward": 0.0,
                "done": True,
                "info": {}
            }

        self.current_summary = action.get("summary", "")
        self.action_items = action.get("action_items", [])
        
        reward = compute_reward(
            self.current_summary, 
            self.action_items, 
            self.expected_count
        )
        
        final_reward = min(max(float(reward), 0.0), 1.0)
        self.feedback = generate_feedback(
            self.current_summary, 
            self.action_items, 
            self.expected_count
        )
        self.done = True
        
        return {
            "observation": self.state(),
            "reward": final_reward,
            "done": self.done,
            "info": {}
        }

    def state(self) -> Dict[str, Any]:
        return {
            "meeting_notes": self.meeting_notes,
            "current_summary": self.current_summary,
            "action_items": self.action_items,
            "feedback": self.feedback
        }
