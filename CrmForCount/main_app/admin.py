from django.contrib import admin
from .models import FpvFlowStorage, MainFpvFlowOrder, MavicAutelStorage, MavicAutelPositionFlow, RifleOrderModel, RadioServiceModel

# Register your models here.
admin.site.register(FpvFlowStorage)
admin.site.register(MainFpvFlowOrder)
admin.site.register(MavicAutelStorage)
admin.site.register(MavicAutelPositionFlow)
admin.site.register(RifleOrderModel)
admin.site.register(RadioServiceModel)