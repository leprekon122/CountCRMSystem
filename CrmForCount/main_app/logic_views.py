from django.db.models import Sum, Q

from .models import FpvFlowStorage, MainFpvFlowOrder, MavicAutelStorage, MavicAutelPositionFlow, RifleOrderModel, \
    RadioServiceModel
from datetime import datetime


class CreateMavicAutelStorageNotice:
    '''class for creating  notice in MavicAutelStorage model'''

    def __init__(self, id=None, dron_name=None, dron_number=None, dron_in=None, dron_out=None,
                 who_took=None, position_name=None, document_num=None, drone_value=None):
        self.id = id
        self.dron_name = dron_name
        self.dron_number = dron_number
        self.dron_in = dron_in
        self.dron_out = dron_out
        self.who_took = who_took
        self.position_name = position_name
        self.document_num = document_num
        self.drone_value = int(drone_value or 0)

    def update_document_num(self):
        MavicAutelStorage.objects.filter(id=self.id).update(
            number_of_document=self.document_num)

    def create_mavic_autel_storage(self):
        try:
            MavicAutelStorage.objects.create(
                dron_name=self.dron_name,
                dron_number=self.dron_number,
                dron_in=self.dron_in,
                dron_out=self.dron_out,
                who_took=self.who_took,
                position_name=self.position_name,
                number_of_document=self.document_num,
                supply_value=self.drone_value
            )
        except:
            MavicAutelStorage.objects.create(
                dron_name=self.dron_name,
                dron_number=self.dron_number,
                dron_in=self.dron_in,
                dron_out=self.dron_out,
                who_took=self.who_took,
                position_name=self.position_name,
                number_of_document=self.document_num,
            )

    def update_notice(self=None):
        '''func for creating update request'''

        MavicAutelStorage.objects.filter(id=self.id).update(status=0,
                                                            who_took=self.who_took,
                                                            position_name=self.position_name,
                                                            dron_out=self.dron_out)

        background_set = MavicAutelStorage.objects.filter(id=self.id).values()[0]
        id_for_update = MavicAutelStorage.objects.filter(id=self.id).values()[0]['id_for_flow']

        if id_for_update is not None:
            MavicAutelPositionFlow.objects.filter(id=id_for_update).update(
                dron_in=background_set['dron_in'],
                dron_out=background_set['dron_out'],
                position_name=background_set['position_name'],
                status=1
            )
        else:
            MavicAutelPositionFlow.objects.create(dron_name=background_set['dron_name'],
                                                  dron_number=background_set['dron_number'],
                                                  dron_in=background_set['dron_in'],
                                                  # dron_out=background_set['dron_out'],
                                                  position_name=background_set['position_name'],
                                                  id_for_storage=self.id
                                                  )

    def updat_notice_in_flow_page(self):
        id_for_storage = MavicAutelPositionFlow.objects.filter(id=self.id).values()[0]['id_for_storage']

        MavicAutelPositionFlow.objects.filter(id=self.id).update(dron_out=datetime.now().date(),
                                                                 who_took=self.who_took,
                                                                 status=2
                                                                 )

        MavicAutelStorage.objects.filter(id=id_for_storage).update(status=1,
                                                                   dron_out=None,
                                                                   who_took=None,
                                                                   position_name=None,
                                                                   id_for_flow=self.id
                                                                   )


class CreateFpvStorageNotice:

    def __init__(self, dron_name=None, serial=None, diagonal=None, dron_number=None, dron_in=None, dron_out=None,
                 who_took=None, position_name=None, operator_name=None):
        self.dron_name = dron_name
        self.serial = serial
        self.diagonal = diagonal
        self.dron_number = dron_number
        self.dron_in = dron_in
        self.dron_out = dron_out
        self.who_took = who_took
        self.position_name = position_name
        self.operator_name = operator_name

    @property
    def create_notice(self):
        """func creating new add"""
        FpvFlowStorage.objects.create(dron_name=self.dron_name, serial=self.serial, diagonal=self.diagonal,
                                      dron_number=self.dron_number, dron_in=self.dron_in, dron_out=self.dron_out,
                                      who_took=self.who_took, position_name=self.position_name)

    def creation_dataset_for_fpv_main_order(self):
        """func for crating new article in fpv main order"""
        MainFpvFlowOrder.objects.create(dron_name=self.dron_name, serial=self.serial, diagonal=self.diagonal,
                                        dron_number=self.dron_number, dron_in=self.dron_in, dron_out=self.dron_out,
                                        position_name=self.position_name, operator_name=self.operator_name)


