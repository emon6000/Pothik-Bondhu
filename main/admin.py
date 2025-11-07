# main/admin.py

from django.contrib import admin
from .models import District  # 1. Import your new District model

# 2. Register your model with the admin site
admin.site.register(District)