import json
import os

class FeedbackSystem:
    feedback_store = []

    @classmethod
    def load_feedback(cls):
        if os.path.exists("feedback.json"):
            with open("feedback.json", "r") as f:
                cls.feedback_store = json.load(f)
        else:
            cls.feedback_store = [
                {"user": "Ali", "feedback": "Great app! Very helpful."},
                {"user": "Sana", "feedback": "Loved how easy it was to use SkillBridge."}
            ]
            with open("feedback.json", "w") as f:
                json.dump(cls.feedback_store, f, indent=4)

    @classmethod
    def store_feedback(cls, name, feedback):
        cls.feedback_store.append({"user": name, "feedback": feedback})
        with open("feedback.json", "w") as f:
            json.dump(cls.feedback_store, f, indent=4)

    @classmethod
    def get_feedback(cls):
        return cls.feedback_store

    @classmethod
    def get_recent_feedback(cls, count=5):
        return cls.feedback_store[-count:] if cls.feedback_store else []

    @classmethod
    def display_feedback(cls):
        if cls.feedback_store:
            for i, entry in enumerate(cls.feedback_store, 1):
                print(f"{i}. User: {entry['user']} - Feedback: {entry['feedback']}")
        else:
            print("No feedback yet!")
