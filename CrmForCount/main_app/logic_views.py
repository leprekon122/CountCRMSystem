from .models import FpvFlowStorage, MainFpvFlowOrder, MavicAutelStorage, MavicAutelPositionFlow
from datetime import datetime


class CreateMavicAutelStorageNotice:
    '''class for creating  notice in MavicAutelStorage model'''

    def __init__(self, id=None, dron_name=None, dron_number=None, dron_in=None, dron_out=None,
                 who_took=None, position_name=None):
        self.id = id
        self.dron_name = dron_name
        self.dron_number = dron_number
        self.dron_in = dron_in
        self.dron_out = dron_out
        self.who_took = who_took
        self.position_name = position_name

    def create_mavic_autel_storage(self):
        MavicAutelStorage.objects.create(
            dron_name=self.dron_name,
            dron_number=self.dron_number,
            dron_in=self.dron_in,
            dron_out=self.dron_out,
            who_took=self.who_took,
            position_name=self.position_name
        )

    def update_notice(self=None):
        '''func for creating update request'''

        MavicAutelStorage.objects.filter(id=self.id).update(status=0,
                                                            who_took=self.who_took,
                                                            position_name=self.position_name,
                                                            dron_out=self.dron_out)

        background_set = MavicAutelStorage.objects.filter(id=self.id).values()[0]

        MavicAutelPositionFlow.objects.create(dron_name=background_set['dron_name'],
                                              dron_number=background_set['dron_number'],
                                              dron_in=background_set['dron_in'],
                                              dron_out=background_set['dron_out'],
                                              who_took=background_set['who_took'],
                                              position_name=background_set['position_name'])


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

    def __init__(self, id=None, dron_out=None, who_took=None, position_name=None, drone_name=None, dron_num=None):
        self.drone_name = drone_name
        self.drone_num = dron_num
        self.dron_out = dron_out
        self.who_took = who_took
        self.position_name = position_name
        self.id = id

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
                                                               position_name=self.position_name
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
        data = {
            "model": MavicAutelStorage.objects.values()
        }
        return data

    def mavic_autel_flow_position(self):
        """func for making base dataset for Mavic/Autel position flow page """

        data = {"model": MavicAutelPositionFlow.objects.values()}

        return data