from django.urls import path
from .views import ItemAPI, CategoryAPI

urlpatterns = [
    path('item/', ItemAPI.as_view(),
         name='item-api'),
    path('category/', CategoryAPI.as_view(),
         name='category-api'),
]
