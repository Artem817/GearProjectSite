from django.db import models

from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=50)
    address = models.TextField(blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    registration_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class EquipmentCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Equipment(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(EquipmentCategory, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField()
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='equipment_images/', null=True, blank=True)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def is_available(self, start_date, end_date):
        overlapping_rentals = Rental.objects.filter(
            equipment=self,
            rental_date__lte=end_date,
            return_date__gte=start_date,
            status='Ongoing',
        )
        overlapping_reservations = Reservation.objects.filter(
            equipment=self,
            rental_start_date__lte=end_date,
            rental_end_date__gte=start_date,
            status='Confirmed',
        )
        return not (overlapping_rentals.exists() or overlapping_reservations.exists())

class Account(models.Model):
    ROLE_CHOICES = (
        ('Admin', 'Admin'),
        ('Staff', 'Staff'),
        ('Customer', 'Customer'),
    )
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Customer')

    def __str__(self):
        return f'Profile of {self.user.username}'

class Maintenance(models.Model):
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    maintenance_date = models.DateField(default=timezone.now)
    description = models.TextField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'Maintenance {self.id} for {self.equipment.name}'

class Reservation(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Cancelled', 'Cancelled'),
    )
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    reservation_date = models.DateTimeField(default=timezone.now)
    rental_start_date = models.DateField()
    rental_end_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f'Reservation {self.id} by {self.client}'

class Rental(models.Model):
    STATUS_CHOICES = [
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
    ]
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    rental_date = models.DateField()
    return_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ongoing')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        days = (self.return_date - self.rental_date).days + 1
        self.total_price = days * self.equipment.price_per_day
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Rental {self.id} - {self.client}'

class Payment(models.Model):
    rental = models.ForeignKey(Rental, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(default=timezone.now)
    method = models.CharField(max_length=50)

    def __str__(self):
        return f'Payment {self.id} for Rental {self.rental.id}'