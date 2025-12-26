from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _


class Site(models.Model):
    name = models.CharField(max_length=255, unique=True)
    address = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ["name"]
        verbose_name = _("Площадка")
        verbose_name_plural = _("Площадки")

    def __str__(self) -> str:
        return self.name


class Workshop(models.Model):
    site = models.ForeignKey(
        Site, on_delete=models.CASCADE, related_name="workshops"
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["name"]
        unique_together = ("site", "name")
        verbose_name = _("Цех")
        verbose_name_plural = _("Цеха")

    def __str__(self) -> str:
        return f"{self.site}: {self.name}"


class EquipmentType(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        related_name="children",
        on_delete=models.SET_NULL,
    )
    description = models.TextField(blank=True)
    default_attributes = models.JSONField(
        default=list,
        blank=True,
        help_text=_("Список рекомендуемых характеристик для этого типа"),
    )

    class Meta:
        ordering = ["name"]
        verbose_name = _("Тип оборудования")
        verbose_name_plural = _("Типы оборудования")

    def __str__(self) -> str:
        return self.name


class Equipment(models.Model):
    name = models.CharField(max_length=255)
    inventory_number = models.CharField(max_length=100, unique=True)
    equipment_type = models.ForeignKey(
        EquipmentType, on_delete=models.PROTECT, related_name="equipment"
    )
    site = models.ForeignKey(
        Site, on_delete=models.PROTECT, related_name="equipment"
    )
    workshop = models.ForeignKey(
        Workshop, on_delete=models.PROTECT, related_name="equipment"
    )
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="equipment/", null=True, blank=True)
    attributes = models.JSONField(default=dict, blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="created_equipment",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        verbose_name = _("Оборудование")
        verbose_name_plural = _("Оборудование")

    def __str__(self) -> str:
        return f"{self.name} ({self.inventory_number})"

    def clean(self) -> None:
        if self.workshop and self.site and self.workshop.site_id != self.site_id:
            raise ValidationError(
                {"workshop": _("Цех должен принадлежать выбранной площадке")}
            )
        if self.attributes is not None and not isinstance(self.attributes, dict):
            raise ValidationError({"attributes": _("Характеристики должны быть словарём")})


class Passport(models.Model):
    equipment = models.ForeignKey(
        Equipment, on_delete=models.CASCADE, related_name="passports"
    )
    description = models.CharField(max_length=255, blank=True)
    file = models.FileField(upload_to="passports/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-uploaded_at"]
        verbose_name = _("Паспорт")
        verbose_name_plural = _("Паспорта")

    def __str__(self) -> str:
        return self.description or f"Паспорт {self.pk}"


class CartItem(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="cart_items"
    )
    equipment = models.ForeignKey(
        Equipment, on_delete=models.CASCADE, related_name="cart_items"
    )
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "equipment")
        ordering = ["-added_at"]
        verbose_name = _("Запись корзины")
        verbose_name_plural = _("Корзина")

    def __str__(self) -> str:
        return f"{self.user} → {self.equipment} x{self.quantity}"


class OrderRequest(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="order_requests",
    )
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=50, blank=True)
    comment = models.TextField(blank=True)
    items = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = _("Заявка")
        verbose_name_plural = _("Заявки")

    def __str__(self) -> str:
        return f"Заявка #{self.pk} от {self.name}"
