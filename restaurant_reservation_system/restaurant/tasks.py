from celery import shared_task
from django.core.mail import send_mail
from .models import Reservation

@shared_task
def send_reservation_notification(reservation_id):
    # Buscar a reserva no banco de dados
    reservation = Reservation.objects.get(id=reservation_id)

    # Enviar notificação via e-mail
    subject = 'Confirmação de Reserva'
    message = f'Sua reserva foi confirmada para o dia {reservation.date} para {reservation.number_of_people} pessoa(s).'
    
    send_mail(
        subject,
        message,
        'testesdofernandasso@gmail.com',  # Substitua pelo e-mail configurado
        [reservation.email],  # E-mail do cliente
        fail_silently=False,
    )
