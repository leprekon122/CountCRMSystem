from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.views import APIView
from rest_framework import permissions
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .logic_views import CreateFpvStorageNotice, CreateDatasets, CreateMavicAutelStorageNotice, FpvFlowPage, \
    RadioOrderLogic, RifleOrderLogic, RadioSupplyPosition, StatisticsLogic, FilterForMAvicAutelPosition, \
    BatteryStorageOrderLogic, BatteryPositionOrderLogic, PermissionOnView
from .models import FpvFlowStorage, MavicAutelPositionFlow, MainFpvFlowOrder, MavicAutelStorage, RifleOrderModel, \
    BatteryPositionOrderModel, UserOrderPermission
from datetime import datetime

from django.core.exceptions import PermissionDenied


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
    queryset = BatteryPositionOrderModel.objects.all()

    permission_classes = [
        permissions.IsAuthenticated,
        DjangoModelPermissions
    ]

    @staticmethod
    def get(request):

        return render(request, "main_app/first_page.html")

    @staticmethod
    def post(request):
        add_fpv_main = request.POST.get('add_fpv_main')
        add_fpv_storage = request.POST.get('add_fpv_storage')
        add_autel_mavic_storage = request.POST.get('add_autel_mavic_storage')
        add_radio_supply = request.POST.get('add_radio_supply')
        add_rifle = request.POST.get('add_rifle')
        add_battery_storage = request.POST.get('add_battery_storage')
        # BatteryStorageOrderLogic

        if add_battery_storage:
            BatteryStorageOrderLogic(battery_type=request.POST.get('battery_name'),
                                     price=request.POST.get('battery_price'),
                                     quantities=request.POST.get('quantities'),
                                     date_in=request.POST.get('bat_date_in'),
                                     doc_num=request.POST.get('bat_doc_num')).create_notice()

        if add_rifle:
            logic = RifleOrderLogic(nickname=request.POST.get('nickname'), type_rifle=request.POST.get('type_rifle'),
                                    rifle_number=request.POST.get('Rifle_number'),
                                    date_in_rifle=request.POST.get('date_in_rifle'),
                                    produced_date=request.POST.get('produced_date'))
            logic.add_notice()
        if add_autel_mavic_storage:
            CreateMavicAutelStorageNotice(dron_name=request.POST.get('dron_name1'),
                                          dron_number=request.POST.get('dron_num1'),
                                          dron_in=request.POST.get('date_in1'),
                                          dron_out=datetime.now().date(),
                                          document_num=request.POST.get('dok_num'),
                                          who_took=request.POST.get('who_took1'),
                                          drone_value=request.POST.get('dron_value'),
                                          position_name=request.POST.get(
                                              'position_name2'),
                                          ).create_mavic_autel_storage()

        if add_fpv_storage:
            logic = CreateFpvStorageNotice(dron_name=request.POST.get('dron_name'), serial=request.POST.get('serial'),
                                           diagonal=request.POST.get('diagonal'),
                                           dron_number=request.POST.get('dron_num'),
                                           dron_in=request.POST.get('date_in'),
                                           dron_out=datetime.now().date(), who_took=request.POST.get('who_took'),
                                           position_name=request.POST.get('position_name')).create_notice

        if add_fpv_main:
            CreateFpvStorageNotice(dron_name=request.POST.get('dron_name2'), serial=request.POST.get('serial2'),
                                   diagonal=request.POST.get('diagonal2'),
                                   dron_number=request.POST.get('dron_num2'),
                                   dron_in=request.POST.get('date_in2'),
                                   dron_out=datetime.now().date(),
                                   position_name=request.POST.get(
                                       'position_name1'),
                                   operator_name=(request.POST.get(
                                       'operator_name1'))).creation_dataset_for_fpv_main_order()

        if add_radio_supply:
            RadioOrderLogic(supply_name=request.POST.get('supply_name'),
                            supply_price=request.POST.get('supply_price'),
                            serial_number=request.POST.get('serial_number'),
                            date_in=request.POST.get('date_in')).create_radio_note()

        return render(request, "main_app/first_page.html")


