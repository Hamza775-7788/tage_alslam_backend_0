from django import forms
from .models import Drug 


class DrugForm(forms.ModelForm):
    class Meta:
        model = Drug
        fields = '__all__'  # أو حدد الحقول المطلوبة مثلاً: ['name', 'description', 'price']
