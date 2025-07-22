from django.db import models
from django.conf import settings

# Create your models here.

class Invoice(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts', null=True, blank=True)
    invoice_number = models.CharField(max_length=20, unique=True)
    date = models.DateField()  
    due_date = models.DateField()

    client_name = models.CharField(max_length=100)
    client_address = models.TextField()
    client_email = models.EmailField()

    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    tax = models.DecimalField(max_digits=10, decimal_places=2)
    total_due = models.DecimalField(max_digits=10, decimal_places=2)

    payment_terms = models.TextField() 

    created_at = models.DateTimeField(auto_now_add=True)

    payment_terms = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def number_of_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']  


class InvoiceItem(models.Model):
    invoice = models.ForeignKey(
        Invoice,
        on_delete=models.CASCADE,
        related_name='items'
    )
    description = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.description} (x{self.quantity})"


class CompanyProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='company_profile',
        null=True, 
        blank=True,
    )    
    name = models.CharField(max_length=255)
    address = models.TextField()
    phone = models.CharField(max_length=50)
    email = models.EmailField()
    bank_name = models.CharField(max_length=255)
    bank_account_name = models.CharField(max_length=255)
    iban = models.CharField(max_length=50)
    swift_code = models.CharField(max_length=50)

    def __str__(self):
        return self.name
