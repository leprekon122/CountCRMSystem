from django.db.models import Sum, Q

from .models import FpvFlowStorage, MainFpvFlowOrder, MavicAutelStorage, MavicAutelPositionFlow, RifleOrderModel, \
    RadioServiceModel, RadioServicePositionModel, BatteryStorageOrderModel, BatteryPositionOrderModel, BatteryTrash, \
    UserOrderPermission
from datetime import datetime
from django.contrib.auth.models import User


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
                 adaptive_mavic=None, start_num=None, end_num=None, adaptive_document=None, status=None):
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
        self.status = status

    def search_by_status_mav_storage(self):
        """function for filtering by status in Mavic/Autel storage page"""
        dataset = MavicAutelStorage.objects.filter(status=self.status).values()
        total_value = MavicAutelStorage.objects.filter(status=self.status).aggregate(Sum('supply_value'))[
            'supply_value__sum']

        data = {'model': dataset,
                'total_value': total_value
                }
        return data

    def adaptive_search_by_dron_num_flow_order(self):
        """crating dataset for  searching by drone num """
        dataset = MavicAutelPositionFlow.objects.filter(dron_number__icontains=self.drone_num).values()
        data = {'model': dataset}
        return data

    def adaptive_search_by_dron_num(self):
        """crating dataset for  searching by drone num """
        dataset = MavicAutelStorage.objects.filter(dron_number__icontains=self.drone_num).values()
        total_value = \
            MavicAutelStorage.objects.filter(dron_number__icontains=self.drone_num).aggregate(Sum('supply_value'))[
                'supply_value__sum']
        data = {'model': dataset,
                'total_value': total_value
                }
        return data

    def create_adaptive_document_dataset(self):
        """function for document number adaptive filter in MAvicAutel Storage"""
        dataset = MavicAutelStorage.objects.filter(number_of_document__icontains=self.adaptive_document).values()
        total_value = MavicAutelStorage.objects.filter(number_of_document__icontains=self.adaptive_document).aggregate(
            Sum('supply_value'))['supply_value__sum']
        data = {'model': dataset,
                'total_value': total_value
                }
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
        total_value = \
            MavicAutelStorage.objects.filter(dron_name__icontains=self.adaptive_mavic).aggregate(Sum('supply_value'))[
                'supply_value__sum']
        data = {"model": data_set,
                'total_value': total_value
                }
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
        total_value = RadioServiceModel.objects.aggregate(Sum('price'))['price__sum']
        data = {"model": RadioServiceModel.objects.values().order_by('-id'),
                'total_value': total_value
                }

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

    def __init__(self, notice_id=None, supply_name=None, supply_price=None, serial_number=None, date_in=None,
                 status=None):
        self.notice_id = notice_id
        self.supply_name = supply_name
        self.supply_price = supply_price
        self.serial_number = serial_number
        self.date_in = date_in
        self.status = status

    def order_by_status(self):
        """function for creating order by status"""
        data_set = RadioServiceModel.objects.filter(status=self.status).values()
        total_value = RadioServiceModel.objects.filter(status=self.status).aggregate(Sum('price'))['price__sum']

        data = {'model': data_set,
                'total_value': total_value
                }
        return data

    def delete_notice(self):
        """delete notice from RadioModel"""
        RadioServiceModel.objects.filter(id=self.notice_id).update(date_out=datetime.now().date(), status=0)

    def create_radio_note(self):
        RadioServiceModel.objects.create(supply_name=self.supply_name, price=self.supply_price,
                                         serial_number=self.serial_number, date_in=self.date_in, )


