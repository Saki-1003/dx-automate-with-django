from django.urls import path
from . import views

urlpatterns = [
  path('stocks/', views.stocks, name='stocks'),
  path('stock_detail/<int:id>/', views.stock_detail, name='stock_detail'),
  path('stock_autocomplete/', views.StockAutocomplete.as_view(), name='stock_autocomplete'),
]