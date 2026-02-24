from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("kerdes/add/", views.add_kerdes),
    path("kerdes/add/addrecord", views.add_kerdes_record),
    path("kerdes/update/<int:id>", views.update_kerdes),
    path("kerdes/update/updaterecord/<int:id>", views.update_kerdes_record),
    path("kerdes/delete/<int:id>", views.delete_kerdes),
    path("valasz/add/<int:kerdes_id>", views.add_valasz),
    path("valasz/add/addrecord/<int:kerdes_id>", views.add_valasz_record),
    path("valasz/update/<int:id>", views.update_valasz),
    path("valasz/update/updaterecord/<int:id>", views.update_valasz_record),
    path("valasz/delete/<int:id>", views.delete_valasz),
    path("listaelem/add/<int:kerdes_id>", views.add_listaelem),
    path("listaelem/add/addrecord/<int:kerdes_id>", views.add_listaelem_record),
    path("listaelem/delete/<int:id>", views.delete_listaelem),
]
