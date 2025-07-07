from django.urls import path, include
from .web import add_drug,drug_list,edit_drug,delete_drug
from rest_framework.routers import DefaultRouter
from .views import (
    DrugViewSet,
    DrugCategoryViewSet,
    DrugUnitsViewSet,
    OrderViewSet,
    OfferViewSet,
    DrugMostOrderedViewSet,
    get_un_active_drugs,

)

router = DefaultRouter()
router.register(r'drug-most-ordered', DrugMostOrderedViewSet,basename='drug-most-ordered')
router.register(r'drugs', DrugViewSet)
router.register(r'categories', DrugCategoryViewSet)
router.register(r'units', DrugUnitsViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'offer', OfferViewSet)



urlpatterns = [
    
    path('', include(router.urls)),
    path("un-active/",get_un_active_drugs,name="unactive"),
    path('d/', drug_list, name='drug_list'),
    path('add/', add_drug, name='add_drug'),
    path('edit/<int:id>/', edit_drug, name='edit_drug'),
    path('delete/<int:id>/', delete_drug, name='delete_drug'),

]
