from django.contrib import admin
from django.contrib.sites.models import Site

from myapp.models import Userdata,Maps

from django.contrib.gis.admin import OSMGeoAdmin

admin.site.register(Userdata)

@admin.register(Maps)
class EntryAdmin(OSMGeoAdmin):
	default_lon=1400000
	default_lat=7495000
	default_zoom=12
