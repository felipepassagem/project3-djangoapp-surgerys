from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('quant', views.quant, name="quant"),
    path('add_surgery', views.add_surgery, name="add_surgery"),
    path('update_surgery/<surgery_id>', views.update_surgery, name="update_surgery"),
    path('add_implant', views.add_implant, name="add_implant"),
    path('stock', views.stock, name="stock"),
    path('delete_implant/<int:implant_id>', views.delete_implant, name="delete_implant"),
    path('update_implant/<int:implant_id>', views.update_implant, name="update_implant"),
    path('delete_surgery/<int:surgery_id>', views.delete_surgery, name="delete_surgery"),
    path('add_client', views.add_client, name="add_client"),
    path('client_list', views.client_list, name="client_list"),
    path('delete_client/<int:client_id>', views.delete_client, name="delete_client"),
    path('update_client/<int:client_id>', views.update_client, name="update_client"),
    
]