from django.contrib import admin
from .models import Update
from tage_alslam_backend.messagesServises import sendMessage 
# Register your models here.


class UpdatesAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        is_new = obj.pk is None  # تحقق هل هو إدخال جديد
        super().save_model(request, obj, form, change)
        if is_new:
           
            itle = obj.title
            body = obj.description 

            sendMessage("test",itle,body)




admin.site.register(Update,UpdatesAdmin)