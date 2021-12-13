from django.contrib import admin

from accounts.models import Address, Client

admin.site.register(Client)
admin.site.register(Address)
