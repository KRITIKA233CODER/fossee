from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
import io

User = get_user_model()


class UploadTest(TestCase):
    def setUp(self):
        self.username = 'testuser'
        self.password = 'pass'
        self.user = User.objects.create_user(username=self.username, password=self.password)

    def obtain_jwt(self):
        url = '/api/auth/login/'
        resp = self.client.post(url, {'username': self.username, 'password': self.password}, content_type='application/json')
        return resp.json()

    def test_upload_sample_csv(self):
        # obtain access token via simplejwt endpoint
        token_resp = self.obtain_jwt()
        self.assertIn('access', token_resp)
        access = token_resp.get('access')

        csv_content = b"Equipment Name,Type,Flowrate,Pressure,Temperature\nPump A,Pump,10,1.2,45\nValve B,Valve,5,0.8,30\n"
        url = reverse('dataset-upload')
        resp = self.client.post(url, {'file': io.BytesIO(csv_content)}, HTTP_AUTHORIZATION=f'Bearer {access}')
        self.assertIn(resp.status_code, (200,201))
        data = resp.json()
        self.assertIn('id', data)
        self.assertIn('summary', data)
