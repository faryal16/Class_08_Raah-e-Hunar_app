class TrainingProgram:
    @staticmethod
    def get_programs(user):
        skill_program_map = {
            "computer": ["Freelancing Basics", "Digital Literacy"],
            "programming": ["Python Basics", "Web Development"],
            "teaching": ["Classroom Management", "Early Childhood Education"],
            "typing": ["Office Assistant Training"],
            "sewing": ["Advanced Sewing", "Fashion Design"],
            "handicraft": ["Handicraft Business Skills"],
            "farming": ["Modern Farming Techniques"],
            "cooking": ["Catering Services"],
            "driving": ["Driving License Course"],
            "repairing": ["Mobile Repair", "Electronics Repair"]
        }

        user_skills = [skill.lower() for skill in user.skills]
        recommended = []

        for skill in user_skills:
            programs = skill_program_map.get(skill, [])
            recommended.extend(programs)

        return recommended if recommended else ["Basic Skills Training", "Entrepreneurship 101"]
