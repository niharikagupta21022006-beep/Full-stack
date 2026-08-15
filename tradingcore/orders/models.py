from django.db import models

class Order(models.Model):
    SIDE_CHOICES = [
        ('BUY','Buy'),
        ('SELL','Sell')
    ]

    price = models.DecimalField(max_digits = 10,decimal_places = 2)
    quantity = models.IntegerField()
    side = models.CharField(max_length = 4,choices = SIDE_CHOICES)
    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f"{self.side} {self.quantity} @ {self.price}"
