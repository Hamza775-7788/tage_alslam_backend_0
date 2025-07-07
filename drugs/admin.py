from django.contrib import admin
from . import models
# Register your models here.
from tage_alslam_backend.messagesServises import sendMessage


newDrugTitle = "صنف جديد" 

class DrugAdmin(admin.ModelAdmin):
    
    def save_model(self, request, obj, form, change):
        is_new = obj.pk is None  # تحقق هل هو إدخال جديد
        super().save_model(request, obj, form, change)
        if is_new:
            name = obj.name_ar 

            sendMessage("test",newDrugTitle,name)

class OfferAdmin(admin.ModelAdmin):
    
    def save_model(self, request, obj, form, change):
        is_new = obj.pk is None  # تحقق هل هو إدخال جديد
        super().save_model(request, obj, form, change)
        if is_new:
            title = obj.title
            body = obj.description 

            sendMessage("admin",title,body)
admin.site.register(models.DrugCategory)
admin.site.register(models.Drug,DrugAdmin)
admin.site.register(models.DrugUnits)
admin.site.register(models.Order)
admin.site.register(models.OrderItem)
admin.site.register(models.Offer,OfferAdmin)


