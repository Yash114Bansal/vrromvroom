from rest_framework.throttling import UserRateThrottle

class ResendOTPRateThrottle(UserRateThrottle):
    scope = 'resend_otp'