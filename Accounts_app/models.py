from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):

    ROLE_CHOICES = (
        ('seller', 'Seller'),
        ('buyer', 'Buyer'),
    )

    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    is_verified = models.BooleanField(default=False)

#-----------------------------------------------------------------------------------------


class Seller(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    seller_name = models.CharField(max_length=100)
    address = models.TextField()
    phone_number = models.CharField(max_length=15)

    #  PAN Details
    pan_number = models.CharField(max_length=20, null=True, blank=True)
    pan_card_image = models.ImageField(upload_to='kyc/pan/', null=True, blank=True)

    #  Aadhaar Details
    aadhar_number = models.CharField(max_length=20, null=True, blank=True)
    aadhar_image = models.ImageField(upload_to='kyc/aadhar/', null=True, blank=True)

    #  Bank Details
    bank_account_holder_name = models.CharField(max_length=100, null=True, blank=True)
    bank_account_number = models.CharField(max_length=30, null=True, blank=True)
    bank_ifsc = models.CharField(max_length=20, null=True, blank=True)

    #  KYC Status (Very Important)
    kyc_status = models.CharField(
        max_length=20,
        choices=[
            ('Pending', 'Pending'),
            ('Approved', 'Approved'),
            ('Rejected', 'Rejected')
        ],
        default='Pending'
    )

    def __str__(self):
        return self.seller_name
    


#--------------------------------------------------------------------------------------




class Buyer(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    buyer_name = models.CharField(max_length=100)
    address = models.TextField()
    phone_number = models.CharField(max_length=15)