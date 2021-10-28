from django.db import models
from django.contrib.auth.models import User


class advisor(models.Model):
    name = models.CharField(max_length=30)
    photo = models.FileField(blank=False)

    def __str__(self):
        return self.name


class advisor_booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    booking_time = models.DateTimeField()
    advisors = models.ForeignKey(advisor, on_delete=models.CASCADE, blank=True)

    def __str__(self):
        return str(self.user)
