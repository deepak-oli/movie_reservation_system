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

async def send_email(message: MessageSchema, template_name: str=None):
    fm = FastMail(conf)
    await fm.send_message(message, template_name=template_name)
