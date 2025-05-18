
import requests


class Workshop:
    # Skill to workshop mapping with title and price (0 = free)
    workshop_data = {
        "computer": [
            {"title": "Intro to Freelancing", "price": 0},
            {"title": "Digital Literacy Bootcamp", "price": 999}
        ],
        "programming": [
            {"title": "Build Your First Website", "price": 0},
            {"title": "Python Crash Course", "price": 1499},
        ],
        "teaching": [
            {"title": "Early Childhood Development", "price": 0},
            {"title": "Effective Teaching Methods", "price": 799},
        ],
        "typing": [
            {"title": "Typing Speed Mastery", "price": 0}
        ],
        "sewing": [
            {"title": "Fashion Startup Basics", "price": 0},
            {"title": "Advanced Sewing Workshop", "price": 1299},
        ],
        "handicraft": [
            {"title": "Handmade Crafts Business", "price": 999}
        ],
        "farming": [
            {"title": "Sustainable Farming Techniques", "price": 499}
        ],
        "cooking": [
            {"title": "Catering Business Workshop", "price": 0}
        ],
        "driving": [
            {"title": "Driving License Preparation", "price": 1499}
        ],
        "repairing": [
            {"title": "Electronics Repair 101", "price": 0},
            {"title": "Mobile Repair Hands-on", "price": 999},
        ]
    }


    # Mock testimonials
    testimonials = [
        {"name": "Ayesha Khan", "career": "Digital Marketing", "story": "After completing the Digital Literacy Bootcamp, Ayesha landed a great remote job."},
        {"name": "Bilal Ahmed", "career": "Programming", "story": "The Python Crash Course helped Bilal switch careers to software development successfully."},
        {"name": "Sara Malik", "career": "Teaching", "story": "Sara improved her teaching skills with our Effective Teaching Methods workshop and got promoted."}
    ]
    def __init__(self, user):
        if user is None:
            raise ValueError("User object cannot be None.")
        self.user = user
        # Safe get skills list or empty list
        # self.recommended_workshops = 
        self.skills = getattr(user, "skills", [])
        self.email = getattr(user, "email", None)
        if not self.email:
            # Try nested attribute or raise error
            self.email = getattr(getattr(user, "account", None), "email", None)
        if not self.skills:
            print("Warning: User skills not found.")
        if not self.email:
            print("Warning: User email not found.")

    def recommend(self):
        recommended_workshops = []
        user_skills = [skill.lower() for skill in self.user.skills]
        for skill in user_skills:
            recommended_workshops.extend(self.workshop_data.get(skill, []))
        return recommended_workshops if recommended_workshops else [{"title": "Basic Skills Workshop", "price": 0}]

    def generate_stripe_url(self, workshop_title):
        matching = next((w for w in self.recommend() if w["title"] == workshop_title), None)

        if not matching:
            print(f"⚠️ Workshop titled '{workshop_title}' not found.")
            return None

        try:
            response = requests.post(
                "https://backend-api-vert-seven.vercel.app/create-checkout-session/",
                json={
                    "title": workshop_title,
                    "price": matching["price"],
                    "email": self.email,
                    "success_url": "https://class08-raah-e-hunar-app.streamlit.app/?paid=success",
                    "cancel_url": "https://class08-raah-e-hunar-app.streamlit.app/?paid=cancel"
                }
            )
            print(f"Response: {response.text}")

            if response.status_code == 200:
                checkout_url = response.json().get("checkout_url")
                if checkout_url:
                    return checkout_url
                else:
                    print("⚠️ 'checkout_url' not found in response JSON.")
                    return None
            else:
                print(f"❌ Stripe error: {response.status_code} - {response.text}")
                return None

        except Exception as e:
            print(f"⚠️ Error creating Stripe session: {e}")
            return None

 
    def get_testimonials(self):
        """Return mock testimonials."""
        return self.testimonials