class FPVFlowInStorage(APIView):
    objects = None

    queryset = BatteryPositionOrderModel.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    @staticmethod
    def get(request):
        """function for rendering get requests"""
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
        """function for rendering post requests"""
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
    queryset = BatteryPositionOrderModel.objects.all()

    permission_classes = [
        permissions.IsAuthenticated,
        DjangoModelPermissions
    ]

    @staticmethod
    def get(request):
        """function for rendering get requests"""
        logic = CreateDatasets.fpv_main_order_flow(self=None)
        return render(request, "main_app/fpv_main_order_flow.html", logic)

    @staticmethod
    def post(request):
        """function for rendering post requests"""
        logic = CreateDatasets.fpv_main_order_flow(self=None)
        delete_fpv_flow = request.POST.get('delete_fpv_flow')
        to_storage = request.POST.get('to_storage')

        if to_storage:
            FpvFlowPage(position_name=request.POST.get('fpv_flow_pos'),
                        who_took=request.POST.get('who'),
                        dron_id=to_storage
                        ).to_storage_return()

        if delete_fpv_flow:
            FpvFlowPage(dron_id=delete_fpv_flow, position_name=request.POST.get('fpv_flow_pos'),
                        who_took=request.POST.get('who')).delet_fpv_flow_notice()

        return render(request, "main_app/fpv_main_order_flow.html", logic)


class MavicAutelInStorage(APIView):
    """ class for respond in MavicAutelStorage order"""
    queryset = BatteryPositionOrderModel.objects.all()

    permission_classes = [
        permissions.IsAuthenticated,
        DjangoModelPermissions
    ]

    @staticmethod
    def get(request):
        """function for rendering get requests"""

        logic_perm = PermissionOnView(request.user).render_username()
        print(logic_perm)

        if logic_perm == 2:
            print(request.user)
            raise PermissionDenied

        else:
            logic = CreateDatasets.mavic_autel_storage_set()
            adaptive_search = request.GET.get('adaptive_search')
            start_num = request.GET.get('start_num')
            end_num = request.GET.get('end_num')
            adaptive_document = request.GET.get('adaptive_document')
            dron_num_search = request.GET.get('dron_num_search')
            status = request.GET.get('status')

            if status:
                on_storage = request.GET.get('on_storage')
                on_position = request.GET.get('on_position')

                if on_storage:
                    logic = CreateDatasets(status=on_storage).search_by_status_mav_storage()
                elif on_position:
                    logic = CreateDatasets(status=on_position).search_by_status_mav_storage()
                else:
                    logic = CreateDatasets.mavic_autel_storage_set()
                return render(request, "main_app/mavic_autel_storage.html", logic)

            if dron_num_search:
                logic = CreateDatasets(dron_num=dron_num_search).adaptive_search_by_dron_num()

            if adaptive_document:
                logic = CreateDatasets(adaptive_document=adaptive_document).create_adaptive_document_dataset()
                return render(request, "main_app/mavic_autel_storage.html", logic)

            if start_num is not None or end_num is not None:
                logic = CreateDatasets(start_num=start_num, end_num=end_num).create_dataset_for_mav_storage_prais_val()
                return render(request, "main_app/mavic_autel_storage.html", logic)

            if adaptive_search:
                logic = CreateDatasets(adaptive_mavic=adaptive_search).create_adaptive_mavic_autel()
                return render(request, "main_app/mavic_autel_storage.html", logic)
            return render(request, "main_app/mavic_autel_storage.html", logic)

    @staticmethod
    def post(request):
        """function for rendering post requests"""
        mavic_change = request.POST.get('mavic_change')
        document_num = request.POST.get('document_num')

        if document_num:
            CreateMavicAutelStorageNotice(id=int(request.POST.get('dok_btn')),
                                          document_num=document_num).update_document_num()

        if mavic_change:
            CreateMavicAutelStorageNotice(id=mavic_change,
                                          who_took=request.POST.get('whot_took_change'),
                                          position_name=request.POST.get('postion_name_change'),
                                          dron_out=datetime.now().date()
                                          ).update_notice()

        logic = CreateDatasets.mavic_autel_storage_set(self=None)
        return render(request, "main_app/mavic_autel_storage.html", logic)


