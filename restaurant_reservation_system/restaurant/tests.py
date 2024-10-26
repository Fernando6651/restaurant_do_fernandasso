from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User
from restaurant.models import Reservation, TableAvailability
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken
from django.test import TestCase

class ReservationTests(APITestCase):

    def setUp(self):
        # Cria um usuário de teste e autentica
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client = APIClient()

        # Obter e configurar o token JWT para autenticação
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(refresh.access_token)}')

        # Configura a disponibilidade de mesas para a data de teste
        self.aware_date = timezone.make_aware(timezone.datetime(2024, 10, 30))
        self.table_availability = TableAvailability.objects.create(
            date=self.aware_date, available_tables=5, max_tables=5
        )

    def test_create_reservation_with_available_tables(self):
        """Testa a criação de uma reserva quando há mesas disponíveis."""
        url = reverse('reservation-list')
        data = {
            'customer_name': 'John Doe',
            'email': 'john@example.com',
            'date': '2024-10-30T00:00:00Z',
            'number_of_people': 4,
            'status': 'pending'
        }

        # Envia uma requisição POST autenticada
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Verifica se a quantidade de mesas foi decrementada
        self.assertEqual(TableAvailability.objects.get(date=self.table_availability.date).available_tables, 1)

    def test_unauthenticated_user_cannot_create_reservation(self):
        """Testa se um usuário não autenticado não pode criar uma reserva."""
        # Remove o token JWT para simular usuário não autenticado
        self.client.credentials()  # Remove credenciais
        url = reverse('reservation-list')
        data = {
            'customer_name': 'John Doe',
            'email': 'john@example.com',
            'date': '2024-10-30T00:00:00Z',
            'number_of_people': 4,
            'status': 'pending'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_user_can_view_own_reservations(self):
        """Testa se um usuário autenticado pode ver suas próprias reservas."""
        Reservation.objects.create(
            customer=self.user,
            customer_name='Test User',
            email='test@example.com',
            date=self.aware_date,
            number_of_people=4,
            status='confirmed'
        )

        url = reverse('reservation-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['customer_name'], 'Test User')

class AvailabilityTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.test_date = "2024-12-12"
        TableAvailability.objects.create(date=self.test_date, available_tables=5)

    def test_check_availability_existing_date(self):
        """Testa a verificação de disponibilidade para uma data existente."""
        response = self.client.get(reverse('check_availability') + f'?date={self.test_date}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertJSONEqual(response.content, {'available_tables': 5})

    def test_check_availability_non_existing_date(self):
        """Testa a verificação de disponibilidade para uma data inexistente."""
        response = self.client.get(reverse('check_availability') + '?date=2024-12-13')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertJSONEqual(response.content, {'available_tables': 0})

    def test_check_availability_invalid_date(self):
        """Testa a verificação de disponibilidade com uma data inválida."""
        response = self.client.get(reverse('check_availability') + '?date=invalid-date')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertJSONEqual(response.content, {'error': 'Data inválida.'})
