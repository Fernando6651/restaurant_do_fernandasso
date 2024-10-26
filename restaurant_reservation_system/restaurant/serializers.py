from rest_framework import serializers
from restaurant.models import Reservation

class ReservationSerializer(serializers.ModelSerializer):
    customer = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Reservation
        fields = ['customer_name', 'email', 'date', 'number_of_people', 'status', 'customer']
        read_only_fields = ['customer']  # 'customer' será preenchido automaticamente
