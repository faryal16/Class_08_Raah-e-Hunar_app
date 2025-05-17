class UserProfile:
    def __init__(self, skills):
       
        self.skills = [skill.strip().lower() for skill in skills]