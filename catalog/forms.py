from typing import Any, Dict

from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Equipment, EquipmentType, OrderRequest, Passport, Site, Workshop


class BootstrapFormMixin:
    def _apply_bootstrap(self) -> None:
        for field in self.fields.values():
            existing_classes = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = f"{existing_classes} form-control".strip()


class EquipmentForm(BootstrapFormMixin, forms.ModelForm):
    attributes = forms.JSONField(
        required=False,
        initial=dict,
        help_text=_("Укажите пары ключ/значение. Пусто — без доп. характеристик."),
    )

    class Meta:
        model = Equipment
        fields = [
            "name",
            "inventory_number",
            "equipment_type",
            "site",
            "workshop",
            "description",
            "image",
            "attributes",
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args: Any, **kwargs: Dict[str, Any]) -> None:
        super().__init__(*args, **kwargs)
        self._apply_bootstrap()
        self.fields["attributes"].widget.attrs.setdefault("rows", 4)
        equipment_type: EquipmentType | None = self.initial.get("equipment_type") or (
            self.instance.equipment_type if self.instance.pk else None
        )
        if equipment_type and equipment_type.default_attributes:
            for attr_name in equipment_type.default_attributes:
                self.fields["attributes"].initial.setdefault(attr_name, "")

    def clean_attributes(self) -> dict[str, Any]:
        attrs = self.cleaned_data.get("attributes") or {}
        if not isinstance(attrs, dict):
            raise forms.ValidationError(_("Характеристики должны быть словарём."))
        return attrs


class EquipmentSearchForm(BootstrapFormMixin, forms.Form):
    query = forms.CharField(label=_("Поиск"), required=False)
    equipment_type = forms.ModelChoiceField(
        queryset=EquipmentType.objects.all(), required=False, label=_("Тип")
    )
    site = forms.CharField(label=_("Площадка"), required=False)
    workshop = forms.CharField(label=_("Цех"), required=False)
    attribute_key = forms.CharField(label=_("Характеристика"), required=False)
    attribute_value = forms.CharField(label=_("Значение"), required=False)

    def __init__(self, *args: Any, **kwargs: Dict[str, Any]) -> None:
        super().__init__(*args, **kwargs)
        self._apply_bootstrap()
        for field in ("equipment_type",):
            self.fields[field].widget.attrs["class"] = "form-select"


class PassportForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Passport
        fields = ["description", "file"]

    def __init__(self, *args: Any, **kwargs: Dict[str, Any]) -> None:
        super().__init__(*args, **kwargs)
        self._apply_bootstrap()


class EquipmentTypeForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = EquipmentType
        fields = ["name", "parent", "description", "default_attributes"]

    def __init__(self, *args: Any, **kwargs: Dict[str, Any]) -> None:
        super().__init__(*args, **kwargs)
        self._apply_bootstrap()
        self.fields["parent"].required = False


class SiteForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Site
        fields = ["name", "address"]

    def __init__(self, *args: Any, **kwargs: Dict[str, Any]) -> None:
        super().__init__(*args, **kwargs)
        self._apply_bootstrap()


class WorkshopForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Workshop
        fields = ["site", "name", "description"]

    def __init__(self, *args: Any, **kwargs: Dict[str, Any]) -> None:
        super().__init__(*args, **kwargs)
        self._apply_bootstrap()
        self.fields["description"].widget.attrs.setdefault("rows", 2)


class CheckoutForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = OrderRequest
        fields = ["name", "email", "phone", "comment"]

    def __init__(self, *args: Any, **kwargs: Dict[str, Any]) -> None:
        super().__init__(*args, **kwargs)
        self._apply_bootstrap()
        self.fields["comment"].widget.attrs.setdefault("rows", 3)
        self.fields["name"].label = "Имя / организация"
        self.fields["email"].label = "Email"
        self.fields["phone"].label = "Телефон"
        self.fields["comment"].label = "Комментарий / условия поставки"
