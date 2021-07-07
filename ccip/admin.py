from django.contrib import admin

from .models import *


# Register your models here.
class DisplayImplant(admin.ModelAdmin):
    list_display = ('id', 'type', 'size', 'quantity')
    list_display_links = ('id', 'type', 'size')
    search_fields = ('id','type', 'size')
    list_per_page = (10)

class DisplaySurgery(admin.ModelAdmin):
    list_display = ('id', 'client', 'user')
    list_display_links = ('id', 'client', 'user')
    search_fields = ('id',)
    list_per_page = (10)

class DisplayClient(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'phone')
    list_display_links = ('id', 'full_name')
    search_fields = ('id', 'user')
    list_per_page = (10)

admin.site.register(Implant, DisplayImplant)
admin.site.register(Surgery, DisplaySurgery)
admin.site.register(Client, DisplayClient)