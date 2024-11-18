from django.contrib import admin
from .models import QA, Feedback, QA_Buyer, Question, VehicleBrand, VehicleType, Year, FuelType,  District, GearType,  OwnerType
# Register your models here.

admin.site.register(VehicleType)
admin.site.register(VehicleBrand)
admin.site.register(Year)
admin.site.register(FuelType)
admin.site.register(Feedback)
admin.site.register(QA)
admin.site.register(QA_Buyer)
admin.site.register(Question)
admin.site.register(District)
admin.site.register(GearType)
admin.site.register( OwnerType)
