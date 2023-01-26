from django.db import models

class Cart(models.Model):
    product = models.CharField(primary_key=True, max_length=255)
    price = models.BigIntegerField(blank=True, null=True)
    quantity = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cart'


class Products(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.CharField(max_length=255, blank=True, null=True)
    price = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'products'