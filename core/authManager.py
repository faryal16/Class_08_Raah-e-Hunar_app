import os
import httpx
import streamlit as st
import firebase_admin
from firebase_admin import credentials, initialize_app
import asyncio
from httpx_oauth.clients.google import GoogleOAuth2
import nest_asyncio
import jwt
from streamlit_cookies_manager import EncryptedCookieManager
import json

nest_asyncio.apply()

class AuthManager:
    def __init__(self):
         # Initialize cookies manager
        self.cookies = EncryptedCookieManager(
            prefix="raah_e_hunar_",
            password=st.secrets["client_secret"]  # set a secret key in your secrets.toml
        )

        if not self.cookies.ready():
            st.stop() 
        self.redirect_url = (
            "https://class08-raah-e-hunar-app.streamlit.app/"
            if "streamlit_app" in os.environ.get("HOST", "") or "streamlit" in st.secrets
            else "http://localhost:8501/"
        )

        json_str = os.getenv("FIREBASE_CREDENTIALS_JSON")

        if json_str:
            # Load from environment variable (string)
            cred_dict = json.loads(json_str)
            self.cred = credentials.Certificate(cred_dict)

        elif "firebase_credentials_json" in st.secrets:
            # Load from Streamlit secrets.toml
            firebase_cred = st.secrets["firebase_credentials_json"]

            if isinstance(firebase_cred, str):
                # If it's a JSON string, parse it
                cred_dict = json.loads(firebase_cred)
            else:
                # If it's already a dict, use as is
                cred_dict = firebase_cred

            self.cred = credentials.Certificate(cred_dict)

        else:
            # fallback local file
            self.cred = credentials.Certificate("raah-e-hunar-firebase-adminsdk-fbsvc-bab7ff5e7e.json")

        try:
            firebase_admin.get_app()
        except ValueError:
            initialize_app(self.cred)

        self.client_id = st.secrets["client_id"]
        self.client_secret = st.secrets["client_secret"]
        self.client = GoogleOAuth2(self.client_id, self.client_secret)

        for key in ["email", "name", "picture"]:
            if key not in st.session_state:
                st.session_state[key] = ""

        self.message_container = st.empty()
        self.login_button_container = st.empty()

    async def get_access_token(self, code: str):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://oauth2.googleapis.com/token",
                    data={
                        "code": code,
                        "client_id": self.client_id,
                        "client_secret": self.client_secret,
                        "redirect_uri": self.redirect_url,
                        "grant_type": "authorization_code"
                    },
                    headers={"Content-Type": "application/x-www-form-urlencoded"}
                )
                response.raise_for_status()
                return response.json()
        except Exception:
            self.show_error("Failed to get access token.")
            return None

    def parse_id_token(self, id_token: str):
        try:
            decoded = jwt.decode(id_token, options={"verify_signature": False})
            return {
                "user_id": decoded.get("sub"),
                "email": decoded.get("email"),
                "name": decoded.get("name"),
                "picture": decoded.get("picture")
            }
        except Exception:
            self.show_error("Failed to decode ID token.")
            return None

    def handle_callback(self):
        code = st.query_params.get("code")
        if code:
            token = asyncio.run(self.get_access_token(code))
            if token and "id_token" in token:
                user_info = self.parse_id_token(token["id_token"])
                if user_info:
                    st.session_state.email = user_info["email"]
                    st.session_state.name = user_info["name"]
                    st.session_state.picture = user_info["picture"]

                    # Store user info in cookies to persist session
                    self.cookies["email"] = user_info["email"]
                    self.cookies["name"] = user_info["name"]
                    self.cookies["picture"] = user_info["picture"]
                    self.cookies.save()

                    st.query_params.clear()
                    self.message_container.success(f"Welcome back, {user_info['name']}!")
                    self.login_button_container.empty()
                    return user_info["email"]
        return None
  


    def show_login_button(self):
        try:
            authorization_url = asyncio.run(self.client.get_authorization_url(
                self.redirect_url,
                scope=["email", "profile"],
                extras_params={"access_type": "offline", "prompt": "consent"}
            ))
            self.message_container = st.empty()
            self.login_button_container = st.empty()
            self.login_button_container.markdown(
                f'<a href="{authorization_url}" target="_self" style="text-decoration:none">'
                f'<button style="background-color:#4285F4;color:white;padding:10px 20px;'
                f'border:none;border-radius:5px;cursor:pointer;font-size:16px;">'
                f'Login with Google</button></a>', unsafe_allow_html=True)
            self.message_container.empty()
        except Exception:
            self.show_error("Error generating login URL.")

    def show_error(self, message):
        self.message_container.error(message)
    
    # New method to restore session from cookies
    def get_logged_in_user(self):
        if "email" in st.session_state and st.session_state.email:
            # Already loaded
            return

        # Check cookies for stored user info
        email = self.cookies.get("email", "")
        name = self.cookies.get("name", "")
        picture = self.cookies.get("picture", "")

        if email:
            st.session_state.email = email
            st.session_state.name = name
            st.session_state.picture = picture
            return email

        return None
    
    def logout(self):
        for key in ["email", "name", "picture"]:
            if key in st.session_state:
                del st.session_state[key]
            if key in self.cookies:
                del self.cookies[key]
        self.cookies.save()