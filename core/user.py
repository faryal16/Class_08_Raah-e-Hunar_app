class UserProfile:
    def __init__(self, name, age, education, skills):
        self.name = name
        self.age = age
        self.education = education
        self.skills = [skill.strip().lower() for skill in skills]