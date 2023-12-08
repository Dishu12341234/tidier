from django.db import models

class BinsStats(models.Model):
    BinID = models.CharField(max_length=6, unique=True)
    status = models.CharField(max_length=4, blank=True,null=True)
    refreshStats = models.CharField(max_length=4, blank=True)
    lastRefresh = models.DateField(blank=True)
    fillUp = models.IntegerField(blank=True)
    Lat = models.FloatField(blank=True, null=True)
    Lon = models.FloatField(blank=True, null=True)
    Area = models.CharField(max_length=200, blank=True)
    City = models.CharField(max_length=200,blank=True)