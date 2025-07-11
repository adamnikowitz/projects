import json
import os

class MemoryManager:
    def __init__(self, path="memory/user_profile.json"):
        self.path = path
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        if not os.path.exists(path):
            self.data = {"feedback": [], "problems": [], "weaknesses": ["recursion"]}
            self._save()
        else:
            self._load()

    def _load(self):
        with open(self.path, "r") as f:
            self.data = json.load(f)

    def _save(self):
        with open(self.path, "w") as f:
            json.dump(self.data, f, indent=2)

    def get_weaknesses(self):
        return list(set(self.data["weaknesses"]))

    def log_problem(self, problem: str):
        self.data["problems"].append(problem)
        self._save()

    def log_feedback(self, feedback: str):
        self.data["feedback"].append(feedback)
        if "recursion" in feedback.lower():
            self.data["weaknesses"].append("recursion")
        self._save()
