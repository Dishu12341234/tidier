from django.contrib import admin
from .models import BinsStats

class BinsStatsAdmin(admin.ModelAdmin):
    list_display = ('BinID', 'refreshStats', 'status') 

admin.site.register(BinsStats, BinsStatsAdmin)
