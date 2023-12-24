from django.contrib import admin
from .models import BinsStats,BINQRs

class BinsStatsAdmin(admin.ModelAdmin):
    list_display = ('BinID', 'refreshStats', 'status') 
class BINQRsAdmin(admin.ModelAdmin):
    list_display = ('data',)
admin.site.register(BinsStats, BinsStatsAdmin)
admin.site.register(BINQRs, BINQRsAdmin)
