from accounts.models import UserProfile
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from documents.models import AadharCardModel, DrivingLicenseModel, ImageWithVehicleModel
from django.urls import reverse



class DocumentVerificationTests(APITestCase):
    def setUp(self):
        self.user = UserProfile.objects.create_user(email='email@akgec.ac.in', password='testpassword')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_aadhar_upload(self):
        url = reverse('aadhar-upload')
        file_path = 'documents/tests/test_documents/test.pdf'
        with open(file_path, 'rb') as file:
            data = {'document': file}
            response = self.client.post(url, data, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(AadharCardModel.objects.filter(user=self.user).exists())

    def test_driving_license_upload(self):
        url = reverse('driving-license-upload')
        file_path = 'documents/tests/test_documents/test.pdf'
        with open(file_path, 'rb') as file:
            data = {'document': file}
            response = self.client.post(url, data, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(DrivingLicenseModel.objects.filter(user=self.user).exists())

    # def test_image_with_vehicle_upload(self):
    #     url = reverse("driving-license-upload")
    #     file_path = 'documents/tests/test_documents/test.png'
    #     with open(file_path, 'rb') as file:
    #         data = {'document': file}
    #         response = self.client.post(url, data, format='multipart')

    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #     print(response.data)
    #     print(ImageWithVehicleModel.objects.all())
    #     self.assertTrue(ImageWithVehicleModel.objects.filter(user=self.user).exists())

    def test_document_verification_status(self):
        url = reverse("document-verification-status")
        AadharCardModel.objects.create(user=self.user, document='documents/tests/test_documents/test.pdf', is_verified=True, verified_by=self.user, message='Verification successful')
        DrivingLicenseModel.objects.create(user=self.user, document='documents/tests/test_documents/test.pdf', is_verified=False, message='Verification pending')

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data['aadhar_card']['is_verified'], True)
        self.assertEqual(data['aadhar_card']['message'], 'Verification successful')
        self.assertEqual(data['driving_license']['is_verified'], False)
        self.assertEqual(data['driving_license']['message'], 'Verification pending')
        self.assertIsNone(data['image_with_vehicle'])  # Assuming there is no record for image with vehicle
