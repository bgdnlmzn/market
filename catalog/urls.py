from django.urls import path

from . import views

app_name = "catalog"

urlpatterns = [
    path("", views.EquipmentListView.as_view(), name="equipment_list"),
    path(
        "equipment/<int:pk>/",
        views.EquipmentDetailView.as_view(),
        name="equipment_detail",
    ),
    path(
        "equipment/create/",
        views.EquipmentCreateView.as_view(),
        name="equipment_create",
    ),
    path(
        "equipment/<int:pk>/edit/",
        views.EquipmentUpdateView.as_view(),
        name="equipment_update",
    ),
    path(
        "equipment/<int:pk>/delete/",
        views.EquipmentDeleteView.as_view(),
        name="equipment_delete",
    ),
    path(
        "types/create/",
        views.EquipmentTypeCreateView.as_view(),
        name="equipment_type_create",
    ),
    path(
        "sites/create/",
        views.SiteCreateView.as_view(),
        name="site_create",
    ),
    path(
        "workshops/create/",
        views.WorkshopCreateView.as_view(),
        name="workshop_create",
    ),
    path(
        "equipment/<int:pk>/passport/",
        views.upload_passport,
        name="passport_upload",
    ),
    path(
        "equipment/<int:pk>/add-to-cart/",
        views.add_to_cart,
        name="add_to_cart",
    ),
    path("cart/", views.CartListView.as_view(), name="cart"),
    path(
        "cart/<int:pk>/remove/",
        views.remove_from_cart,
        name="remove_from_cart",
    ),
    path("cart/checkout/", views.checkout, name="checkout"),
]

