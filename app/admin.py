from django.contrib import admin

# Register your models here.
from app.models.short import ShortUrls

admin.site.register(ShortUrls)