from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, re_path
from django.views.static import serve
from django.urls import path

urlpatterns = [
    path('', views.login_page, name='login_page'),
    path('first_page', views.FirstPage.as_view(), name='first_page'),
    path('fpv_storage', views.FPVFlowInStorage.as_view(), name='fpv_storage'),
    path('fpv_main_order', views.FpvMainFlowPage.as_view(), name='fpv_main_order'),
    path('mavic_autel_storage', views.MavicAutelInStorage.as_view(), name='mavic_autel_storage'),
    path('mavic_autel_position_flow', views.MavicAutelPostionFlow.as_view(), name="mavic_autel_position"),
    path('rifle_order', views.RifleOrderPage.as_view(), name='rifle_order'),
    path('radio_service', views.RadioServiceSupply.as_view(), name='radio_service'),
    path('radio_position_flow', views.RadioSupply.as_view(), name='radio_position'),
    path('statistic_page', views.StatisticsPage.as_view(), name='stat_page'),
    path('battery_storage', views.BatteryStorageOrder.as_view(), name='battery_storage'),
    path('battery_position', views.BatteryPositionOrder.as_view(), name='battery_position')
]

urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT})
]
