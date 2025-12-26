from rest_framework.routers import DefaultRouter

from .api import (
    CartItemViewSet,
    EquipmentTypeViewSet,
    EquipmentViewSet,
    PassportViewSet,
    SiteViewSet,
    WorkshopViewSet,
)

router = DefaultRouter()
router.register(r"equipment-types", EquipmentTypeViewSet, basename="equipment-type")
router.register(r"sites", SiteViewSet, basename="site")
router.register(r"workshops", WorkshopViewSet, basename="workshop")
router.register(r"equipment", EquipmentViewSet, basename="equipment")
router.register(r"passports", PassportViewSet, basename="passport")
router.register(r"cart", CartItemViewSet, basename="cart")

urlpatterns = router.urls

