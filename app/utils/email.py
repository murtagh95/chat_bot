""" Emails config and send function """
# Python
import os

# FastAPI
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig

# Utils
from app.utils.api.authentication import get_token
from pydantic import BaseModel, EmailStr
from typing import List

# Models
from app.core.models.tortoise.user import User


conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("EMAIL", "aaa@aaa.com"),
    MAIL_PASSWORD=os.getenv("EMAIL_PASS", "aaaa"),
    MAIL_FROM=os.getenv("EMAIL", "aaa@aaa.com"),
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_TLS=True,
    MAIL_SSL=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)


class EmailSchema(BaseModel):
    """ Email schema """
    email: List[EmailStr]


async def send_email(email: List, instance: User):
    token_data = {
        "id": instance.id,
        "username": instance.username
    }
    token = get_token(token_data)
    url = f"{os.getenv('BASE_URL', '')}/user/verification/?token={token}"
    template = f"""
<!DOCTYPE html>
<html lang="en">
<head>
</head>
<body>
    <div style="
        display: flex;
        align-items:center;
        justify-content:center;
        flex-direction: column;">
        <h3>Account Verification</h3>
        <br>
        <p>Thanks for choosing, please click on the button below to verify
        your account</p>
        <a style="
            margin-top: 1rem;
            padding: 1rem;
            border-radius: 0.5rem;
            font-size: 1rem;
            text-decoration: none;
            background: #0275d8;
            color: white;"
            href="{url}">
            Verify your email
        </a>
        <p>Please kindly ignore this email if you did not register and
         nothing will happened. Thanks</p>
    </div>
</body>
</html>
    """
    message = MessageSchema(
        subject="Account Verification Email",
        recipients=email,
        body=template,
        subtype="html"
    )
    fm = FastMail(config=conf)
    await fm.send_message(message=message)
