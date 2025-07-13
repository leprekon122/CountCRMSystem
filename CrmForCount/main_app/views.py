from rest_framework.views import APIView
from rest_framework import permissions
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .logic_views import CreateFpvStorageNotice, CreateDatasets, CreateMavicAutelStorageNotice
from .models import FpvFlowStorage, MavicAutelStorage
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
    permission_classes = [permissions.IsAuthenticated]

    @staticmethod
    def get(request):
        return render(request, "main_app/first_page.html")

    @staticmethod
    def post(request):
        add_fpv_main = request.POST.get('add_fpv_main')
        add_fpv_storage = request.POST.get('add_fpv_storage')
        add_autel_mavic_storage = request.POST.get('add_autel_mavic_storage')

        if add_autel_mavic_storage:
            logic = CreateMavicAutelStorageNotice(dron_name=request.POST.get('dron_name1'),
                                                  dron_number=request.POST.get('dron_num1'),
                                                  dron_in=request.POST.get('date_in1'),
                                                  dron_out=datetime.now().date(),
                                                  who_took=request.POST.get('who_took1'),
                                                  position_name=request.POST.get(
                                                      'position_name2')).create_mavic_autel_storage()

        if add_fpv_storage:
            logic = CreateFpvStorageNotice(dron_name=request.POST.get('dron_name'), serial=request.POST.get('serial'),
                                           diagonal=request.POST.get('diagonal'),
                                           dron_number=request.POST.get('dron_num'),
                                           dron_in=request.POST.get('date_in'),
                                           dron_out=datetime.now().date(), who_took=request.POST.get('who_took'),
                                           position_name=request.POST.get('position_name')).create_notice

        if add_fpv_main:
            logic = CreateFpvStorageNotice(dron_name=request.POST.get('dron_name2'), serial=request.POST.get('serial2'),
                                           diagonal=request.POST.get('diagonal2'),
                                           dron_number=request.POST.get('dron_num2'),
                                           dron_in=request.POST.get('date_in2'),
                                           dron_out=datetime.now().date(),
                                           position_name=request.POST.get(
                                               'position_name1'),
                                           operator_name=(request.POST.get(
                                               'operator_name1'))).creation_dataset_for_fpv_main_order()

        return render(request, "main_app/first_page.html")


class FPVFlowInStorage(APIView):
    objects = None
    permission_classes = [permissions.IsAuthenticated]

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


class FpvMainFlowPage(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @staticmethod
    def get(request):
        logic = CreateDatasets.fpv_main_order_flow(self=None)
        return render(request, "main_app/fpv_main_order_flow.html", logic)

    @staticmethod
    def post(request):
        return render(request, "main_app/fpv_main_order_flow.html")


class MavicAutelInStorage(APIView):
    """ class for respond in MavicAutelStorage order"""
    permission_classes = [permissions.IsAuthenticated]

    @staticmethod
    def get(request):
        logic = CreateDatasets.mavic_autel_storage_set()
        return render(request, "main_app/mavic_autel_storage.html", logic)

    @staticmethod
    def post(request):
        mavic_change = request.POST.get('mavic_change')

        if mavic_change:
            logic = CreateMavicAutelStorageNotice(id=mavic_change,
                                                  who_took=request.POST.get('whot_took_change'),
                                                  position_name=request.POST.get('postion_name_change'),
                                                  dron_out=datetime.now().date()
                                                  ).update_notice()

        logic = CreateDatasets.mavic_autel_storage_set(self=None)
        return render(request, "main_app/mavic_autel_storage.html", logic)


class MavicAutelPostionFlow(APIView):
    """view for Mavic/Autel potion flow"""
    permission_classes = [permissions.IsAuthenticated]

    @staticmethod
    def get(request):
        logic = CreateDatasets.mavic_autel_flow_position(self=None)
        return render(request, 'main_app/mavic_autel_position_flow.html', logic)