class CreateDatasets:
    """Class for creating datasets on order pages """

    def __init__(self, id=None, dron_out=None, who_took=None, position_name=None, drone_name=None, dron_num=None,
                 adaptive_mavic=None, start_num=None, end_num=None, adaptive_document=None):
        self.drone_name = drone_name
        self.drone_num = dron_num
        self.dron_out = dron_out
        self.who_took = who_took
        self.position_name = position_name
        self.id = id
        self.adaptive_mavic = adaptive_mavic
        self.start_num = start_num
        self.end_num = end_num
        self.adaptive_document = adaptive_document

    def adaptive_search_by_dron_num_flow_order(self):
        """crating dataset for  searching by drone num """
        dataset = MavicAutelPositionFlow.objects.filter(dron_number__icontains=self.drone_num).values()
        data = {'model': dataset}
        return data

    def adaptive_search_by_dron_num(self):
        """crating dataset for  searching by drone num """
        dataset = MavicAutelStorage.objects.filter(dron_number__icontains=self.drone_num).values()
        data = {'model': dataset}
        return data

    def create_adaptive_document_dataset(self):
        """function for document number adaptive filter in MAvicAutel Storage"""
        dataset = MavicAutelStorage.objects.filter(number_of_document__icontains=self.adaptive_document).values()
        data = {'model': dataset}
        return data

    def create_dataset_for_mav_storage_prais_val(self):

        if self.start_num != 0 or self.end_num != 0:
            if self.start_num != 0 and self.end_num == 0:
                model = MavicAutelStorage.objects.filter(supply_value__gte=self.start_num).values()
            if self.start_num == 0 and self.end_num != 0:
                model = MavicAutelStorage.objects.filter(supply_value__lte=self.end_num).values()
            if self.start_num != 0 and self.end_num != 0:
                model = MavicAutelStorage.objects.filter(
                    Q(supply_value__gte=self.start_num) & Q(supply_value__lte=self.end_num)).values()

            data = {'model': model}
            return data

    def create_radio_adaptive(self):
        data_set = RadioServiceModel.objects.filter(supply_name__icontains=self.adaptive_mavic).values()
        data = {"model": data_set}
        return data

    def create_adaptive_mavic_autel(self):
        data_set = MavicAutelStorage.objects.filter(dron_name__icontains=self.adaptive_mavic).values()
        data = {"model": data_set}
        return data

    def CreateSetForFpvStorageOrder(self):
        """Creating main set"""
        set = FpvFlowStorage.objects.all().values()
        data = {"model": set,
                "stat": 2
                }
        return data

    def DeleteNoticeFpvStorage(self):
        """request for deleting notice"""
        set = FpvFlowStorage.objects.filter(id=self.id).update(status=0,
                                                               dron_out=self.dron_out,
                                                               who_took=self.who_took,
                                                               position_name=self.position_name,
                                                               )
        data_for_creating = FpvFlowStorage.objects.filter(id=self.id).values()[0]

        if data_for_creating['id_for_flow'] is not None:
            MainFpvFlowOrder.objects.filter(id=data_for_creating['id_for_flow']).update(
                dron_name=data_for_creating['dron_name'], serial=data_for_creating['serial'],
                diagonal=data_for_creating['diagonal'],
                dron_number=data_for_creating['dron_number'],
                dron_in=datetime.now().date(),
                dron_out=datetime.now().date(),
                id_for_storage=self.id,
                status=1
            )
        else:
            MainFpvFlowOrder.objects.create(dron_name=data_for_creating['dron_name'],
                                            serial=data_for_creating['serial'],
                                            diagonal=data_for_creating['diagonal'],
                                            dron_number=data_for_creating['dron_number'],
                                            dron_in=datetime.now().date(),
                                            dron_out=datetime.now().date(),
                                            id_for_storage=self.id
                                            )

    def LowDateFilter(self=None):
        """Date filter Up to low """
        set = FpvFlowStorage.objects.values().order_by('dron_in')
        data = {"model": set,
                'stat': 1
                }
        return data

    def FilterByDateUp(self=None):
        """Date filter Low to Up """
        set = FpvFlowStorage.objects.values().order_by('-dron_in')
        data = {"model": set,
                'stat': 2
                }
        return data

    def fpv_main_order_flow(self):
        """func for making data set in main fpv order"""
        data = {
            "model": MainFpvFlowOrder.objects.all().values()
        }
        return data

    def mavic_autel_storage_set(self=None):
        """func making main order in MAvic/Autel Storge page"""
        total_value = MavicAutelStorage.objects.aggregate(Sum('supply_value'))['supply_value__sum']
        data = {
            "model": MavicAutelStorage.objects.values(),
            'total_value': total_value
        }
        return data

    def mavic_autel_flow_position(self):
        """func for making base dataset for Mavic/Autel position flow page """

        data = {"model": MavicAutelPositionFlow.objects.values()}

        return data

    def RifleDataSetMAin(self):
        """data set for rifle main order"""

        data = {'model': RifleOrderModel.objects.values()}
        return data

    def RadioServiceSetMain(self):
        """data set for RadioService main order"""

        data = {"model": RadioServiceModel.objects.values().order_by('-id')}

        return data


