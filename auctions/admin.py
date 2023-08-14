from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Bids)
admin.site.register(models.Listings)
admin.site.register(models.Comment)
admin.site.register(models.category)
#admin.site.register(models.watchlist)