# fimports 
import streamlit as st
from core import workshop_data
from core.authManager import AuthManager
from core.user import UserProfile
from core.advisor import CareerAdvisor
from core.training import TrainingProgram
from core.job import JobOpportunity
from core.feedback import FeedbackSystem
from core.jobsearch import JobSearcher
from core.workshop import Workshop
import os
os.system('pip install httpx')

st.set_page_config(page_title="Raah-e-Hunar", page_icon="✨", layout="wide")

# feedback loading
if "feedback_loaded" not in st.session_state:
    FeedbackSystem.load_feedback()
    st.session_state.feedback_loaded = True


   # Handle Stripe payment redirect
# --- Must be at the very top ---
params = st.query_params
if "payment" in params:
    if params["payment"] == "success":
        if not st.session_state.get("email"):
            # Assume user will be re-logged in on next redirect
            st.info("Verifying login session...")
        else:
            st.title("Enrollment Confirmed")
            st.balloons()
            st.markdown("### ✅ Your workshop enrollment was successful!")
            st.markdown("""
            Thank you for enrolling in the workshop. We’re excited to have you onboard!

            🎓 **Workshop Status:** Confirmed  
            📧 **Confirmation Email:** Sent to your registered email  
            📅 **Workshop Start Date:** You will receive details shortly

            If you have any questions or need assistance, please [contact us](#).
            """)
            if st.button("🏠 Go to Home"):
                st.query_params.clear() 
                st.session_state.page = "🏠 Home"
                st.rerun()
            st.stop()
 

    elif params["payment"] == "cancel":
        st.title("Payment Cancelled")
        st.warning("⚠️ Payment was cancelled. No charges were made.")
        if st.button("🏠 Go to Home"):
            st.set_query_params()  
            if "email" in st.session_state and st.session_state.email:
                st.session_state.page = "🏠 Home"
            else:
                st.session_state.page = None  # or your login page state
            st.rerun()

    
# Auth
auth_manager = AuthManager()
if not st.session_state.get("email"):
    auth_manager.handle_callback()


if not st.session_state.get("email"):
    # Use a tighter ratio to bring image and text closer
    col1, col2 = st.columns([1, 12])

    with col1:
        st.image("assets/logo.png", width=70)  # smaller image to align better
        
    with col2:
        st.markdown("""
            <div style='display: flex; flex-direction: column; justify-content: center; padding-top: 10px; '>
                <div style='font-weight: 700; font-size: 36px; color: #DC143C;'>✨ Raah-e-Hunar Login</div>
                <div style='font-size: 14px; color: #666; margin-bottom: 10px'>Empowering rural youth with skills & careers</div>
            </div>
        """, unsafe_allow_html=True)

    st.info("Please login with Google to continue.")
    auth_manager.show_login_button()
    st.stop()


# Sidebar profile
with st.sidebar:
    profile_html = f"""
    <div style='display: flex; align-items: center; gap: 10px; margin-bottom: 10px;'>
        <img src="{st.session_state.picture}" style="width: 40px; height: 40px; border-radius: 50%;" />
        <div>
            <div style='font-weight: bold;'>{st.session_state.name}</div>
            <div style='font-size: 12px; color: grey;'>{st.session_state.email}</div>
        </div>
    </div>
    """
    st.markdown(profile_html, unsafe_allow_html=True)



# App navigation
   
