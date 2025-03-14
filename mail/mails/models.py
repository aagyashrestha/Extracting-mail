from django.db import models

class Transaction(models.Model):
    amount = models.FloatField()
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.amount} - {self.description}"
