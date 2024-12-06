from django.db import models
from django.conf import settings

from accounts.models import Account


class Meeting(models.Model):
    title = models.CharField(max_length=200)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    invited_contacts = models.ManyToManyField(Account, related_name="events", blank=True)

    def __str__(self):
        return self.title