class RadioSupplyPosition:

    def __init__(self, notice_id=None, supply_name=None, supply_price=None, serial_number=None, date_in=None,
                 storage_id=None, who_took=None, position_name=None, coordinates=None):
        self.notice_id = int(notice_id) if notice_id is not None else None
        self.supply_name = supply_name
        self.supply_price = supply_price
        self.serial_number = serial_number
        self.date_in = date_in
        self.storage_id = int(storage_id) if storage_id is not None else None
        self.who_took = who_took,
        self.position_name = position_name
        self.coordinates = coordinates

    def create_article(self):
        """create new article"""
        check_id = RadioServiceModel.objects.filter(id=self.storage_id).values()[0]['id_for_position']
        if check_id is None:
            RadioServiceModel.objects.filter(id=self.storage_id).update(status=0, who_took=self.who_took,
                                                                        position_name=self.position_name,
                                                                        date_out=datetime.now())
            dataset = \
                RadioServiceModel.objects.filter(id=self.storage_id).values('supply_name', 'price', 'serial_number',
                                                                            'date_in')[0]

            RadioServicePositionModel.objects.create(supply_name=dataset['supply_name'], price=dataset['price'],
                                                     serial_number=dataset['serial_number'], date_in=dataset['date_in'],
                                                     id_for_storage=self.storage_id,
                                                     )
        else:
            RadioServicePositionModel.objects.filter(id=check_id).update(status=1)
            RadioServiceModel.objects.filter(id=self.storage_id).update(status=0, who_took=self.who_took,
                                                                        position_name=self.position_name,
                                                                        date_out=datetime.now()
                                                                        )

    def delete_article(self):
        RadioServicePositionModel.objects.filter(id=self.notice_id).update(status=0, who_took=self.who_took,
                                                                           position_name=self.coordinates,
                                                                           date_out=datetime.now())

    def create_dataset_main(self):
        """create main dataset for page"""
        dataset = RadioServicePositionModel.objects.values()
        data = {'model': dataset}
        return data

    def return_to_storage(self):
        """return to storage article"""
        return_id = RadioServicePositionModel.objects.filter(id=self.storage_id).values()[0]['id_for_storage']

        RadioServicePositionModel.objects.filter(id=self.storage_id).update(status=2, id_for_storage=return_id)
        RadioServiceModel.objects.filter(id=return_id).update(status=1, id_for_position=self.storage_id)


class RifleOrderLogic:
    """class of rifle order logic """

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


class StatisticsLogic:

    def __init__(self, note_id=None):
        self.note_id = note_id

    def stat_data_mavic_autel(self):
        """func for main data report"""
        in_storage = len(MavicAutelStorage.objects.filter(status=1).values())
        in_position = len(MavicAutelPositionFlow.objects.filter(status=1).values())
        all_period_taking = len(MavicAutelStorage.objects.filter(status=0).values())
        all_destroy = len(MavicAutelPositionFlow.objects.filter(status=0).values())

        in_storage_mav = len(MavicAutelStorage.objects.filter(
            Q(status=1) |
            Q(dron_name__contains='DJI Mavic 3 Thermal') |
            Q(dron_name__contains='DJI Mavic 3(Thermal)') |
            Q(dron_name__contains='DJI Matrice 4T') |
            Q(dron_name__contains='БпАК DJI MAvic 3T') |
            Q(dron_name__contains='Mavic 3E (Enterprise)') |
            Q(dron_name__contains='БпАК Autel EVO MAX 4T') |
            Q(dron_name__contains='Autel EVO MAX 4T') |
            Q(dron_name__contains='БПАК DJI MATRICE 4T') |
            Q(dron_name__contains='DJi Mavic 3 PRO (DJI RS)')
        ).values())

        in_position_mav = len(MavicAutelPositionFlow.objects.filter(Q(status=1) |
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
                                                                    ).values())

        taking_for_all_per_mavic = len(MavicAutelStorage.objects.filter(Q(status=0) |
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
                                                                        ).values())

        all_destroy_mav = len(MavicAutelPositionFlow.objects.filter(Q(status=0) |
                                                                    Q(dron_name__contains='DJi  Mavic 3 Thermal') |
                                                                    Q(dron_name__contains='DJI  Mavic 3(Thermal)') |
                                                                    Q(dron_name__contains='DJI  Matrice 4T') |
                                                                    Q(dron_name__contains='БпАК DJI MAvic 3T') |
                                                                    Q(dron_name__contains='Mavic 3E (Enterprise)') |
                                                                    Q(dron_name__contains='БпАК Autel EVO MAX 4T') |
                                                                    Q(dron_name__contains='Autel EVO MAX 4T') |
                                                                    Q(dron_name__contains='БПАК DJI MATRICE 4T') |
                                                                    Q(dron_name__contains='DJi Mavic 3 PRO (DJI RS)') |
                                                                    Q(dron_name__contains='DJI Mavic 3') |
                                                                    Q(dron_name__contains='Autel EVO Max 4N')

                                                                    ).values())

        data = {'in_storage': in_storage,
                'in_position': in_position,
                'all_period_taking': all_period_taking,
                'all_destroy': all_destroy,
                'in_storage_mav': in_storage_mav,
                'in_position_mav': in_position_mav,
                'taking_for_all_per_mavic': taking_for_all_per_mavic,
                'all_destroy_mav': all_destroy_mav
                }
        return data


