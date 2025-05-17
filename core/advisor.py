class CareerAdvisor:
    def recommend(self, user):
        recommendations = []

        skill_based = {
            "sewing": ["Tailor", "Clothing Designer"],
            "programming": ["Web Developer", "Freelancer"],
            "computer": ["Digital Marketer", "Online Freelancer"],
            "typing": ["Data Entry Operator", "Office Assistant"],
            "teaching": ["Tutor", "Community Instructor"],
            "handicraft": ["Craft Seller", "Handmade Product Designer"],
            "farming": ["Agricultural Worker", "Farm Supervisor"],
            "cooking": ["Caterer", "Chef Assistant"],
            "driving": ["Driver", "Delivery Rider"],
            "repairing": ["Technician", "Mechanic"]
        }

        # Normalize skills to lowercase for comparison
        user_skills = [skill.lower() for skill in user.skills]

        for skill in user_skills:
            if skill in skill_based:
                recommendations.extend(skill_based[skill])


        # Fallback if no matches
        if not recommendations:
            recommendations.extend(["General Labor", "Handicrafts Worker"])

        # Remove duplicates and return
        return list(set(recommendations))
