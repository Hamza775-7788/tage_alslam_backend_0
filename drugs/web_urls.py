from django.urls import path, include
from .web import add_drug,drug_list,edit_drug,delete_drug

from .views import (

    get_un_active_drugs,

)


urlpatterns = [
    
    path('', drug_list, name='drug_list'),
    path('add/', add_drug, name='add_drug'),
    path('edit/<int:id>/', edit_drug, name='edit_drug'),
    path('delete/<int:id>/', delete_drug, name='delete_drug'),

]
