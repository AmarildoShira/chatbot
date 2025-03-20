import json
import difflib

class LearningBot:
    def __init__(self, knowledge_file="PyetjePergjigje.json"):
        self.knowledge_file = knowledge_file
        self.load_knowledge()

    def load_knowledge(self):
        try:
            with open(self.knowledge_file, "r") as file:
                self.knowledge = json.load(file)
                # Normalize keys to lowercase
                self.knowledge = {key.lower(): value for key, value in self.knowledge.items()}
        except (FileNotFoundError, json.JSONDecodeError):
            self.knowledge = {
                "pershendetje!": "Pershendetje! Si mundem te te ndihmoj?",
                "si e ke emrin?": "Une jam Boti inteligjent!",
                "si je?": "Mire faleminderit, ti si je?",
                "cili eshte kryeqyteti i shqiperise?": "Kryeqyteti i Shqiperise eshte Tirana.",
                "sa vjec je?": "Nuk mundem ta llogaris moshen time!"
            }

    def save_knowledge(self):
        with open(self.knowledge_file, "w") as file:
            json.dump(self.knowledge, file, indent=4)

    def find_best_match(self, question):
        matches = difflib.get_close_matches(question, self.knowledge.keys(), n=1, cutoff=0.93)
        return matches[0] if matches else None

    def ask(self, question):
        question_normalized = question.strip().lower()
        best_match = self.find_best_match(question_normalized)
        
        if best_match:
            return {"response": self.knowledge[best_match], "learn": False}
        else:
            return {"response": "Nuk e di pergjigjen. Mund të më mësosh?", "learn": True}

    def learn(self, question, answer):
        question_normalized = question.strip().lower()
        self.knowledge[question_normalized] = answer.strip()
        self.save_knowledge()
        return "Faleminderit! E mesova përgjigjen."
