# 1. Install packages listed in requirements.txt

pip install -r requirements.txt

# 2. Export all installed packages to requirements.txt

pip freeze > requirements.txt

#Architecture Flow:
User
↓
Frontend (e.g., HTML/CSS) or API Client (e.g., Postman, Swager API)
↓
FastAPI (Backend)
↓
NLP Engine (e.g., spaCy, parsedatetime, custom logic)
↓
Google Calendar API (via OAuth 2.0)
↓
Google Calendar (Events Read/Write)
