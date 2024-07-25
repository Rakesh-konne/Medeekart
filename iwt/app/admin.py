from django.contrib import admin
from . models import Customer,Medicine,Cart
# Register your models here.


admin.site.register(Medicine)
@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display=['id','user','locality','city','state']


@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display=['id','user','medicine','quantity']

