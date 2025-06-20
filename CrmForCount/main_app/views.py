from rest_framework.views import APIView
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .logic_views import CreateFpvStorageNotice


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
                                           dron_number=int(request.GET.get('dron_num')), dron_in=request.GET.get('date_in'),
                                           dron_out=request.GET.get('date_out'), who_took=request.GET.get('who_took'),
                                           position_name=request.GET.get('position_name')).create_notice


        return render(request, "main_app/first_page.html")
