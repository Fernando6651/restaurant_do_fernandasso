from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Reservation
from django.core.exceptions import ValidationError
from django.utils import timezone

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Obrigatório. Adicione um e-mail válido.")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['customer_name', 'email', 'date', 'number_of_people']

    def clean_date(self):
        date = self.cleaned_data.get('date')
        now = timezone.now()  # Obtém o datetime com informações de fuso horário

        if date < now:
            raise forms.ValidationError("A data da reserva não pode ser no passado.")
        
        return date