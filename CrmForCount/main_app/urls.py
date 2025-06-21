from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, re_path
from django.views.static import serve
from django.urls import path

urlpatterns = [
    path('', views.login_page, name='login_page'),
    path('first_page', views.FirstPage.as_view(), name='first_page'),
    path('fpv_storage', views.FPVFlowInStorage.as_view(), name='fpv_storage')
]

urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT})
]
