import requests
from django.core.mail import send_mail
from django.conf import settings

def send_welcome_email(otp, email):
    subject = "Welcome to VroomVroom - Your AKGEC Ride-Sharing Experience Begins!"
    
    message = f"""
    <html>
    <body>
        <p>Hi there,</p>

        <p>Welcome to VroomVroom, the ultimate ride-sharing experience exclusively for AKGEC college!</p>

        <p>We're thrilled to have you on board. Your journey with us starts now. Let's make commuting convenient and enjoyable.</p>

        <p>To get started, use the following one-time password (OTP) during the registration process:</p>

        <a href="#" style="display: inline-block; padding: 10px 20px; background-color: #4CAF50; color: white; text-align: center; text-decoration: none; font-size: 16px; margin-bottom: 10px; border-radius: 5px;">{otp}</a>

        <p>If you have any questions or need assistance, feel free to reach out to our support team.</p>

        <p>Happy riding!</p>
        
        <p>Best regards,<br>The VroomVroom Team</p>
    </body>
    </html>
    """

    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]

    return send_mail(subject, '', from_email, recipient_list, html_message=message)

def send_mobile_otp(otp,mobile_number):
    r = requests.get(f"https://2factor.in/API/V1/{settings.OTP_API_KEY}/SMS/{mobile_number}/{otp}/")
    if r.status_code == 200:
        return True
    print(r)
    return False
