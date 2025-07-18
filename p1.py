from google_auth_oauthlib.flow import InstalledAppFlow
import os

SCOPES = ['https://www.googleapis.com/auth/calendar']

flow = InstalledAppFlow.from_client_secrets_file(
    'credentials/credentials.json', SCOPES
)

creds = flow.run_local_server(port=0)

# save token.json in credentials folder
os.makedirs("credentials", exist_ok=True)
with open('credentials/token.json', 'w') as token:
    token.write(creds.to_json())

print("✅ token.json generated in 'credentials/' folder.")
