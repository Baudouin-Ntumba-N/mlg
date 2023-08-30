from django.contrib import admin

from learning import models


# Register your models here.


admin.site.register(models.Inscrit, models.InscritAdmin)
admin.site.register(models.Categorie)
admin.site.register(models.Document)
admin.site.register(models.HomeCoverImage)
admin.site.register(models.AboutUs)