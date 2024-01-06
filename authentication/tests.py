from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken
from vroomvroom.settings import REST_FRAMEWORK
from .models import OTP, ResetPasswordModel


REST_FRAMEWORK["DEFAULT_THROTTLE_RATES"] = {
    "anon": "5000000/hour",
    "resend_otp": "5000000/hour",
}


class RegisterUserTests(APITestCase):
    def setUp(self):
        self.client = APIClient()

    def test_register_view_valid_data(self):
        url = reverse("register")
        # Register New User With AKGEC Mail And Password
        data = {"email": "test@akgec.ac.in", "password": "Password@123"}

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("access_token", response.data)
        self.assertIn("refresh_token", response.data)

    def test_register_view_invalid_email(self):
        # Registering With Invalid Mail Format
        url = reverse("register")
        data = {"email": "invalid@example.com", "password": "Password@123"}

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)

    def test_register_view_invalid_password(self):
        # Registering with invalid password Format
        url = reverse("register")
        data = {"email": "test@akgec.ac.in", "password": "987987879"}

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", response.data)


class TokenGenerationTests(APITestCase):
    def setUp(self):
        self.user_data = {"email": "test@akgec.ac.in", "password": "Password@123"}
        self.user = get_user_model().objects.create_user(**self.user_data)
        self.token_url = reverse("token_generate")

    def test_token_generation(self):
        # Testing Token generation
        data = {
            "email": self.user_data["email"],
            "password": self.user_data["password"],
        }
        response = self.client.post(self.token_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_token_verification(self):

        # Generate a token for the user
        refresh = RefreshToken.for_user(self.user)
        token = {"token": str(refresh)}

        # Verify the token
        response = self.client.post(reverse("token_verify"), token, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_token_refresh(self):
        # Generate a token for the user
        refresh = RefreshToken.for_user(self.user)
        token = {"refresh": str(refresh)}

        # Refresh the token
        response = self.client.post(reverse("token_refresh"), token, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)


class ResendEmailVerificationViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@akgec.ac.in",
            password="Test@123",
        )
        self.client.force_authenticate(user=self.user)

    def test_resend_email_verification_success(self):
        # Send a verification email initially
        response_initial = self.client.post(reverse("resend_email_verification"))
        self.assertEqual(response_initial.status_code, status.HTTP_200_OK)

        # Ensure the OTP object is created
        self.assertTrue(OTP.objects.filter(user=self.user, otp_type="email").exists())

        # Resend the verification email
        response_resend = self.client.post(reverse("resend_email_verification"))
        self.assertEqual(response_resend.status_code, status.HTTP_200_OK)

        # Ensure a new OTP object is created
        self.assertTrue(OTP.objects.filter(user=self.user, otp_type="email").exists())

    def test_resend_email_verification_user_already_verified(self):
        # Mark the user as email verified
        self.user.email_verified = True
        self.user.save()

        response = self.client.post(reverse("resend_email_verification"))

        # Ensure the response indicates that the email is already verified
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Email is Already Verified", response.data["message"])


class EmailVerifyViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@akgec.ac.in",
            password="Test@123",
            email_verified=False,
        )
        self.client.force_authenticate(user=self.user)

    def test_email_verify_success(self):
        # Send a verification email initially
        response_initial = self.client.post(reverse("resend_email_verification"))
        self.assertEqual(response_initial.status_code, status.HTTP_200_OK)

        # Ensure the OTP object is created
        self.assertTrue(OTP.objects.filter(user=self.user, otp_type="email").exists())

        # Retrieve the OTP from the database
        otp_object = OTP.objects.get(user=self.user, otp_type="email")

        # Verify the email using the OTP
        response_verify = self.client.post(
            reverse("verify_email"), {"otp": otp_object.otp}
        )
        self.assertEqual(response_verify.status_code, status.HTTP_200_OK)

        # Ensure the user's email is marked as verified
        self.user.refresh_from_db()
        self.assertTrue(self.user.email_verified)

    def test_email_verify_invalid_otp(self):
        # Try to verify email with an invalid OTP
        response = self.client.post(reverse("verify_email"), {"otp": "invalid_otp"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Invalid OTP", response.data["error"])

    def test_email_verify_expired_otp(self):
        # Send a verification email initially
        response_initial = self.client.post(reverse("resend_email_verification"))
        self.assertEqual(response_initial.status_code, status.HTTP_200_OK)

        # Ensure the OTP object is created
        self.assertTrue(OTP.objects.filter(user=self.user, otp_type="email").exists())

        # Retrieve the OTP from the database
        otp_object = OTP.objects.get(user=self.user, otp_type="email")

        # Expire the OTP
        otp_object.expiry_time = otp_object.expiry_time - timezone.timedelta(days=1)
        otp_object.save()

        # Try to verify email with an expired OTP
        response_verify = self.client.post(
            reverse("verify_email"), {"otp": otp_object.otp}
        )
        self.assertEqual(response_verify.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("OTP has expired", response_verify.data["error"])

class SendPhoneOTPViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email='test@example.com',
            password='Test@123',
            email_verified=False,
        )
        self.client.force_authenticate(user=self.user)


    def test_send_phone_otp_invalid_user_email_not_verified(self):

        # Try to send OTP for phone verification
        response = self.client.post(reverse('send_phone_verification'), {'phone_number': '1234567890'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Verify Email First.', response.data['message'])

class PhoneOTPVerifyViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email='test@example.com',
            password='Test@123',
            email_verified=True,
        )
        self.client.force_authenticate(user=self.user)
        self.otp = OTP.objects.create(user=self.user, otp=123456, otp_type='phone',expiry_time = timezone.now() + timezone.timedelta(minutes=5))

    def test_verify_phone_otp_success(self):
        # Verify phone using OTP
        response = self.client.post(reverse('verify_phone'), {'otp': self.otp.otp})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Phone verified successfully', response.data['message'])

        # Ensure the user's phone is marked as verified
        self.user.refresh_from_db()
        self.assertTrue(self.user.phone_verified)

    def test_verify_phone_otp_invalid_otp(self):
        # Try to verify phone with an invalid OTP
        response = self.client.post(reverse('verify_phone'), {'otp': 'invalid_otp'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Invalid OTP', response.data['error'])

    def test_verify_phone_otp_expired_otp(self):
        # Expire the OTP
        self.otp.expiry_time = self.otp.expiry_time - timezone.timedelta(minutes=5)
        self.otp.save()

        # Try to verify phone with an expired OTP
        response = self.client.post(reverse('verify_phone'), {'otp': self.otp.otp})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('OTP has expired', response.data['error'])

class ForgetPasswordEmailSendOTPViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email='test@example.com',
            password='Test@123',
            email_verified=True,
        )

    def test_send_email_otp_success(self):
        # Send OTP for email verification
        response = self.client.post(reverse('reset_send_otp_email'), {'email': self.user.email})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Email sent successfully', response.data['message'])
        self.assertIn('token', response.data)

        # Check that the ResetPasswordModel object is created
        self.assertTrue(ResetPasswordModel.objects.filter(user=self.user).exists())

    def test_send_email_otp_invalid_user_email_not_verified(self):
        # Ensure the user's email is not verified
        self.user.email_verified = False
        self.user.save()

        # Try to send OTP for email verification
        response = self.client.post(reverse('reset_send_otp_email'), {'email': self.user.email})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('No Account Registered With Given Mail ID.', response.data['error'])

class ForgetPasswordPhoneSendOTPViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email='test@example.com',
            password='Test@123',
            email_verified=True,
            phone_number='1234567890',
            phone_verified=True,
        )

    def test_send_phone_otp_invalid_user_phone_not_verified(self):
        # Ensure the user's phone is not verified
        self.user.phone_verified = False
        self.user.save()

        # Try to send OTP for phone verification
        response = self.client.post(reverse('reset_send_otp_phone'), {'phone_number': self.user.phone_number})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('No Account Registered With Given Phone Number', response.data['error'])

class ForgetPasswordVerifyOTPViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email='test@example.com',
            password='Test@123',
            email_verified=True,
        )
        self.reset_password_model = ResetPasswordModel.objects.create(user=self.user, otp=123456, token='TestTOken',expiry_time = timezone.now() + timezone.timedelta(minutes=5))

    def test_verify_otp_success(self):
        # Verify OTP using token
        response = self.client.post(reverse('reset_verify_otp'), {'otp': self.reset_password_model.otp, 'token': self.reset_password_model.token})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('OTP verified successfully', response.data['message'])
        self.assertIn('token', response.data)

        # Ensure the ResetPasswordModel object is marked as verified
        self.reset_password_model.refresh_from_db()
        self.assertTrue(self.reset_password_model.verified)

    def test_verify_otp_invalid_otp(self):
        # Try to verify OTP with an invalid OTP
        response = self.client.post(reverse('reset_verify_otp'), {'otp': 'invalid_otp', 'token': self.reset_password_model.token})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Invalid OTP', response.data['error'])

    def test_verify_otp_invalid_token(self):
        # Try to verify OTP with an invalid token
        response = self.client.post(reverse('reset_verify_otp'), {'otp': self.reset_password_model.otp, 'token': 'invalid_token'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Invalid OTP', response.data['error'])

class UpdatePasswordViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email='test@example.com',
            password='Test@123',
            email_verified=True,
        )
        self.reset_password_model = ResetPasswordModel.objects.create(
            user=self.user,
            otp=123456,
            expiry_time=timezone.now() + timezone.timedelta(minutes=5),
            token='some_token',
            verified=True,
        )

    def test_update_password_success(self):
        new_password = 'NewPassword@123'
        token = self.reset_password_model.token

        # Update password after verification
        response = self.client.post(reverse('update_password'), {'token': token, 'new_password': new_password})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Password updated successfully', response.data['message'])

        # Ensure the user's password is updated
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password(new_password))

        # Ensure the ResetPasswordModel object is deleted
        self.assertFalse(ResetPasswordModel.objects.filter(user=self.user).exists())

    def test_update_password_invalid_token(self):
        # Try to update password with an invalid token
        response = self.client.post(reverse('update_password'), {'token': 'invalid_token', 'new_password': 'NewPassword@123'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('User Verification Failed', response.data['error'])

    def test_update_password_expired_token(self):
        # Expire the token
        self.reset_password_model.expiry_time = timezone.now() - timezone.timedelta(minutes=5)
        self.reset_password_model.save()

        # Try to update password with an expired token
        response = self.client.post(reverse('update_password'), {'token': self.reset_password_model.token, 'new_password': 'NewPassword@123'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Token has expired', response.data['error'])

class ResetPasswordLogoutTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email='test@example.com',
            password='Test@123',
        )
        self.refresh_token = RefreshToken.for_user(self.user)
        self.access_token = str(self.refresh_token.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

    def test_same_access_token_after_reset_password(self):
        # Reset the user's password using user.set_password
        new_password = 'NewPassword@123'
        self.user.set_password(new_password)
        self.user.save()

        # Try making a request with the same access token after resetting the password
        response_after_reset_password = self.client.get(reverse('get_user_details'))
        self.assertEqual(response_after_reset_password.status_code, status.HTTP_401_UNAUTHORIZED)