class MavicAutelPostionFlow(APIView):
    """view for Mavic/Autel potion flow"""
    queryset = BatteryPositionOrderModel.objects.all()

    permission_classes = [
        permissions.IsAuthenticated,
        DjangoModelPermissions
    ]

    @staticmethod
    def get(request):
        """function for rendering get requests"""
        logic = CreateDatasets.mavic_autel_flow_position(self=None)
        dron_num_search = request.GET.get('dron_num_search')
        status = request.GET.get('status')

        if status:
            on_position = request.GET.get('on_position')
            destroyed = request.GET.get('destroyed')

            if on_position:
                logic = FilterForMAvicAutelPosition(status=on_position).status_on_position()
            elif destroyed:
                logic = FilterForMAvicAutelPosition(status=destroyed).status_on_position()
            else:
                return render(request, 'main_app/mavic_autel_position_flow.html', logic)

        if dron_num_search:
            logic = CreateDatasets(dron_num=dron_num_search).adaptive_search_by_dron_num_flow_order()
            return render(request, 'main_app/mavic_autel_position_flow.html', logic)

        return render(request, 'main_app/mavic_autel_position_flow.html', logic)

    @staticmethod
    def post(request):
        """function for rendering post requests"""

        destroy_pos_item = request.POST.get('destroy_pos_item')
        to_storage = request.POST.get("to_storage")

        if to_storage:
            CreateMavicAutelStorageNotice(id=to_storage,
                                          dron_out=datetime.now().date(),
                                          who_took=request.POST.get('who_crash')
                                          ).updat_notice_in_flow_page()

        if destroy_pos_item:
            MavicAutelPositionFlow.objects.filter(id=destroy_pos_item).update(dron_out=datetime.now().date(),
                                                                              who_took=request.POST.get('who_crash'),
                                                                              status=0,
                                                                              crash_coordinates=request.POST.get(
                                                                                  'crash_coordinates'),
                                                                              comment=request.POST.get('comment')

                                                                              )

        logic = CreateDatasets.mavic_autel_flow_position(self=None)
        return render(request, 'main_app/mavic_autel_position_flow.html', logic)


class RifleOrderPage(APIView):
    """Page for manging rifle_order.html"""
    queryset = BatteryPositionOrderModel.objects.all()

    permission_classes = [
        permissions.IsAuthenticated,
        DjangoModelPermissions
    ]

    @staticmethod
    def get(request):
        """function for rendering get requests"""
        logic = CreateDatasets.RifleDataSetMAin(self=None)
        del_rifle = request.GET.get('del_rifle')

        if del_rifle:
            RifleOrderLogic(notice_id=del_rifle).delete_notice()

        return render(request, 'main_app/rifle_order.html', logic)

    @staticmethod
    def post(request):
        """function for rendering post requests"""
        logic = CreateDatasets.RifleDataSetMAin(self=None)
        change_username_btn = request.POST.get('change_username_btn')
        username_data = request.POST.get('change_username')
        test = RifleOrderModel.objects.filter(id=change_username_btn).values()
        test[0]['Nickname'] = username_data

        if change_username_btn:
            # RifleOrderLogic(notice_id=change_username_btn, nickname=username_data).change_name()
            test = RifleOrderModel.objects.get(id=int(change_username_btn))
            test.Nickname = username_data
            test.save()

        return render(request, 'main_app/rifle_order.html', logic)


