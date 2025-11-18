from django.contrib import admin
from .models import StorageUnit, Compartment, Part, Inventory, LEDConfiguration

# Register your models here.
admin.site.register(StorageUnit)
admin.site.register(Compartment)
admin.site.register(Part)
admin.site.register(Inventory)
admin.site.register(LEDConfiguration)
