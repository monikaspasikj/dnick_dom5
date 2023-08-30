from enum import Enum
from django.contrib.auth.models import User
from django.db import models


class Product(models.Model):
    kod = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    how_to_use = models.CharField(max_length=255)
    contains = models.CharField(max_length=255)
    price = models.FloatField()
    # image = models.ImageField(upload_to="images/")
    image = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    date_from = models.DateTimeField(null=True, blank=True)
    date_to = models.DateTimeField(null=True, blank=True)

    CATEGORY_CHOICES = [
        ('HE', 'Herbicidi'),
        ('FU', 'Fungicidi'),
        ('IN', 'Insekticidi'),
        ('AK', 'Akaracidi'),
        ('BI', 'Biocidi'),
    ]

    category = models.CharField(
        max_length=2,
        choices=CATEGORY_CHOICES,
        default='HE'
    )

    ##kod, quantity da se stavi u order
    ### how to make custom login forma
    ### dodadi enum za kategorie

    def __str__(self):
        return self.name


class Customer(models.Model):
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    age = models.IntegerField()
    address = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    passwordConfirm = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} {self.surname}"


class Order(models.Model):
    id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    date_created = models.DateTimeField(null=True, blank=True)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return self.id

class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.order} - {self.product}"

# Create your models here.
