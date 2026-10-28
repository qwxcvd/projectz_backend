import resend

resend.api_key = ""


async def send_verification_code(email: str, code: str) -> None:
    params = {
        "from": "Test <onboarding@resend.dev>",
        "to": [email],
        "subject": "Подтверждение почты",
        "text": f"Ваш код подтверждения: {code}",
    }

    await resend.Emails.send_async(params)