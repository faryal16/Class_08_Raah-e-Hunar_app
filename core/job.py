class JobOpportunity:
    @staticmethod
    def match_jobs(user):
        job_map = {
            "typing": ["Remote Typist", "Data Entry Clerk"],
            "handicraft": ["Craft Seller", "Market Vendor"],
            "computer": ["Customer Support Assistant", "Online Seller"],
            "programming": ["Junior Developer", "Tech Support"],
            "teaching": ["Tutor", "Online Educator"],
            "sewing": ["Tailor Assistant", "Boutique Worker"],
            "farming": ["Farm Assistant", "Warehouse Helper"],
            "cooking": ["Kitchen Helper", "Canteen Staff"],
            "driving": ["Delivery Driver", "Auto Rickshaw Driver"],
            "repairing": ["Electronics Assistant", "Mechanic Trainee"]
        }

        user_skills = [skill.lower() for skill in user.skills]
        matches = []

        for skill in user_skills:
            if skill in job_map:
                matches.extend(job_map[skill])

        return list(set(matches)) if matches else ["Helper", "Apprentice"]
