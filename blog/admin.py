from django.contrib import admin
from django.db import models

from .models import Post

admin.site.register((Post))
