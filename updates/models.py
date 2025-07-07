from django.db import models

# Create your models here.
class Update(models.Model):
    title = models.CharField(max_length=100,verbose_name="عنوان التحديث")
    description = models.TextField(blank=True, null=True,verbose_name="الوصف")
    version  = models.CharField(max_length=100,verbose_name="الاصدار")
    file = models.FileField(upload_to='updates/', blank=False, null=False,verbose_name="الملف")
    is_active = models.BooleanField (default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.version} - ({self.created_at})"