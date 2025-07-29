import json
import os
import datetime

class MemoryManager:
    def __init__(self, path="memory/user_profile.json"):
        self.path = path
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        if not os.path.exists(path):
            self.data = {
                "feedback": [], 
                "problems": [], 
                "weaknesses": ["recursion"],
                "difficulty_feedback": [],  # Track when problems are too hard/easy
                "problem_attempts": 0
            }
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
        # Ensure all required keys exist (for backward compatibility)
        if "problem_attempts" not in self.data:
            self.data["problem_attempts"] = 0
            
        self.data["problems"].append(problem)
        self.data["problem_attempts"] = self.data.get("problem_attempts", 0) + 1
        self._save()

    def log_feedback(self, feedback: str):
        # Ensure all required keys exist (for backward compatibility)
        if "difficulty_feedback" not in self.data:
            self.data["difficulty_feedback"] = []
        if "problem_attempts" not in self.data:
            self.data["problem_attempts"] = 0
            
        self.data["feedback"].append({
            "feedback": feedback,
            "timestamp": str(datetime.datetime.now())
        })
        
        # Analyze feedback for patterns
        if "too hard" in feedback.lower():
            self.data["difficulty_feedback"].append({
                "type": "too_hard",
                "timestamp": str(datetime.datetime.now())
            })
            
        if "recursion" in feedback.lower():
            self.data["weaknesses"].append("recursion")
        if "array" in feedback.lower() and "difficult" in feedback.lower():
            self.data["weaknesses"].append("arrays")
        if "dynamic programming" in feedback.lower():
            self.data["weaknesses"].append("dynamic_programming")
            
        self._save()
        
    def get_difficulty_history(self):
        """Get history of difficulty feedback"""
        return self.data.get("difficulty_feedback", [])
        
    def get_stats(self):
        """Get user statistics"""
        return {
            "total_problems": len(self.data.get("problems", [])),
            "total_feedback": len(self.data.get("feedback", [])),
            "too_hard_count": len([f for f in self.data.get("difficulty_feedback", []) if f.get("type") == "too_hard"]),
            "weaknesses": self.get_weaknesses()
        }