from django.contrib import admin

from .models import CartItem, Equipment, EquipmentType, Passport, Site, Workshop


@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    list_display = ("name", "address")
    search_fields = ("name", "address")


@admin.register(Workshop)
class WorkshopAdmin(admin.ModelAdmin):
    list_display = ("name", "site", "description")
    list_filter = ("site",)
    search_fields = ("name",)


class PassportInline(admin.TabularInline):
    model = Passport
    extra = 0
    fields = ("description", "file")
    readonly_fields = ("uploaded_at",)


@admin.register(EquipmentType)
class EquipmentTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "parent")
    search_fields = ("name", "description")
    list_filter = ("parent",)


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "inventory_number",
        "equipment_type",
        "site",
        "workshop",
        "image",
        "created_by",
        "updated_at",
    )
    search_fields = ("name", "inventory_number", "description")
    list_filter = ("equipment_type", "site", "workshop")
    autocomplete_fields = ("equipment_type", "site", "workshop")
    inlines = (PassportInline,)
    readonly_fields = ("created_at", "updated_at")


@admin.register(Passport)
class PassportAdmin(admin.ModelAdmin):
    list_display = ("equipment", "description", "uploaded_at")
    search_fields = ("equipment__name", "description")
    list_filter = ("uploaded_at",)


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ("user", "equipment", "quantity", "added_at")
    list_filter = ("user",)
    search_fields = ("user__username", "equipment__name")
    raw_id_fields = ("user", "equipment")
