
from django.urls import path, include
from .views import UpdatesViewset
from rest_framework.routers import DefaultRouter




router = DefaultRouter()
router.register(r'updates', UpdatesViewset)
urlpatterns = [
    
    path('', include(router.urls)),


]
