from django.urls import path
import basketapp.views as basket

app_name = 'basketapp'

urlpatterns = [
    path('', basket.basket, name='list'),
    path('add/<int:pk>/', basket.basket_add, name='add'),
    path('remove/<int:pk>/', basket.basket_remove, name='remove'),
    path('edit/<int:pk>/<int:quantity>/', basket.basket_edit, name='edit'),
]
