from fastapi_mail import MessageSchema

from app.config.email import send_email
from app.constants.envs import envs

async def send_password_reset_email(email: str, token: str, username: str):
    verification_link = f"{envs.FRONTEND_URL}/reset-password/{token}"
    message = MessageSchema(
        subject="Reset Password",
        recipients=[email],
        template_body={
            "username": username,
            "reset_link": verification_link,
        },
        subtype="html"
    )
    await send_email(message, template_name="reset_password.html")