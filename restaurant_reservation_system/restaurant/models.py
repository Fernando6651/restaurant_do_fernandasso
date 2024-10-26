from django.db import models
from django.contrib.auth.models import User

class Reservation(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)  # Relaciona a reserva ao usuário
    customer_name = models.CharField(max_length=100)
    email = models.EmailField()
    date = models.DateTimeField()
    number_of_people = models.IntegerField()
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('confirmed', 'Confirmed'), ('canceled', 'Canceled')])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reservation for {self.customer_name} on {self.date}"

class TableAvailability(models.Model):
    date = models.DateField(unique=True)
    available_tables = models.IntegerField()
    max_tables = models.IntegerField(default=20)

    def __str__(self):
        return f"Tables available on {self.date}: {self.available_tables}/{self.max_tables}"
    
    def decrement_availability(self, count=1):
        """ Decrease available tables by count if possible. """
        if self.available_tables >= count:
            self.available_tables -= count
            self.save()
            return True
        return False
    
class Dish(models.Model):
    CATEGORY_CHOICES = [
        ('starter', 'Entrada'),
        ('main', 'Prato Principal'),
        ('dessert', 'Sobremesa'),
        ('beverage', 'Bebida')
    ]

    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    image = models.ImageField(upload_to='dishes/', blank=True, null=True)  # Imagem opcional

    def __str__(self):
        return self.name