def run_main_app():
  
    # st.sidebar.title("📌 Raah-e-Hunar")

    # Initialize the session page state
    if "page" not in st.session_state:
        st.session_state.page = "🏠 Home"

    selected_page = st.sidebar.selectbox("📂 Go to", [
        "🏠 Home", "🎯 Career Center", "🛠️ Skill Workshops","📌 My Workshops",
        "🌐 Search Online Jobs", "ℹ️ About", "💬 Feedback", "🚪 Logout"
    ], index=["🏠 Home", "🎯 Career Center", "🛠️ Skill Workshops","📌 My Workshops", "🌐 Search Online Jobs", "ℹ️ About", "💬 Feedback", "🚪 Logout"].index(st.session_state.page))

    skill_options = [
        "Teaching", "Programming", "Typing", "Sewing", "Computer", "Handicraft",
        "Farming", "Cooking", "Driving", "Repairing"
    ]
    # Only update the session page if a different page is selected
    if selected_page != st.session_state.page:
        st.session_state.page = selected_page
        st.rerun()

    page = st.session_state.page
    if page == "🏠 Home":
        st.title("✨ Welcome to Raah-e-Hunar")
     
        st.markdown("""
         ### Empowering Rural Talent 💪

        **Raah-e-Hunar** is dedicated to empowering youth from rural areas and small towns by providing:
        - 🧭 Personalized career guidance based on your skills and interests.
        - 🧑‍🏫 Access to skill workshops and training programs to boost your employability.
        - 💼 Job opportunities — both local and remote — tailored for you.
        - 🌐 Easy online job search by category and keyword.
        
        ---
        ### How to Get Started:
        1. Use the **🎯 Career Center** to input your skills and explore career paths.
        2. Check out the **🛠️ Skill Workshops** for hands-on training.
        3. Search jobs in the **🌐 Search Online Jobs** section.
        4. Share your thoughts or suggestions in **💬 Feedback**.
        
        We’re here to help you build a brighter future! 🚀
        """)

    elif page == "🎯 Career Center":
        st.header("🧠 Career Center")
        with st.form("career_form"):
            skills = st.multiselect("Select your current skills", skill_options)
            submit = st.form_submit_button("Submit")

        if submit:
            user = UserProfile( skills)
            st.session_state.user = user

        user = st.session_state.get("user")
        if user:
            user_name = st.session_state.name
            st.header(f"🔍 {user_name}, explore your ideal careers:")
            st.markdown("---")

           # Two-column layout for Career Recommendations and Job Opportunities
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("📌 Career Recommendations")
                advisor = CareerAdvisor()
                for r in advisor.recommend(user):
                    st.markdown(f"- {r}")

            with col2:
                st.subheader("💼 Job Opportunities")
                for j in JobOpportunity.match_jobs(user):
                    st.markdown(f"- {j}")

            st.markdown("---")
            # Training Section
            st.subheader("📚 Suggested Training Programs")
            # List current recommended trainings
            for t in TrainingProgram.get_programs(user):
                st.markdown(f"- {t}")
                
            st.markdown("---")
            # Separator
            st.markdown("""
            <div style="padding: 16px; border-radius: 10px; border-left: 5px solid #4CAF50; background-color: #f1f8e9;">
                <h4 style="color: #2e7d32;">💡 Ready to level up?</h4>
                <p style="font-size: 15px; color: #333;">
                    Check out our hands-on workshops and quick courses to boost your career! 🚀
                </p>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("🎯 Explore Workshops & Trainings"):
                    st.session_state.page = "🛠️ Skill Workshops"
                    st.rerun()

            
    elif page == "🛠️ Skill Workshops":
        st.title("🛠️ Skill Workshops")
        user = st.session_state.get("user")
        if user:
            email = st.session_state.email
            workshop_engine = Workshop(user)

            # Load user's enrolled workshops from persistent storage
            user_enrolled = workshop_data.get_user_workshops(email)

            used_free = any(w.get("free_first", False) for w in user_enrolled)
            free_msg = "You have used your free workshop credit." if used_free else "Your first workshop is free! 🎉"
            st.info(f"🔓 Freemium model: Free workshops available, but {free_msg}")

            workshops = workshop_engine.recommend()
            for i, workshop in enumerate(workshops):
                st.markdown(f"### {workshop['title']}")

                # Check if already joined
                already_joined = any(w['title'] == workshop['title'] for w in user_enrolled)
                if already_joined:
                    st.success("✅ Already Joined")
                    continue

                elif workshop["price"] == 0:
                    st.success("🎁 This workshop is free!")
                    if st.button(f"Join Now - {workshop['title']}", key=f"join_free_{i}"):
                        workshop_data.add_user_workshop(email, workshop)
                        st.balloons()
                        st.success(f"✅ You've successfully joined the '{workshop['title']}' workshop! Enjoy learning!")
                        st.rerun()

                else:  # Paid
                    st.warning(f"💳 Paid - PKR {workshop['price']}")
                    url = workshop_engine.generate_stripe_url(workshop["title"])
                    if url:
                        st.markdown(
                            f'<a href="{url}" target="_blank">'
                            f'<button style="background-color:#6757ff; color:white; padding:10px 20px;'
                            f'border:none; border-radius:5px; font-size:16px;">Pay With Stripe</button></a>',
                            unsafe_allow_html=True
                        )
                    else:
                        st.error("⚠️ Stripe link could not be generated. Please try again or contact support.")

                      # Testimonials
            st.markdown("---")
            st.subheader("🌟 Success Stories from Our Learners")
            for t in workshop_engine.get_testimonials():
                st.markdown(f"**{t['name']}** — *{t['career']}*")
                st.markdown(f"> {t['story']}")
                st.markdown("")
        else:
            st.warning("Please select your skills from career center to view workshops.")


    elif page == "📌 My Workshops":
        st.title("📌 My Workshops")

        email = st.session_state.get("email")
        if not email:
            st.warning("Please login to see your enrolled workshops.")
            return

        joined_workshops = workshop_data.get_user_workshops(email)

        if not joined_workshops:
            st.info("You haven’t joined any workshops yet.")
            return

        total_paid = sum(w.get("price", 0) for w in joined_workshops)
        st.markdown(f"**🔢 Total Workshops Joined:** {len(joined_workshops)}")
        st.markdown(f"**💰 Total Amount Paid:** PKR {total_paid}")
        st.markdown("---")

        for i, workshop in enumerate(joined_workshops):
            st.markdown(f"### {workshop['title']}")
            price = workshop.get("price", 0)
            if price == 0:
                st.success("✅ Free Workshop")
            else:
                st.info(f"💳 Paid - PKR {price}")

            if "date" in workshop:
                st.markdown(f"📅 **Date:** {workshop['date']}")
            if "duration" in workshop:
                st.markdown(f"⏱️ **Duration:** {workshop['duration']}")

            st.divider()

    elif page == "🌐 Search Online Jobs":
        st.header("🌐 Search Online Jobs")
        job_searcher = JobSearcher()
        categories = ["All", "Python", "JavaScript", "Next.js", "React", "Design", "Marketing", "Teaching", "Remote", "AI", "Data"]
        selected_category = st.selectbox("Choose a job category", categories)
        search_term = None if selected_category == "All" else selected_category

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
                st.info("No jobs found for this category.")
        else:
            st.info("Please select a category to begin.")

    elif page == "ℹ️ About":
        st.header("🌟 About Raah-e-Hunar")
        st.markdown("""
            **Raah-e-Hunar** is a platform focused on bridging the opportunity gap for youth in rural and semi-urban areas.
    
        Our mission is to:
        - Equip rural youth with relevant skills and knowledge.
        - Connect learners with career guidance and local/remote job opportunities.
        - Provide affordable or free workshops and training programs.
        - Foster a supportive community that encourages growth and success.
        
        This initiative is powered by passionate developers and educators who believe in the potential of every young individual, no matter their location.
        
        ---
        For questions, partnerships, or support, please [contact us](mailto:support@raah-e-hunar.org).
        
        Together, let's build pathways to success! 🌱""")

    elif page == "💬 Feedback":
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
        recent_feedback = FeedbackSystem.get_recent_feedback()
        if recent_feedback:
            for entry in recent_feedback:
                st.markdown(f"**👤 {entry['user']}** says:\n> {entry['feedback']}")
        else:
            st.info("No feedback yet. Be the first to share!")
            
            
    elif page == "🚪 Logout":
        
       auth_manager.logout()
       st.rerun()
    
        
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown(
        "<div style='text-align: center;'>✨ Made with ❤️ for rural youth by "
        "<a href='https://www.github.com/faryal16' target='_blank'>Code_With_Fairy</a></div>",
        unsafe_allow_html=True
    )

run_main_app()
