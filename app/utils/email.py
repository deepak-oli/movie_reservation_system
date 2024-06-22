from itsdangerous import URLSafeTimedSerializer
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig

from app.constants.envs import envs

conf = ConnectionConfig(
    MAIL_USERNAME=envs.MAIL_USERNAME,
    MAIL_PASSWORD=envs.MAIL_PASSWORD,
    MAIL_FROM=envs.MAIL_FROM,
    MAIL_PORT=envs.MAIL_PORT,
    MAIL_SERVER=envs.MAIL_SERVER,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    TEMPLATE_FOLDER="app/templates"
)

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
            "verification_link": verification_link
        },
        subtype="html"
    )
    fm = FastMail(conf)
    await fm.send_message(message, template_name="verify_user.html")

