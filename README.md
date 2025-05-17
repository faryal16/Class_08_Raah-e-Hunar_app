# **Raah-e-Hunar** - Empowering Rural Youth 🌾💪

**Raah-e-Hunar** is a community-driven platform designed to empower youth in rural and underserved areas by providing career guidance, skill development workshops (free and paid), job opportunities, and an easy way to search for online jobs. The app combines a Streamlit front-end with a FastAPI backend for payments and authentication, delivering a seamless experience.

---

## Table of Contents
1. [Features](#features)  
2. [Installation & Setup](#installation--setup)  
3. [Usage](#usage)  
4. [Architecture](#architecture)  
5. [Try the App](#try-the-app)  
6. [Dependencies](#dependencies)  
7. [Feedback](#feedback)  
8. [License](#license)  

---

## Features
- **Career Guidance**: Personalized career advice based on user skills and profile.  
- **Training Programs**: Access curated workshops, some free and some paid via Stripe integration.  
- **Free & Paid Workshops**: Freemium model allowing users to join a free workshop or pay for advanced workshops with Stripe checkout.  
- **User Enrollment**: Tracks user workshop enrollment persistently for personalized recommendations and to prevent duplicate enrollments.  
- **Job Opportunities**: Browse and search local and online job listings relevant to skills and preferences.  
- **Authentication & Authorization**: Secure user login using JWT and OAuth for protected access to features.  
- **Stripe Payment Integration**: Backend powered by FastAPI to create Stripe checkout sessions and handle webhooks for payment verification.  
- **Feedback System**: Submit and display user feedback to improve platform features.  

---

## Installation & Setup

### Prerequisites:
- Python 3.7+  
- Stripe account (for payment integration)  

### Clone the repo:
```bash
git clone https://github.com/faryal16/Class_08_Raah-e-Hunar_app.git
cd Class_08_Raah-e-Hunar_app
```
### Install Python dependencies:
```bash

pip install -r requirements.txt
```
### Environment Variables:
Create a .env file in your backend directory with the following:

```bash

STRIPE_SECRET_KEY=your_stripe_secret_key_here
STRIPE_WEBHOOK_SECRET=your_stripe_webhook_secret_here
JWT_SECRET_KEY=your_jwt_secret_key_here
```
### Running the Backend (FastAPI):
```bash

uvicorn stripe_server:app --reload --host 127.0.0.1 --port 8000
```
### Running the Frontend (Streamlit):
```bash

streamlit run main.py
```
### Usage
- Login/Register with your credentials or OAuth provider.

- Complete your profile with skills and email for personalized recommendations.

- Browse workshops:

- Free workshops can be joined immediately.

- Paid workshops have a "Pay with Stripe" button that opens the Stripe checkout session.

- Enroll in workshops: User enrollment is saved to persistent storage to track progress and used free credits.

- Search for jobs tailored to your skills and preferences.

- Give Feedback to help us improve the platform.

### Architecture
- Frontend: Streamlit app (app.py) handling UI, user interaction, session state, and calling backend APIs.

- Backend: FastAPI app (stripe_server.py) handling Stripe payment sessions, webhook events, and authentication.

- Data Persistence: Workshop enrollment and user data stored using JSON files or Firebase (optional).

- Authentication: JWT-based secure login and OAuth integrations using PyJWT and httpx-oauth.

- Payment: Stripe API used for checkout sessions with handling for free workshops (price=0 logic in frontend).

### Dependencies
- streamlit — Frontend UI

- fastapi — Backend API server

- uvicorn — ASGI server for FastAPI

- requests — HTTP client for backend/frontend communication

- stripe — Stripe SDK for payment integration

- PyJWT — JSON Web Token handling for authentication

- httpx — Async HTTP client (used for OAuth)

- httpx-oauth — OAuth client library

- firebase-admin — For Firebase integration (optional for data storage)

- nest_asyncio — Asyncio patching for compatibility (used in Streamlit backend calls)

- python-dotenv — Load environment variables from .env file

### Add these to your requirements.txt:
```bash

streamlit
fastapi
uvicorn
requests
stripe
PyJWT
httpx
httpx-oauth
firebase-admin
nest_asyncio
python-dotenv
```
### Try the App
Try it yourself by running the app locally or access the deployed app (if hosted) at:
(Raah-e-Hunar on Streamlit)[https://class08-raah-e-hunar-app.streamlit.app/]

### Feedback
Your feedback matters! Please use the Feedback tab inside the app to submit your suggestions or report issues.

### License
This project is licensed under the MIT License.

**Made with ❤️ by Code_With_Fairy for empowering rural youth.**