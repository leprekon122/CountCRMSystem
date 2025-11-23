from django.db import models


class FpvFlowStorage(models.Model):
    objects = None
    dron_name = models.CharField(max_length=255, null=True, blank=True)
    serial = models.CharField(max_length=255, blank=True, null=True)
    diagonal = models.IntegerField(null=True, blank=True)
    dron_number = models.IntegerField(null=True, blank=True)
    dron_in = models.DateField(null=True, blank=True)
    dron_out = models.DateField(null=True, blank=True)
    who_took = models.CharField(null=True, blank=True)
    position_name = models.CharField(max_length=255, null=True, blank=True)
    status = models.IntegerField(null=True, blank=True, default=1)
    id_for_flow = models.IntegerField(null=True, blank=True)

    class Meta:
        verbose_name = 'FpvFlowStorage'
        verbose_name_plural = "FpvFlowStorage"


class MainFpvFlowOrder(models.Model):
    objects = None

    dron_name = models.CharField(max_length=255, null=True, blank=True)
    serial = models.CharField(max_length=255, blank=True, null=True)
    diagonal = models.IntegerField(null=True, blank=True)
    dron_number = models.IntegerField(null=True, blank=True)
    dron_in = models.DateField(null=True, blank=True)
    dron_out = models.DateField(null=True, blank=True)
    position_name = models.CharField(max_length=255, null=True, blank=True)
    operator_name = models.CharField(max_length=100, null=True, blank=True)
    crash_coordinates = models.CharField(max_length=50, null=True, blank=True)
    id_for_storage = models.IntegerField(null=True, blank=True)
    status = models.IntegerField(null=True, blank=True, default=1)

    class Meta:
        verbose_name = "MainFpvFlowOrder"
        verbose_name_plural = "MainFpvFlowOrder"


class MavicAutelStorage(models.Model):
    objects = None
    dron_name = models.CharField(max_length=255)
    dron_number = models.CharField(max_length=255)
    dron_in = models.DateField(null=True, blank=True)
    dron_out = models.DateField(null=True, blank=True)
    who_took = models.CharField(max_length=255, null=True, blank=True)
    position_name = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=255, default=1)
    id_for_flow = models.IntegerField(null=True, blank=True)
    supply_value = models.IntegerField(null=True, blank=True)
    number_of_document = models.CharField(max_length=255, null=True, blank=True, default=0)

    class Meta:
        verbose_name = "MavicAutelStorage"
        verbose_name_plural = "MavicAutelStorage"


class MavicAutelPositionFlow(models.Model):
    objects = None
    dron_name = models.CharField(max_length=255)
    dron_number = models.CharField(max_length=255)
    dron_in = models.DateField(null=True, blank=True)
    dron_out = models.DateField(null=True, blank=True)
    who_took = models.CharField(max_length=255, null=True, blank=True)
    position_name = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=255, default=1)
    id_for_storage = models.IntegerField(null=True, blank=True)
    crash_coordinates = models.CharField(max_length=50, null=True, blank=True)
    comment = models.TextField(null=True, blank=True, default=0)

    class Meta:
        verbose_name = "MavicAutelPositionFlow"
        verbose_name_plural = "MavicAutelPositionFlow"


class RifleOrderModel(models.Model):
    objects = None

    Nickname = models.CharField(max_length=120)
    Type_rifle = models.CharField(max_length=20)
    Rifle_number = models.CharField(max_length=50)
    Produced_date = models.CharField(max_length=4)
    status = models.CharField(default=1)
    date_in = models.DateField(auto_now=True)
    date_out = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = 'RifleOrderModel'
        verbose_name_plural = 'RifleOrderModel'


class RadioServiceModel(models.Model):
    objects = None

    supply_name = models.CharField(max_length=255)
    price = models.CharField(max_length=255)
    serial_number = models.CharField(max_length=255)
    date_in = models.DateField(auto_now=True)
    date_out = models.DateField(null=True, blank=True)
    status = models.CharField(default=1)

    class Meta:

        verbose_name = "RadioServiceModel"
        verbose_name_plural = "RadioServiceModel"
