from django.contrib import admin
from .models import *

""""registration of the models in admin panel"""

admin.site.register(Vendor)
admin.site.register(PurchaseOrder)
admin.site.register(HistoricalPerformance)