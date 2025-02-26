from django import forms
from django.contrib.auth.models import User
from .models import Account,Payment,EquipmentCategory,Maintenance,Reservation


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password',
                               widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password',
                                widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'email']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']

    def clean_email(self):
        data = self.cleaned_data['email']
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError('Email already in use.')
        return data


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def clean_email(self):
        data = self.cleaned_data['email']
        qs = User.objects.exclude(id=self.instance.id)\
                         .filter(email=data)
        if qs.exists():
            raise forms.ValidationError('Email already in use.')
        return data


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['date_of_birth', 'photo']
        
from django import forms
from .models import Equipment

class EquipmentForm(forms.ModelForm):
    class Meta:
        model = Equipment
        fields = ['name', 'description', 'price_per_day', 'image', 'available']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'price_per_day': forms.NumberInput(attrs={'step': '0.01'}),
        }
        labels = {
            'name': 'Назва',
            'description': 'Опис',
            'price_per_day': 'Ціна за день',
            'image': 'Зображення',
            'available': 'Доступне для оренди',
        }
        
from django import forms
from .models import Equipment, Rental, Client

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['first_name', 'last_name', 'email', 'phone']
        labels = {
            'first_name': 'Ім\'я',
            'last_name': 'Прізвище',
            'email': 'Електронна пошта',
            'phone': 'Телефон',
        }

class RentalForm(forms.ModelForm):
    rental_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label='Дата початку оренди'
    )
    return_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label='Дата закінчення оренди'
    )

    equipment = forms.ModelChoiceField(
        queryset=Equipment.objects.filter(available=True),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Спорядження'
    )

    class Meta:
        model = Rental
        fields = ['equipment', 'client', 'rental_date', 'return_date']
        widgets = {
            'client': forms.Select(attrs={'class': 'form-control'}),
        }

class EquipmentCategoryForm(forms.ModelForm):
    class Meta:
        model = EquipmentCategory
        fields = ['name', 'description']
        labels = {
            'name': 'Назва категорії',
            'description': 'Опис',
        }

class EquipmentForm(forms.ModelForm):
    class Meta:
        model = Equipment
        fields = ['name', 'category', 'description', 'price_per_day', 'image', 'available']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'price_per_day': forms.NumberInput(attrs={'step': '0.01'}),
        }
        labels = {
            'name': 'Назва',
            'category': 'Категорія',
            'description': 'Опис',
            'price_per_day': 'Ціна за день',
            'image': 'Зображення',
            'available': 'Доступне для оренди',
        }

class MaintenanceForm(forms.ModelForm):
    class Meta:
        model = Maintenance
        fields = ['equipment', 'maintenance_date', 'description', 'cost']
        widgets = {
            'maintenance_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }
        labels = {
            'equipment': 'Спорядження',
            'maintenance_date': 'Дата обслуговування',
            'description': 'Опис',
            'cost': 'Вартість',
        }

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['equipment', 'client', 'rental_start_date', 'rental_end_date']
        widgets = {
            'rental_start_date': forms.DateInput(attrs={'type': 'date'}),
            'rental_end_date': forms.DateInput(attrs={'type': 'date'}),
        }
        labels = {
            'equipment': 'Спорядження',
            'client': 'Клієнт',
            'rental_start_date': 'Дата початку оренди',
            'rental_end_date': 'Дата закінчення оренди',
        }

    def clean(self):
        cleaned_data = super().clean()
        equipment = cleaned_data.get('equipment')
        rental_start_date = cleaned_data.get('rental_start_date')
        rental_end_date = cleaned_data.get('rental_end_date')
        if rental_start_date and rental_end_date:
            if rental_start_date > rental_end_date:
                raise forms.ValidationError('Дата початку не може бути пізніше дати закінчення.')
            if not equipment.is_available(rental_start_date, rental_end_date):
                raise forms.ValidationError('Спорядження не доступне у вибраний період.')
        return cleaned_data

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['rental', 'amount', 'payment_date', 'method']
        widgets = {
            'payment_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
        labels = {
            'rental': 'Оренда',
            'amount': 'Сума',
            'payment_date': 'Дата оплати',
            'method': 'Метод оплати',
        }