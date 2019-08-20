from django.db import models


class Order(models.Model):
    user_id = models.BigIntegerField()
    order_no = models.CharField(max_length=32)
    order_price = models.DecimalField(max_digits=10, decimal_places=2)
    create_time = models.DateTimeField()
    update_time = models.DateTimeField()

    class Meta:
        db_table = 't_order'
