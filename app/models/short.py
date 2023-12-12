from django.contrib.auth.models import User
from django.db import models


class ShortUrls(models.Model):
    long_url = models.TextField()
    short_url = models.CharField(max_length=10, unique=True)
    qr_file = models.ImageField(upload_to='QrImages')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    used = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if self.short_url:
            return super(ShortUrls, self).save(*args, **kwargs)

    def __str__(self):
        return self.short_url
