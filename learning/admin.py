from django.contrib import admin

from learning.models import Inscrit, InscritAdmin, Categorie, Document, Contact, HomeCoverImage


# Register your models here.


admin.site.register(Inscrit, InscritAdmin)
admin.site.register(Categorie)
admin.site.register(Document)
admin.site.register(Contact)
admin.site.register(HomeCoverImage)