class FilterForMAvicAutelPosition:

    def __init__(self, status=None):
        self.status = status

    def status_on_position(self):
        """function fot filtering by status on position flow page"""
        data_set = MavicAutelPositionFlow.objects.filter(status=self.status).values()
        data = {'model': data_set}
        return data


class BatteryStorageOrderLogic:
    """class dor business logic in battery_storage_order.html"""

    def __init__(self, battery_type=None, price=0, quantities=0, date_in=None, doc_num=None, notice_id=None,
                 who_took=None, position_name=None):
        self.battery_type = battery_type
        self.price = int(price)
        self.quantities = int(quantities)
        self.date_in = date_in
        self.doc_num = doc_num
        self.notice_id = notice_id
        self.who_took = who_took
        self.position_name = position_name

    def create_main_data_set(self):
        """create main data for page """
        data_set = BatteryStorageOrderModel.objects.values()
        total_value = BatteryStorageOrderModel.objects.all().aggregate(Sum('total_price'))['total_price__sum']

        data = {'model': data_set,
                'total_value': total_value,
                }

        return data

    def create_notice(self):
        """create new article"""
        total_price = self.quantities * self.price
        BatteryStorageOrderModel.objects.create(battery_type=self.battery_type, price=self.price,
                                                quantities=self.quantities, total_price=total_price,
                                                date_in=self.date_in, doc_num=self.doc_num)

    def filter_by_name(self):
        """filter by battery type"""

        data_set = BatteryStorageOrderModel.objects.filter(battery_type__contains=self.battery_type).values()

        data_set = {'model': data_set}
        return data_set

    def send_to_position(self):
        """function for transfer to position order"""
        data_set = BatteryStorageOrderModel.objects.filter(id=self.notice_id).values()[0]
        BatteryStorageOrderModel.objects.filter(id=self.notice_id).update(who_took=self.who_took,
                                                                          position_name=self.position_name,
                                                                          quantities=data_set[
                                                                                         'quantities'] - self.quantities,
                                                                          status=0)

        BatteryPositionOrderModel.objects.create(battery_type=data_set['battery_type'],
                                                 price=data_set['price'],
                                                 total_price=data_set['price'] * self.quantities,
                                                 quantities=self.quantities,
                                                 )


