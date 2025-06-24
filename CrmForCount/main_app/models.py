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

    class Meta:
        verbose_name = "MainFpvFlowOrder"
        verbose_name_plural = "MainFpvFlowOrder"

