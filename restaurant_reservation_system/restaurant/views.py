from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, serializers
from rest_framework.exceptions import ValidationError
from .forms import RegistrationForm, ReservationForm
from .models import Dish, Reservation, TableAvailability
from .serializers import ReservationSerializer
from restaurant.tasks import send_reservation_notification
from django.contrib import messages
from django.utils.dateparse import parse_date
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import logout

class ReservationListCreateView(generics.ListCreateAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Verificar a disponibilidade de mesas para a data escolhida
        reservation_date = serializer.validated_data['date']
        table_availability = TableAvailability.objects.filter(date=reservation_date).first()

        if table_availability:
            if table_availability.available_tables > 0:
                table_availability.available_tables -= 1
                table_availability.save()
                reservation = serializer.save(customer=self.request.user)

                # Enviar notificação de confirmação de reserva
                send_reservation_notification.delay(reservation.id)
            else:
                raise ValidationError("No tables available for the selected date.")
        else:
            raise ValidationError("Table availability for the selected date has not been set.")


class ReservationDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    View para exibir, atualizar ou deletar uma reserva específica.
    Apenas o dono da reserva ou um administrador pode acessar esta view.
    """
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Sobrescreve o método para garantir que apenas o dono da reserva ou um admin
        possa ver, editar ou deletar as reservas.
        """
        if self.request.user.is_staff:
            return Reservation.objects.all()  # Admin pode ver todas as reservas
        return Reservation.objects.filter(customer=self.request.user)  # Usuário comum vê apenas suas reservas

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ['id', 'customer_name', 'email', 'date', 'number_of_people', 'status']

class ReservationListView(generics.ListAPIView):
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Retorna apenas as reservas do usuário autenticado
        return Reservation.objects.filter(customer=self.request.user)

# View para a página inicial
def home(request):
    return render(request, 'restaurant/home.html')

# View para listar as reservas
@login_required
def reservations_list(request):
    reservations = Reservation.objects.filter(customer=request.user)
    return render(request, 'restaurant/reservations_list.html', {'reservations': reservations})

@login_required
def create_reservation(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.customer = request.user  # Associa o usuário logado
            reservation.save()
            messages.success(request, 'Reserva criada com sucesso!')
            return redirect('reservations')
        else:
            messages.error(request, 'Erro ao criar reserva. Verifique os campos.')
    else:
        form = ReservationForm()
    return render(request, 'restaurant/create_reservation.html', {'form': form})


def delete_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    reservation.delete()
    messages.success(request, 'Sua reserva foi excluída com sucesso!')
    return redirect('reservations')


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Sua conta foi criada com sucesso!')
            return redirect('login')
        else:
            messages.error(request, 'Erro ao criar a conta. Verifique os campos.')
    else:
        form = RegistrationForm()
    
    return render(request, 'restaurant/register.html', {'form': form})


def menu_view(request):
    category = request.GET.get('category')  # Captura a categoria da URL, se existir
    if category:
        dishes = Dish.objects.filter(category=category)  # Filtra pela categoria
    else:
        dishes = Dish.objects.all()  # Exibe todos os pratos se nenhuma categoria for selecionada
    
    categories = Dish.CATEGORY_CHOICES  # Lista de categorias para exibir no filtro
    return render(request, 'restaurant/menu.html', {'dishes': dishes, 'categories': categories, 'selected_category': category})

def sobre_view(request):
    return render(request, 'restaurant/sobre.html')




def check_availability(request):
    date_str = request.GET.get('date')
    date = parse_date(date_str)
    
    if date is None:
        return JsonResponse({'error': 'Data inválida.'}, status=400)

    try:
        availability = TableAvailability.objects.get(date=date)
        available_tables = availability.available_tables
    except TableAvailability.DoesNotExist:
        available_tables = 0  # Nenhuma disponibilidade encontrada para a data

    return JsonResponse({'available_tables': available_tables}, status=200)

def create_reservation_view(request):
    
    form = ReservationForm()  # Inicializa o formulário
        
    today = timezone.now().date()
    today_plus_30_days = today + timedelta(days=30)
    
    # Resto da lógica da view de criação de reserva
    return render(request, 'restaurant/create_reservation.html', {
        'form': form,
        'today': today,
        'today_plus_30_days': today_plus_30_days,
    })
    
def generate_availability_for_next_30_days():
    today = timezone.now().date()
    end_date = today + timedelta(days=30)

    for single_date in (today + timedelta(days=n) for n in range((end_date - today).days + 1)):
        TableAvailability.objects.get_or_create(
            date=single_date,
            defaults={'available_tables': 20, 'max_tables': 20}  # Define o valor padrão
        )
        
        
@login_required
@user_passes_test(lambda u: u.is_superuser)
def admin_dashboard(request):
    total_reservations = Reservation.objects.count()
    context = {
        'total_reservations': total_reservations,
    }
    return render(request, 'restaurant/admin_dashboard.html', context)

def logout_view(request):
    logout(request)
    return redirect('home') 