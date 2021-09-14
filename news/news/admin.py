from django.contrib import admin

from .models import User, News, Category, Comment

admin.site.register(User)
admin.site.register(News)
admin.site.register(Comment)
admin.site.register(Category)
