from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import LoginForm, UserRegistrationForm, \
                   UserEditForm, ProfileEditForm
from .models import Account
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.http import HttpResponseForbidden
from .models import Equipment
from .forms import EquipmentForm,RentalForm,ClientForm
from django.db.models import Q
from .models import Equipment, Rental, Client
from .forms import EquipmentForm, RentalForm, ClientForm
from .models import Equipment
from .forms import EquipmentCategoryForm, MaintenanceForm, ReservationForm, PaymentForm
from .models import EquipmentCategory, Maintenance, Reservation, Payment

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})


@login_required
def dashboard(request):
    return render(request,
                  'account/dashboard.html',
                  {'section': 'dashboard'})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(
                user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            # Create the user profile
            Account.objects.create(user=new_user)
            return render(request,
                          'account/register_done.html',
                          {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request,
                  'account/register.html',
                  {'user_form': user_form})


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = ProfileEditForm(
                                    instance=request.user.profile,
                                    data=request.POST,
                                    files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated '\
                                      'successfully')
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(
                                    instance=request.user.profile)
    return render(request,
                  'account/edit.html',
                  {'user_form': user_form,
                   'profile_form': profile_form})
    
def logout_view(request):
    if request.method == 'POST':  # Перевірка, чи це POST-запит
        logout(request)
        return redirect('login')  # або на головну сторінку після виходу
    else:
        return HttpResponseForbidden("Метод не дозволений. Використовуйте POST.")
    


@login_required
def equipment_list(request):
    query = request.GET.get('q')
    if query:
        equipment = Equipment.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
    else:
        equipment = Equipment.objects.all()
    return render(request, 'account/equipment_list.html', {'equipment': equipment})


@login_required
def edit_equipment(request, pk):
    equipment = get_object_or_404(Equipment, pk=pk)
    if request.method == 'POST':
        form = EquipmentForm(request.POST, request.FILES, instance=equipment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Спорядження успішно оновлено.')
            return redirect('equipment_list')
        else:
            messages.error(request, 'Будь ласка, виправте помилки у формі.')
    else:
        form = EquipmentForm(instance=equipment)
    return render(request, 'account/edit_equipment.html', {'form': form})

@login_required
def add_equipment(request):
    if request.method == 'POST':
        form = EquipmentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Спорядження успішно додано.')
            return redirect('equipment_list')
        else:
            messages.error(request, 'Будь ласка, виправте помилки у формі.')
    else:
        form = EquipmentForm()
    return render(request, 'account/add_equipment.html', {'form': form})

@login_required
def delete_equipment(request, pk):
    equipment = get_object_or_404(Equipment, pk=pk)
    equipment.delete()
    return redirect('equipment_list')

@login_required
def client_list(request):
    clients = Client.objects.all()
    return render(request, 'account/client_list.html', {'clients': clients})
@login_required
def client_create(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Клієнт успішно створений.')
            return redirect('client_list')
    else:
        form = ClientForm()
    return render(request, 'account/client_form.html', {'form': form})
@login_required
def client_delete(request, pk):
    client = get_object_or_404(Client, pk=pk)
    if request.method == 'POST':
        client.delete()
        messages.success(request, 'Клієнт успішно видалений.')
        return redirect('client_list')
    return render(request, 'account/client_confirm_delete.html', {'client': client})

@login_required
def client_edit(request, pk):
    client = get_object_or_404(Client, pk=pk)
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            messages.success(request, 'Клієнт успішно оновлений.')
            return redirect('client_list')
    else:
        form = ClientForm(instance=client)
    return render(request, 'account/client_form.html', {'form': form})

@login_required
def rental_list(request):
    rentals = Rental.objects.all()
    return render(request, 'account/rental_list.html', {'rentals': rentals})

@login_required
def rental_create(request):
    if request.method == 'POST':
        form = RentalForm(request.POST)
        if form.is_valid():
            rental = form.save()
            messages.success(request, 'Оренда успішно створена.')
            return redirect('rental_list')
        else:
            messages.error(request, 'Будь ласка, виправте помилки у формі.')
    else:
        form = RentalForm()
    return render(request, 'account/rental_form.html', {'form': form})



@login_required
def rental_detail(request, pk):
    rental = get_object_or_404(Rental, pk=pk)
    return render(request, 'account/rental_detail.html', {'rental': rental})

@login_required
def equipment_category_list(request):
    categories = EquipmentCategory.objects.all()
    return render(request, 'account/equipment_category_list.html', {'categories': categories})

@login_required
def equipment_category_create(request):
    if request.method == 'POST':
        form = EquipmentCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Категорія успішно створена.')
            return redirect('equipment_category_list')
    else:
        form = EquipmentCategoryForm()
    return render(request, 'account/equipment_category_form.html', {'form': form})

@login_required
def maintenance_list(request):
    maintenances = Maintenance.objects.all()
    return render(request, 'account/maintenance_list.html', {'maintenances': maintenances})

@login_required
def maintenance_create(request):
    if request.method == 'POST':
        form = MaintenanceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Обслуговування успішно додано.')
            return redirect('maintenance_list')
    else:
        form = MaintenanceForm()
    return render(request, 'account/maintenance_form.html', {'form': form})

@login_required
def reservation_list(request):
    reservations = Reservation.objects.all()
    return render(request, 'account/reservation_list.html', {'reservations': reservations})

@login_required
def reservation_create(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save()
            messages.success(request, 'Резервація успішно створена.')
            return redirect('reservation_list')
        else:
            messages.error(request, 'Будь ласка, виправте помилки у формі.')
    else:
        form = ReservationForm()
    return render(request, 'account/reservation_form.html', {'form': form})

@login_required
def payment_list(request):
    payments = Payment.objects.all()
    return render(request, 'account/payment_list.html', {'payments': payments})

@login_required
def payment_create(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Оплата успішно додана.')
            return redirect('payment_list')
    else:
        form = PaymentForm()
    return render(request, 'account/payment_form.html', {'form': form})

@login_required
def rental_complete(request, pk):
    rental = get_object_or_404(Rental, pk=pk)
    if request.method == 'POST':
        if rental.status != 'completed':
            rental.status = 'completed'
            rental.save()
            messages.success(request, 'Оренда успішно завершена.')
        else:
            messages.warning(request, 'Оренда вже завершена.')
    return redirect('rental_detail', pk=pk)