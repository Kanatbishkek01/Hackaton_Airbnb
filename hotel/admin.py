from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Category)
# admin.site.register(Hotel)
admin.site.register(HotelImage)
admin.site.register(Comment)
admin.site.register(Like)

class HotelAdmin(admin.ModelAdmin):
    list_display = ['image','title','price','allowed_dates']
    list_filter = ['title','price']
    search_fields = ['title','price']

admin.site.register(Hotel, HotelAdmin)