class RadioServiceSupply(APIView):
    """class for manage radio_servise_supply.html"""
    queryset = BatteryPositionOrderModel.objects.all()

    permission_classes = [
        permissions.IsAuthenticated,
        DjangoModelPermissions
    ]

    @staticmethod
    def get(request):
        """function for rendering get requests"""
        logic = CreateDatasets.RadioServiceSetMain(self=None)
        adaptive_search = request.GET.get('adaptive_search')
        status = request.GET.get('status')

        if status:
            on_storage = request.GET.get('on_storage')
            on_position = request.GET.get('on_position')

            if on_storage:
                logic = RadioOrderLogic(status=on_storage).order_by_status()

            elif on_position:
                logic = RadioOrderLogic(status=on_position).order_by_status()

            return render(request, "main_app/radio_servise_supply.html", logic)

        if adaptive_search:
            logic = CreateDatasets(adaptive_mavic=adaptive_search).create_radio_adaptive()
            render(request, 'main_app/radio_servise_supply.html', logic)
        return render(request, 'main_app/radio_servise_supply.html', logic)

    @staticmethod
    def post(reqeust):
        """function for rendering post requests"""
        logic = CreateDatasets.RadioServiceSetMain(self=None)
        del_radio = reqeust.POST.get('del_radio')
        radio_to_flow = reqeust.POST.get('radio_to_flow')

        if radio_to_flow:
            who_took = reqeust.POST.get('who_took')
            position_name = reqeust.POST.get('position_name')
            RadioSupplyPosition(storage_id=radio_to_flow, notice_id=radio_to_flow, who_took=who_took,
                                position_name=position_name).create_article()
            return render(reqeust, 'main_app/radio_servise_supply.html', logic)

        if del_radio:
            RadioOrderLogic(notice_id=del_radio).delete_notice()
            return render(reqeust, 'main_app/radio_servise_supply.html', logic)
        return render(reqeust, 'main_app/radio_servise_supply.html', logic)


class RadioSupply(APIView):
    """class for routing RadioOrder on position"""
    queryset = BatteryPositionOrderModel.objects.all()

    permission_classes = [
        permissions.IsAuthenticated,
        DjangoModelPermissions
    ]

    @staticmethod
    def get(request):
        """function for rendering get requests"""
        logic = RadioSupplyPosition.create_dataset_main(self=None)

        return render(request, 'main_app/Radio_supply_positon_flow.html', logic)

    @staticmethod
    def post(request):
        """function for rendering post requests"""
        logic = RadioSupplyPosition.create_dataset_main(self=None)
        radio_to_storage = request.POST.get('radio_to_storage')
        del_radio = request.POST.get('del_radio')

        if radio_to_storage:
            RadioSupplyPosition(storage_id=radio_to_storage).return_to_storage()

        if del_radio:
            who_crash = request.POST.get('who_crash')
            coordinates = request.POST.get('coordinates')
            RadioSupplyPosition(notice_id=del_radio, who_took=who_crash, coordinates=coordinates).delete_article()

        return render(request, 'main_app/Radio_supply_positon_flow.html', logic)