class FpvFlowPage:

    def __init__(self, dron_id=None, dron_name=None, serial=None, diagonal=None, dron_number=None, dron_in=None,
                 dron_out=None,
                 who_took=None, position_name=None, operator_name=None):
        self.dron_id = dron_id
        self.dron_name = dron_name
        self.serial = serial
        self.diagonal = diagonal
        self.dron_number = dron_number
        self.dron_in = dron_in
        self.dron_out = dron_out
        self.who_took = who_took
        self.position_name = position_name

    def delet_fpv_flow_notice(self):
        data_set = MainFpvFlowOrder.objects.filter(id=self.dron_id)
        data_set.update(status=0,
                        position_name=self.position_name,
                        operator_name=self.who_took
                        )

    def to_storage_return(self):
        data_set = MainFpvFlowOrder.objects.filter(id=self.dron_id).values()[0]
        MainFpvFlowOrder.objects.filter(id=self.dron_id).update(
            status=2,
            position_name=self.position_name,
            operator_name=self.who_took
        )

        if data_set['id_for_storage'] is not None:
            FpvFlowStorage.objects.filter(id=data_set['id_for_storage']).update(status=1,
                                                                                who_took=self.who_took,
                                                                                position_name=self.position_name,
                                                                                id_for_flow=self.dron_id
                                                                                )
        else:
            FpvFlowStorage.objects.create(
                dron_name=data_set['dron_name'], serial=data_set['serial'], diagonal=data_set['diagonal'],
                dron_number=data_set['dron_number'], dron_in=datetime.now().date(),
                dron_out=data_set['dron_out'], id_for_flow=data_set['id']
            )


class RadioOrderLogic:

    def __init__(self, notice_id=None, supply_name=None, supply_price=None, serial_number=None, date_in=None):
        self.notice_id = notice_id
        self.supply_name = supply_name
        self.supply_price = supply_price
        self.serial_number = serial_number
        self.date_in = date_in

    def delete_notice(self):
        """delete notice from RadioModel"""
        RadioServiceModel.objects.filter(id=self.notice_id).update(date_out=datetime.now().date(), status=0)

    def create_radio_note(self):
        RadioServiceModel.objects.create(supply_name=self.supply_name, price=self.supply_price,
                                         serial_number=self.serial_number, date_in=self.date_in, )


class RifleOrderLogic:

    def __init__(self, notice_id=None, nickname=None, type_rifle=None, rifle_number=None, date_in_rifle=None,
                 produced_date=None):
        self.notice_id = notice_id
        self.nickname = nickname
        self.type_rifle = type_rifle
        self.rifle_number = rifle_number
        self.date_in_rifle = date_in_rifle
        self.produced_date = produced_date

    def add_notice(self):
        """add new notice"""
        RifleOrderModel.objects.create(Nickname=self.nickname, Type_rifle=self.type_rifle,
                                       Rifle_number=self.rifle_number, date_in=self.date_in_rifle,
                                       Produced_date=self.produced_date)

    def change_name(self):
        RifleOrderModel.objects.filter(id=self.notice_id).update(Nickname=self.nickname)

    def delete_notice(self):
        """delete notice from Rifle model"""
        RifleOrderModel.objects.filter(id=self.notice_id).update(date_out=datetime.now().date(), status=0)
