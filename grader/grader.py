from typing import List, Dict, Any

def score_summary(summary: str) -> float:
    if not isinstance(summary, str) or len(summary.strip()) < 20:
        return 0.0
    if len(summary.strip()) > 100:
        return 0.3
    return 0.1

def score_action_items(action_items: Any, expected_count: int) -> float:
    if not isinstance(action_items, list) or not action_items:
        return 0.0
    score = 0.1
    actual_count = len(action_items)
    progress = min(actual_count / expected_count, 1.0)
    score += (progress * 0.3)
    return score

def score_quality_and_priorities(action_items: Any) -> float:
    if not isinstance(action_items, list) or not action_items:
        return 0.0
    score = 0.0
    valid_priorities = {"High", "Medium", "Low"}
    all_priorities_valid = True
    all_descriptive = True
    for item in action_items:
        if not isinstance(item, dict): return 0.0
        if item.get("priority") not in valid_priorities: all_priorities_valid = False
        if not isinstance(item.get("task"), str) or len(item.get("task", "").strip()) < 10: all_descriptive = False
    if all_priorities_valid: score += 0.2
    if all_descriptive: score += 0.1
    return score

def compute_reward(summary: str, action_items: Any, expected_count: int) -> float:
    s1 = score_summary(summary)
    s2 = score_action_items(action_items, expected_count)
    s3 = score_quality_and_priorities(action_items)
    return min(max(float(s1 + s2 + s3), 0.0), 1.0)

def generate_feedback(summary: str, action_items: Any, expected_count: int) -> str:
    messages = []
    if not isinstance(summary, str) or len(summary.strip()) < 20: messages.append("Summary short.")
    if not isinstance(action_items, list): messages.append("Items not list.")
    else:
        if len(action_items) < expected_count: messages.append("Missing items.")
    return " ".join(messages)
