import re
import ssl
import smtplib
import requests

from django.utils.translation import gettext_lazy as _

from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from email.message import EmailMessage
from config import settings

# Utility functions for sending OTP via email
def send_otp_email(email, otp):
    try:
        msg = EmailMessage()
        msg.set_content(f"Your OTP code is {otp}")
        msg["Subject"] = "Your OTP Code"
        msg["From"] = settings.DEFAULT_FROM_EMAIL
        msg["To"] = email

        context = ssl.create_default_context()
        with smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT) as server:
            server.starttls(context=context)
            server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
            server.send_message(msg)

        return {"success": True}

    except ValueError as e:
        return {"success": False, "error": f"Invalid OTP format: {e}"}
    except (smtplib.SMTPException, OSError) as e:
        print(e)
        return {"success": False, "error": str(e)}

# Utility functions for sending OTP via SMS
def send_otp_sms(username, otp):
    try:
        username = int(username)
        otp = int(otp)

        api_url = settings.SMS_API_URL
        params = {
            
            'user_name': settings.SMS_API_USERNAME,  
            'password': settings.SMS_API_PASSWORD,
            'template_code': 'Laftah_T2',
            'param_list': otp, 
            'sender': 'Laftah',
            'to': username
        }
        
        response = requests.get(api_url, params=params)
        
        if response.status_code == 200:
            if response.text.isdigit():
                return {"success": True}
            else:
                return {"success": False, "error": f"SMS API error: {response.text}"}
        else:
            return {"success": False, "error": f"HTTP {response.status_code}: {response.text}"}

    except ValueError:
        return {"success": False, "error": "Invalid username or OTP format"}
    except requests.exceptions.RequestException as e:
        return {"success": False, "error": str(e)}
    
# Helper function to generate cache keys
def _get_cache_keys(identifier, purpose):
    base = f"otp:{purpose}:{identifier}"
    return {
        "otp_data": f"{base}:otp",
        "user_data": f"{base}:user_data",
        "attempts": f"{base}:attempts",
        "blocked": f"{base}:blocked"
    }

# parser for identifiers
class IdentifierParser:
    @staticmethod
    def parse(value):
        first_char = value[0] if value else ""

        if first_char.isalpha():
            try:
                validate_email(value)
                return {"email": value, "phone": None, "identifier_type": "email"}
            except ValidationError:
                raise ValidationError(_("Please enter a valid email address."))

        elif first_char.isdigit() or first_char == "+":
            pattern = re.compile(r"^(?:\+963|0)9\d{8}$")
            if not pattern.match(value):
                raise ValidationError(_("Please enter a valid Syrian phone number starting with +9639 or 09."))
            return {"email": None, "phone": value, "identifier_type": "phone"}

        else:
            raise ValidationError(_("Invalid identifier. Must be a valid email or Syrian phone number."))