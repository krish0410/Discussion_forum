from django.contrib import admin
from .models import Post,replyComment

# Register your models here.

admin.site.register((Post,replyComment))