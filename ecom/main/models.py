from django.db import models


class Cart(models.Model):
    id = models.OneToOneField('Products', models.DO_NOTHING, db_column='id', primary_key=True)
    price = models.BigIntegerField(blank=True, null=True)
    quantity = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cart'


class Products(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.CharField(max_length=255, blank=True, null=True)
    price = models.BigIntegerField(blank=True, null=True)
    details = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'products'
