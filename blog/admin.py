from django.contrib import admin
from .models import Blog, BlogType
# Register your models here.

@admin.register(BlogType)
class BlogTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'type_name')

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'blog_type', 'get_read_num', 'last_update_time')

# @admin.register(ReadNumber)
# class ReadNumberAdmin(admin.ModelAdmin):
#     list_display = ('read_num', 'blog',)