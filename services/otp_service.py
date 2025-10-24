import json
import time
import random
from django.core.cache import cache
from django.utils.translation import gettext_lazy as _

from config import settings
from apps.core.utils import _get_cache_keys, send_otp_email, send_otp_sms


class OTPService:
    def __init__(self, identifier, purpose="signup"):
        self.identifier = identifier
        self.purpose = purpose
        self.keys = _get_cache_keys(identifier, purpose)

    def can_send_otp(self):
        # Check if user is blocked
        if cache.get(self.keys["blocked"]):
            ttl = cache.ttl(self.keys["blocked"])
            return False, _("Too many attempts. Please try again in an hour."), ttl or 0

        attempts = cache.get(self.keys["attempts"]) or 0

        # First two attempts are free
        if attempts < 2:
            return True, None, 0

        # For third attempt and onwards, apply retry duration
        otp_data_raw = cache.get(self.keys["otp_data"])
        if otp_data_raw:
            otp_data = json.loads(otp_data_raw)
            last_sent = otp_data.get("timestamp", 0)
            time_since_last = int(time.time()) - last_sent
            if time_since_last < settings.RETRY_DURATION:
                wait = settings.RETRY_DURATION - time_since_last
                return False, _("Please wait before requesting another code."), wait

        return True, None, 0


    def send_otp(self, user_data, via_email=True):
        can_send, message, wait = self.can_send_otp()
        if not can_send:
            response = {"error": True, "message": message}
            if wait:
                response["retry_after_seconds"] = wait
            return response

        # Generate OTP
        otp = str(random.randint(100000, 999999))
        otp_data = {"otp": otp, "timestamp": int(time.time())}

        cache.set(self.keys["user_data"], json.dumps(user_data), timeout=settings.BLOCK_DURATION)
        cache.set(self.keys["otp_data"], json.dumps(otp_data), timeout=settings.OTP_EXPIRATION)

        send_func = send_otp_email if via_email else send_otp_sms
        result = send_func(self.identifier, otp)
        print(result)
        
        if not result.get("success", False):
            return {"error": True, "message": _("Failed to send OTP."), "detail": result.get("error")}

        # Increment attempts only **after successful send**
        attempts = cache.get(self.keys["attempts"]) or 0
        if attempts >= 2:
            attempts += 1
            if attempts >= settings.MAX_ATTEMPTS + 2:  # +2 because first 2 attempts are free
                cache.set(self.keys["blocked"], True, timeout=settings.BLOCK_DURATION)
                cache.delete(self.keys["attempts"])
                return {"error": True, "message": _("Too many attempts. Please try again in an hour.")}
            cache.set(self.keys["attempts"], attempts, timeout=settings.BLOCK_DURATION)
        else:
            # First two attempts: just increment to track free attempts
            cache.set(self.keys["attempts"], attempts + 1, timeout=settings.BLOCK_DURATION)

        return {"error": False, "message": _("OTP sent successfully.")}


    def verify_otp(self, otp_provided):
        raw_otp = cache.get(self.keys["otp_data"])
        if not raw_otp:
            return {"status": "not_found", "message": _("No OTP request found. Please request a new code.")}

        otp_data = json.loads(raw_otp)
        if otp_data.get("otp") != otp_provided:
            return {"status": "invalid", "message": _("Invalid OTP. Please try again.")}

        raw_user_data = cache.get(self.keys["user_data"])
        if not raw_user_data:
            return {"status": "expired", "message": _("User data expired. Please restart the process.")}

        return {"status": "valid", "data": json.loads(raw_user_data)}

    def clear_otp_data(self):
        cache.delete(self.keys["otp_data"])
        cache.delete(self.keys["user_data"])
        cache.delete(self.keys["attempts"])
        cache.delete(self.keys["blocked"])