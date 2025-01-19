from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.timezone import now

from django.db.models import Sum

# Create your models here.
class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    
    monthly_target = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def calculate_debt(self):
        paid = Payment.objects.filter(member=self).aggregate(Sum('amount'))['amount__sum'] or 0
        return max(0, self.monthly_target - paid)

    def __str__(self):
        return self.name


def validate_receipt_extension(value):
    if not value.name.endswith(('.jpg', '.jpeg', '.pdf')):
        raise ValidationError("Only JPEG or PDF files are allowed.")

class Payment(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)
    receipt = models.FileField(upload_to='receipts/', blank=True, null=True, validators=[validate_receipt_extension])

    def __str__(self):
        return f"{self.member} - ₦{self.amount} - {self.date}"


class MonthlyCollector(models.Model):
    month = models.DateField(unique=True, default=now)
    #collector = models.ForeignKey(Member, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.month.strftime('%B %Y')} - {self.collector.name}"

