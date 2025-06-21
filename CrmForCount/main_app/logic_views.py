from datetime import datetime
from .models import FpvFlowStorage


class CreateFpvStorageNotice:

    def __init__(self, dron_name=None, serial=None, diagonal=None, dron_number=None, dron_in=None, dron_out=None,
                 who_took=None, position_name=None):
        self.dron_name = dron_name
        self.serial = serial
        self.diagonal = diagonal
        self.dron_number = dron_number
        self.dron_in = dron_in
        self.dron_out = dron_out
        self.who_took = who_took
        self.position_name = position_name

    @property
    def create_notice(self):
        """func creating new add"""
        FpvFlowStorage.objects.create(dron_name=self.dron_name, serial=self.serial, diagonal=self.diagonal,
                                      dron_number=self.dron_number, dron_in=self.dron_in, dron_out=self.dron_out,
                                      who_took=self.who_took, position_name=self.position_name)


class CreateDatasets:
    """Class for creating datasets on order pages """

    def __init__(self, id=None, dron_out=None, who_took=None, position_name=None):
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

    def LowDateFilter(self):
        """Date filter Up to low """
        set = FpvFlowStorage.objects.values().order_by('dron_in')
        data = {"model": set,
                'stat': 1
                }
        return data

    def FilterByDateUp(self):
        """Date filter Low to Up """
        set = FpvFlowStorage.objects.values().order_by('-dron_in')
        data = {"model": set,
                'stat': 2
                }
        return data