class StatisticsPage(APIView):
    """class for statistic page"""
    queryset = BatteryPositionOrderModel.objects.all()
    permission_classes = [
        permissions.IsAuthenticated,
        DjangoModelPermissions
    ]

    @staticmethod
    def get(request):
        """function for rendering get requests"""
        logic = StatisticsLogic.stat_data_mavic_autel(self=None)

        in_position_mav = MavicAutelPositionFlow.objects.filter(
                                                                Q(status=1) |
                                                                Q(dron_name__contains='DJI Mavic 3 Thermal') |
                                                                Q(dron_name__contains='DJI Mavic 3(Thermal)') |
                                                                Q(dron_name__contains='DJI Matrice 4T') |
                                                                Q(dron_name__contains='БпАК DJI MAvic 3T') |
                                                                Q(dron_name__contains='Mavic 3E (Enterprise)') |
                                                                Q(dron_name__contains='БпАК Autel EVO MAX 4T') |
                                                                Q(dron_name__contains='Autel EVO MAX 4T') |
                                                                Q(dron_name__contains='БПАК DJI MATRICE 4T') |
                                                                Q(dron_name__contains='DJi Mavic 3 PRO (DJI RS)') |
                                                                Q(dron_name__contains='DJI Mavic 3') |
                                                                Q(dron_name__contains='Autel EVO Max 4N')
                                                                ).count()
        print(in_position_mav)

        return render(request, 'main_app/statistics_page.html', logic)


class BatteryStorageOrder(APIView):
    """class for rendering Battery storage order"""
    queryset = BatteryPositionOrderModel.objects.all()

    permission_classes = [
        permissions.IsAuthenticated,
        DjangoModelPermissions
    ]

    @staticmethod
    def get(request):
        """function rendering GET requests"""
        logic = BatteryStorageOrderLogic.create_main_data_set(self=None)
        battery_type = request.GET.get('battery_type')

        if battery_type:
            bat_name = request.GET.get('bat_type_search')
            logic = BatteryStorageOrderLogic(battery_type=bat_name).filter_by_name()
            return render(request, 'main_app/battery_storage_order.html', logic)

        return render(request, 'main_app/battery_storage_order.html', logic)

    @staticmethod
    def post(request):
        """function for rendering post requests"""
        logic = BatteryStorageOrderLogic.create_main_data_set(self=None)
        to_pos = request.POST.get('to_pos')

        if to_pos:
            who_took = request.POST.get('who_took')
            position_name = request.POST.get('position_name')
            notice_id = request.POST.get('to_pos')
            calculator = request.POST.get('calculator')

            BatteryStorageOrderLogic(notice_id=notice_id, who_took=who_took, position_name=position_name,
                                     quantities=calculator).send_to_position()

        return render(request, 'main_app/battery_storage_order.html', logic)


class BatteryPositionOrder(APIView):
    """class for routing battery_position_order.html"""

    queryset = BatteryPositionOrderModel.objects.all()

    permission_classes = [
        permissions.IsAuthenticated,
        DjangoModelPermissions
    ]

    @staticmethod
    def get(request):
        """function for rendering get requests"""
        logic = BatteryPositionOrderLogic.create_main_data_set(self=None)
        battery_type = request.GET.get('battery_type')
        status = request.GET.get('status')

        if status:
            on_position = request.GET.get('on_position1')
            destroyed = request.GET.get('destroyed')
            if on_position is not None:
                logic = BatteryPositionOrderLogic(status=status).filter_by_status()
                return render(request, 'main_app/battery_position_order.html', logic)
            elif destroyed is not None:
                logic = BatteryPositionOrderLogic(status=status).filter_by_status()
                return render(request, 'main_app/battery_position_order.html', logic)

        if battery_type:
            bat_type_search = request.GET.get('bat_type_search')
            logic = BatteryPositionOrderLogic(battery_type=bat_type_search).filter_by_batt_type()
            return render(request, 'main_app/battery_position_order.html', logic)

        return render(request, 'main_app/battery_position_order.html', logic)

    @staticmethod
    def post(request):
        """function for rendering post requests"""
        logic = BatteryPositionOrderLogic.create_main_data_set(self=None)

        destroy = request.POST.get('destroy')

        if destroy:
            logic = BatteryPositionOrderLogic.create_main_data_set(self=None)
            calculator = request.POST.get('calculator')
            BatteryPositionOrderLogic(notice_id=destroy, quantities=calculator).destroy_logic()
            return render(request, 'main_app/battery_position_order.html', logic)

        return render(request, 'main_app/battery_position_order.html', logic)