class BatteryPositionOrderLogic:
    """class dor business logic in battery_storage_order.html"""

    def __init__(self, battery_type=None, price=0, quantities=0, date_in=None, doc_num=None, notice_id=None,
                 who_took=None, position_name=None, status=None):
        self.battery_type = battery_type
        self.price = int(price)
        self.quantities = int(quantities)
        self.date_in = date_in
        self.doc_num = doc_num
        self.notice_id = notice_id
        self.who_took = who_took
        self.position_name = position_name
        self.status = status

    def filter_by_status(self):
        """function for filtering by status"""

        if int(self.status) == 1:
            data_set = BatteryPositionOrderModel.objects.filter(quantities__gt=0).values()
            total_value = \
                BatteryPositionOrderModel.objects.filter(quantities__gt=0).aggregate(
                    Sum('total_price'))[
                    'total_price__sum']
            data = {
                'model': data_set,
                'total_value': total_value}
            return data

        elif int(self.status) == 0:
            data_set = BatteryPositionOrderModel.objects.filter(quantities=0).values()
            total_value = \
                BatteryPositionOrderModel.objects.filter(quantities=0).aggregate(
                    Sum('total_price'))[
                    'total_price__sum']
            data = {
                'model': data_set,
                'total_value': total_value}
            return data

    def filter_by_batt_type(self):
        """function for searching by batt name type"""
        data_set = BatteryPositionOrderModel.objects.filter(battery_type__icontains=self.battery_type).values()
        total_value = \
            BatteryPositionOrderModel.objects.filter(battery_type__icontains=self.battery_type).aggregate(
                Sum('total_price'))[
                'total_price__sum']
        data = {'model': data_set,
                'total_value': total_value,
                }
        return data

    def create_main_data_set(self):
        """create main data for page battery position """
        data_set = BatteryPositionOrderModel.objects.values()
        total_value = BatteryPositionOrderModel.objects.all().aggregate(Sum('total_price'))['total_price__sum']

        dji_3_trash = BatteryTrash.objects.filter(
            Q(battery_type__icontains='dji inelegance flight battery for mavic 3') |
            Q(battery_type__icontains='dji 3') |
            Q(battery_type__icontains='dji inelegance flight battery for. Mavic 3'))

        autel_bat = BatteryTrash.objects.filter(
            Q(battery_type__icontains='Аккомулятори Autel Evo Max 4T') |
            Q(battery_type__icontains='Autel')
        )

        matrice_4 = BatteryTrash.objects.filter(
            Q(battery_type__icontains='Dji Matrice 4 Serie Battery') |
            Q(battery_type__icontains='dji 4') |
            Q(battery_type__icontains='matrice 4')
        )

        s5p1_2_5000_mah = BatteryTrash.objects.filter(
            battery_type__icontains='Збірка аккомуляторів 5s1p (2*5000 mah)')

        s5p1_6000mah = BatteryTrash.objects.filter(
            battery_type__icontains='Збірка аккомуляторів 5s1p (6000 mah)')

        s4p1_2_5800mah = BatteryTrash.objects.filter(
            Q(battery_type__icontains='Збірка аккомуляторів (4s1p 2* 5800 mah)') |
            Q(battery_type__icontains='4s2p ( 2*5800 mah)'))

        data = {'model': data_set,
                'total_value': total_value,
                'dji_3_trash': len(dji_3_trash),
                'Autel': len(autel_bat),
                'matrice_4': len(matrice_4),
                's5p1_2_5000_mah': len(s5p1_2_5000_mah),
                's5p1_6000mah': len(s5p1_6000mah),
                's4p1_2_5800mah': len(s4p1_2_5800mah)
                }

        return data

    def destroy_logic(self):
        """func for managing destroying process"""
        data_set = BatteryPositionOrderModel.objects.filter(id=self.notice_id).values()[0]
        quant = BatteryPositionOrderModel.objects.filter(id=self.notice_id).values('quantities')[0]['quantities']
        BatteryPositionOrderModel.objects.filter(id=self.notice_id).update(quantities=quant - 1)
        BatteryTrash.objects.create(battery_type=data_set['battery_type'], price=data_set['price'])


class PermissionOnView:

    def __init__(self, username):
        self.username = username

    def render_username(self):
        username = User.objects.filter(username=self.username).values('id')[0]['id']
        data_set = UserOrderPermission.objects.filter(id=username).values('username_id')
        return data_set
