from rest_framework.views import APIView
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .logic_views import CreateFpvStorageNotice, CreateDatasets
from .models import FpvFlowStorage
from datetime import datetime


def login_page(request):
    """func for login"""
    username = request.POST.get('username')
    password = request.POST.get('password')

    user_auth = authenticate(request, username=username, password=password)
    if user_auth is not None:
        login(request, user_auth)
        return redirect('first_page')
    return render(request, "main_app/login_page.html")


class FirstPage(APIView):

    @staticmethod
    def get(request):
        add_fpv_storage = request.GET.get('add_fpv_storage')
        if add_fpv_storage:
            logic = CreateFpvStorageNotice(dron_name=request.GET.get('dron_name'), serial=request.GET.get('serial'),
                                           diagonal=request.GET.get('diagonal'),
                                           dron_number=int(request.GET.get('dron_num')),
                                           dron_in=request.GET.get('date_in'),
                                           dron_out=request.GET.get('date_out'), who_took=request.GET.get('who_took'),
                                           position_name=request.GET.get('position_name')).create_notice

        return render(request, "main_app/first_page.html")


class FPVFlowInStorage(APIView):
    objects = None

    @staticmethod
    def get(request):
        date_low = request.GET.get('date_low')
        date_up = request.GET.get('date_up')

        if date_up:
            logic = CreateDatasets.FilterByDateUp(self=None)
            return render(request, "main_app/fpv_storage_page.html", logic)
        if date_low:
            logic = CreateDatasets.LowDateFilter(self=None)
            return render(request, "main_app/fpv_storage_page.html", logic)
        logic = CreateDatasets.CreateSetForFpvStorageOrder(self=None)
        return render(request, "main_app/fpv_storage_page.html", logic)

    @staticmethod
    def post(request):
        delete_btn = request.POST.get('delete_btn')

        if delete_btn:
            dron_out = datetime.now().date()
            who_took = request.POST.get('who')
            position_name = request.POST.get('position')
            id = delete_btn
            logik = CreateDatasets(id=id, dron_out=dron_out, who_took=who_took, position_name=position_name)
            logik.DeleteNoticeFpvStorage()

            return render(request, "main_app/fpv_storage_page.html", logik.CreateSetForFpvStorageOrder())
        return render(request, "main_app/fpv_storage_page.html", {'model': FpvFlowStorage.objects.all().values()})
