from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Table)
admin.site.register(Category)
admin.site.register(MenuItem)
admin.site.register(Order)
admin.site.register(OrderMenuItem)
admin.site.register(Receipt)
