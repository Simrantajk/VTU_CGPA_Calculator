# admin.py
from django.contrib import admin
from .models import Scheme, Sem, Subject, Branch

admin.site.register(Scheme)
admin.site.register(Branch)
admin.site.register(Sem)
admin.site.register(Subject)