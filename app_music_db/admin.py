from django.contrib import admin
from .models import *

class SongAdmin(admin.ModelAdmin):
    model = Song
    list_per_page = 5000

admin.site.register(Song, SongAdmin)
admin.site.register(CdType)
admin.site.register(Comment)



