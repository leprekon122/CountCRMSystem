from django.contrib import admin
from .models import FpvFlowStorage, MainFpvFlowOrder

# Register your models here.
admin.site.register(FpvFlowStorage)
admin.site.register(MainFpvFlowOrder)