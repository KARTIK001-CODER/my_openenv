from dataclasses import dataclass
from typing import List

@dataclass
class Task:
    name: str
    meeting_notes: str
    expected_action_items_count: int

TASKS = [
    Task(
        name="EASY",
        meeting_notes="""
        [10:00 AM] Alex: Hi team, we need to finalize the quarterly budget by Friday.
        [10:01 AM] Sarah: I'll start working on the Excel sheet right after this call.
        [10:02 AM] Alex: Perfect, thanks Sarah.
        """,
        expected_action_items_count=1
    ),
    Task(
        name="MEDIUM",
        meeting_notes="""
        Project Alpha Sync:
        Mike: The UI redesign is 80% done. I need to fix the responsive layout on mobile.
        Jen: Okay. Also, we need to schedule the user testing sessions for next week.
        Jen: Mike, can you handle the layout? I'll take care of recruitment for testing.
        Mike: Sounds like a plan. 
        Jen: Oh, and don't forget we need to update the client on the delay.
        Jen: I'll send that email today.
        """,
        expected_action_items_count=3
    ),
    Task(
        name="HARD",
        meeting_notes="""
        Transcript: 2024-05-12 Strategic Planning
        
        Sarah: Alright, let's dive in. The churn rate is up 5%. Thoughts?
        Rick: Is that... is that higher than last year?
        Sarah: Yes, Rick. By 2 points.
        Bob: Maybe we should check the onboarding flow? I can run a heat map analysis.
        Sarah: Good idea Bob. Put that on your list for Monday.
        Rick: I think it's the pricing. Hey, did anyone see the game last night?
        Sarah: Focus, Rick. 
        Rick: Sorry! Okay, I’ll prepare a competitive pricing analysis report by Wednesday.
        Bob: Also, the API latency is spiking. 
        Sarah: Is it critical?
        Bob: Not yet, but we should migrate to the new cluster. 
        Sarah: Rick, can you help Bob with the migration doc?
        Rick: Actually, Bob should lead it, but I’ll review the security protocols for the migration.
        Sarah: Fine. Bob, you migration, Rick, you the security review.
        Alice (Interrupting): Wait! We also need to order lunch for the workshop.
        Sarah: Alice, please. Use the Slack channel for that.
        Sarah: One more thing: the board deck needs a refresh. I'll handle that myself.
        Bob: Okay, meeting adjourned. 
        """,
        expected_action_items_count=4
    )
]
