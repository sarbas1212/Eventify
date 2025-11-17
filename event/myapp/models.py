from django.db import models
from django.contrib.auth.models import User

class HeroBanner(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.TextField(blank=True, null=True)
    button_text = models.CharField(max_length=50, default="Book Your Events")
    image = models.ImageField(upload_to='herobanners/')  # <--- Folder name
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Hero Banner"
        verbose_name_plural = "Hero Banners"

    def __str__(self):
        return self.title



class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='services/')

    def __str__(self):
        return self.name


class ServiceType(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='types')
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='service_types/')
    budget = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    trending = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} ({self.service.name})"
    




class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=120)
    phone = models.CharField(max_length=20)
    secondary_phone = models.CharField(max_length=20, blank=True, null=True)
    venue = models.TextField()
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    service_type = models.ForeignKey(ServiceType, on_delete=models.CASCADE)
    event_date = models.DateField()
    event_time = models.TimeField()
    notes = models.TextField(blank=True)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    # Amount actually paid by user
    amount_paid = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    # Status can be 'pending', 'confirmed', 'cancelled' etc.
    status = models.CharField(max_length=24, default='pending')


    payment_type = models.CharField(max_length=50, null=True, blank=True)

    razorpay_order_id = models.CharField(max_length=200, null=True, blank=True)
    razorpay_payment_id = models.CharField(max_length=200, null=True, blank=True)
    razorpay_signature = models.CharField(max_length=255, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.service.name} - {self.service_type.name} on {self.event_date} {self.event_time}"
