from django.db import models


# define product model
class Product(models.Model):

    CONDITION_TYPE = (
        ("new", "New product"),
        ("used", "Used product"),
        ("damaged", "Damaged product")
    )
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    condition = models.CharField(max_length=100,
                                 choices=CONDITION_TYPE)
    price = models.DecimalField(max_digits=8,
                                decimal_places=2)
    created = models.DateTimeField()

    def __str__(self):
        return self.name
