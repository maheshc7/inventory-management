from django.urls import path
from .views import ItemDashboardAPI

urlpatterns = [
    path('item-dashboard/', ItemDashboardAPI.as_view(),
         name='item-dashboard-api'),
]
