import streamlit as st
from core.user import UserProfile
from core.advisor import CareerAdvisor
from core.training import TrainingProgram
from core.job import JobOpportunity
from core.feedback import FeedbackSystem
from core.jobsearch import JobSearcher

job_searcher = JobSearcher()
# Load feedback only once on app start
if "feedback_loaded" not in st.session_state:
    FeedbackSystem.load_feedback()
    st.session_state.feedback_loaded = True

# Setup
st.set_page_config(page_title="Raah-e-Hunar", page_icon="✨", layout="wide")

# Sidebar navigation
st.sidebar.title("📌 Raah-e-Hunar")
page = st.sidebar.selectbox("📂 Go to", [
    "🏠 Home",
    "🎯 Career Center",
    "🌐 Search Online Jobs",
    "ℹ️ About",
    "💬 Feedback"
])

# Common skill list
skill_options = [
    "Teaching", "Programming", "Typing", "Sewing", "Computer", "Handicraft",
    "Farming", "Cooking", "Driving", "Repairing"
]

# Home
if page == "🏠 Home":
    st.title("✨ Welcome to Raah-e-Hunar")

    if "username" not in st.session_state:
        st.session_state.username = ""

    name_input = st.text_input("👋 What's your name?", value=st.session_state.username)

    if name_input:
        st.session_state.username = name_input
        st.markdown(f"### 👋 Hello, **{name_input}**!")
    st.markdown("""
    ### Empowering Rural Talent 💪

    **Raah-e-Hunar** is here to support **youth from villages and small towns** by offering:
    - 🧭 Career guidance tailored to your background
    - 🧑‍🏫 Training programs to upskill yourself
    - 💼 Job opportunities — local and online
    - 🌐 Easy job search using keywords

    Use the sidebar 👈 to explore each feature!
    """)


# Career Advice
elif page == "🎯 Career Center":
    st.header("🧠 Career Center")
    with st.form("career_form"):
        name = st.text_input("Name")
        age = st.number_input("Age", 10, 60)
        education = st.selectbox("Education Level", ["None", "Primary", "High School", "College", "Other"])
        skills = st.multiselect("Select your current skills", skill_options)
        submit = st.form_submit_button("Submit")

    if submit:
        user = UserProfile(name, age, education, skills)
        st.session_state.user = user

    user = st.session_state.get("user")
    if user:
         # Display the user's name dynamically in the header for career recommendations
        st.subheader(f"🎯 {user.name}, best career recommendations for your skills are:")
        st.subheader("📌 Career Recommendations")
        advisor = CareerAdvisor()
        for r in advisor.recommend(user):
            st.markdown(f"- {r}")

        st.subheader("📚 Suggested Training Programs")
        for t in TrainingProgram.get_programs(user):
            st.markdown(f"- {t}")

        st.subheader("💼 Matching Job Opportunities")
        for j in JobOpportunity.match_jobs(user):
            st.markdown(f"- {j}")


elif page == "ℹ️ About":
    st.header("🌟 About Raah-e-Hunar!")
    st.markdown("""

    Raah-e-Hunar is a community-focused platform designed to **empower rural youth** by helping them connect with essential career-building resources and opportunities.

    ### 🎯 Our Mission
    To **bridge the skill gap** in underserved and rural areas by offering easy access to:
    - 🧭 **Career Guidance** – Personalized recommendations based on age, education, and skills.
    - 🧑‍🏫 **Training Programs** – Curated learning paths to help build job-ready skills.
    - 💼 **Job Opportunities** – Local and remote job listings based on your profile.
    - 🌐 **Online Job Search** – Search for global remote jobs from trusted sources.

    ### 🤝 Who Is It For?
    - Young individuals in **villages or small towns**
    - People with **limited access to career counseling**
    - Learners who want to **upskill and get hired**

    ### 🚀 Why Use Raah-e-Hunar?
    ✅ Simple and user-friendly interface  
    ✅ Personalized recommendations  
    ✅ Real-time access to job listings  
    ✅ Completely free to use  

    ---

    💡 Whether you're just starting your career journey or looking for new opportunities, **Raah-e-Hunar is your companion for growth**.

    _Together, let’s build a skilled and self-reliant future!_ 💪
    """)


# Feedback
elif page == "💬 Feedback":
    # Load feedback once
    
    st.header("📝 Your Feedback")

    name = st.text_input("👤 Your Name")
    feedback = st.text_area("💬 What do you think of Raah-e-Hunar?")

    if st.button("Submit Feedback"):
        if name and feedback:
            FeedbackSystem.store_feedback(name, feedback)
            st.success("✅ Thanks for your feedback!")
        else:
            st.warning("⚠️ Please fill in both name and feedback.")

    st.subheader("💬 Recent Feedback")

    recent_feedback = FeedbackSystem.get_recent_feedback()  # Add this method or fallback to get_feedback()

    if recent_feedback:
        for entry in recent_feedback:
            st.markdown(f"**👤 {entry['user']}** says:\n> {entry['feedback']}")
    else:
        st.info("No feedback yet. Be the first to share!")


# Search Online Jobs (API placeholder)
elif page == "🌐 Search Online Jobs":
    st.header("🌐 Search Online Jobs")

    # Let user pick from popular categories
    categories = [
        "All", "Python", "JavaScript", "Next.js", "React", "Design", "Marketing", "Teaching", "Remote", "AI", "Data"
    ]

    selected_category = st.selectbox("Choose a job category", categories)

    # Search bar for keyword (optional)
    query = st.text_input("🔍 Enter keyword (e.g., 'developer', 'UI', 'teacher')")

    # Combine category + keyword
    if selected_category != "All":
        search_term = selected_category
        if query:
            search_term += f" {query}"
    else:
        search_term = query

    if search_term:
        with st.spinner("🔎 Searching for jobs..."):
            results = job_searcher.search_by_keyword(search_term)

        if results:
            for job in results:
                st.subheader(job.get("position", "Unknown Position"))
                st.markdown(f"**🏢 Company:** {job.get('company', 'Unknown')}")
                st.markdown(f"**🌍 Location:** {job.get('location', 'Remote')}")
                st.markdown(f"[📝 Apply Here]({job.get('url', '#')})")
                st.markdown("---")
        else:
            st.info("No jobs found for this search.")
    else:
        st.info("Please enter a keyword or select a category to begin.")

st.markdown("<hr>", unsafe_allow_html=True)
st.markdown(
    "<div style='text-align: center;'>✨ Made with ❤️ for rural youth by <a href='https://www.github.com/faryal16' target='_blank'>Code_With_Fairy</a></div>",
    unsafe_allow_html=True
)


