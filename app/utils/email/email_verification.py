from itsdangerous import URLSafeTimedSerializer
from fastapi_mail import MessageSchema

from app.constants.envs import envs
from app.config.email import send_email

s = URLSafeTimedSerializer(envs.SECRET_KEY)

def generate_verification_token(email: str):
    return s.dumps(email, salt=envs.SECURITY_PASSWORD_SALT)

def confirm_verification_token(token: str, expiration=3600):
    try:
        email = s.loads(
            token,
            salt=envs.SECURITY_PASSWORD_SALT,
            max_age=expiration
        )
    except Exception:
        return False
    return email

async def send_verification_email(email: str, token: str, username: str):
    verification_link = f"{envs.FRONTEND_URL}/verify-email/{token}"
    message = MessageSchema(
        subject="Email Verification",
        recipients=[email],
        template_body={
            "username": username,
            "verification_link": verification_link,
            "token": token
        },
        subtype="html"
    )
    await send_email(message, template_name="verify_user.html")

