from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .forms import (
    EquipmentForm,
    EquipmentSearchForm,
    EquipmentTypeForm,
    PassportForm,
    SiteForm,
    WorkshopForm,
    CheckoutForm,
)
from .models import CartItem, Equipment, EquipmentType, Passport, Site, Workshop


class EquipmentListView(ListView):
    model = Equipment
    paginate_by = 10
    template_name = "catalog/equipment_list.html"

    def get_queryset(self):
        queryset = (
            super()
            .get_queryset()
            .select_related("equipment_type", "site", "workshop")
            .prefetch_related("passports")
        )
        self.search_form = EquipmentSearchForm(self.request.GET or None)
        if self.search_form.is_valid():
            data = self.search_form.cleaned_data
            if data.get("query"):
                queryset = queryset.filter(
                    Q(name__icontains=data["query"])
                    | Q(description__icontains=data["query"])
                    | Q(inventory_number__icontains=data["query"])
                )
            if data.get("equipment_type"):
                queryset = queryset.filter(equipment_type=data["equipment_type"])
            if data.get("site"):
                queryset = queryset.filter(site__name__icontains=data["site"])
            if data.get("workshop"):
                queryset = queryset.filter(
                    workshop__name__icontains=data["workshop"]
                )
            if data.get("attribute_key") and data.get("attribute_value"):
                queryset = queryset.filter(
                    attributes__contains={
                        data["attribute_key"]: data["attribute_value"]
                    }
                )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = getattr(self, "search_form", EquipmentSearchForm())
        return context


class EquipmentDetailView(DetailView):
    model = Equipment
    template_name = "catalog/equipment_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["passport_form"] = PassportForm()
        return context


class SellerPermissionMixin(PermissionRequiredMixin):
    """Allow staff/superuser regardless of group, otherwise check perms (e.g., seller)."""

    def has_permission(self):
        user = self.request.user
        if not user.is_authenticated:
            return False
        if user.is_superuser or user.is_staff:
            return True
        return super().has_permission()


class OwnerPermissionMixin(SellerPermissionMixin):
    owner_field = "created_by"

    def has_permission(self):
        if not super().has_permission():
            return False
        user = self.request.user
        if user.is_superuser or user.is_staff:
            return True
        obj = self.get_object()
        return getattr(obj, self.owner_field, None) == user


class EquipmentCreateView(SellerPermissionMixin, LoginRequiredMixin, CreateView):
    model = Equipment
    form_class = EquipmentForm
    template_name = "catalog/equipment_form.html"
    permission_required = "catalog.add_equipment"
    raise_exception = True

    def get_success_url(self):
        return reverse("catalog:equipment_detail", args=[self.object.pk])

    def form_valid(self, form):
        if not self.request.user.is_superuser and not self.request.user.is_staff and not self.request.user.groups.filter(name="seller").exists():
            messages.error(self.request, "У вас нет прав на добавление оборудования.")
            return redirect("catalog:equipment_list")
        form.instance.created_by = self.request.user
        messages.success(self.request, "Оборудование добавлено.")
        return super().form_valid(form)


class EquipmentUpdateView(OwnerPermissionMixin, LoginRequiredMixin, UpdateView):
    model = Equipment
    form_class = EquipmentForm
    template_name = "catalog/equipment_form.html"
    permission_required = "catalog.change_equipment"
    raise_exception = True

    def get_success_url(self):
        return reverse("catalog:equipment_detail", args=[self.object.pk])

    def form_valid(self, form):
        messages.success(self.request, "Изменения сохранены.")
        return super().form_valid(form)


class EquipmentDeleteView(OwnerPermissionMixin, LoginRequiredMixin, DeleteView):
    model = Equipment
    template_name = "catalog/equipment_confirm_delete.html"
    success_url = reverse_lazy("catalog:equipment_list")
    permission_required = "catalog.delete_equipment"
    raise_exception = True

    def delete(self, request, *args, **kwargs):
        messages.info(request, "Оборудование удалено.")
        return super().delete(request, *args, **kwargs)


class EquipmentTypeCreateView(SellerPermissionMixin, LoginRequiredMixin, CreateView):
    model = EquipmentType
    form_class = EquipmentTypeForm
    template_name = "catalog/simple_form.html"
    permission_required = "catalog.add_equipmenttype"
    raise_exception = True
    success_url = reverse_lazy("catalog:equipment_create")

    def form_valid(self, form):
        messages.success(self.request, "Тип оборудования создан.")
        return super().form_valid(form)


class SiteCreateView(SellerPermissionMixin, LoginRequiredMixin, CreateView):
    model = Site
    form_class = SiteForm
    template_name = "catalog/simple_form.html"
    permission_required = "catalog.add_site"
    raise_exception = True
    success_url = reverse_lazy("catalog:equipment_create")

    def form_valid(self, form):
        messages.success(self.request, "Площадка создана.")
        return super().form_valid(form)


class WorkshopCreateView(SellerPermissionMixin, LoginRequiredMixin, CreateView):
    model = Workshop
    form_class = WorkshopForm
    template_name = "catalog/simple_form.html"
    permission_required = "catalog.add_workshop"
    raise_exception = True
    success_url = reverse_lazy("catalog:equipment_create")

    def form_valid(self, form):
        messages.success(self.request, "Цех создан.")
        return super().form_valid(form)


@login_required
def upload_passport(request: HttpRequest, pk: int) -> HttpResponse:
    equipment = get_object_or_404(Equipment, pk=pk)
    form = PassportForm(request.POST, request.FILES)
    if form.is_valid():
        try:
            passport: Passport = form.save(commit=False)
            passport.equipment = equipment
            passport.save()
            messages.success(request, "Паспорт успешно загружен.")
        except Exception:
            messages.error(request, "Не удалось сохранить паспорт. Попробуйте позже.")
    else:
        messages.error(request, "Не удалось загрузить паспорт. Проверьте файл.")
    return redirect("catalog:equipment_detail", pk=pk)


@login_required
def add_to_cart(request: HttpRequest, pk: int) -> HttpResponse:
    equipment = get_object_or_404(Equipment, pk=pk)
    quantity_str = request.POST.get("quantity", "1")
    try:
        quantity = max(1, int(quantity_str))
    except ValueError:
        quantity = 1
    item, created = CartItem.objects.get_or_create(
        user=request.user,
        equipment=equipment,
        defaults={"quantity": quantity},
    )
    if not created:
        item.quantity += quantity
        item.save(update_fields=["quantity"])
    messages.success(request, "Оборудование добавлено в корзину.")
    return redirect("catalog:equipment_detail", pk=pk)


class CartListView(LoginRequiredMixin, ListView):
    model = CartItem
    template_name = "catalog/cart.html"

    def get_queryset(self):
        return (
            CartItem.objects.filter(user=self.request.user)
            .select_related("equipment", "equipment__site", "equipment__workshop")
            .order_by("-added_at")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        initial = {}
        if self.request.user.is_authenticated:
            initial = {
                "name": self.request.user.get_full_name() or self.request.user.username,
                "email": self.request.user.email,
            }
        context["checkout_form"] = CheckoutForm(initial=initial)
        return context


@login_required
def remove_from_cart(request: HttpRequest, pk: int) -> HttpResponse:
    item = get_object_or_404(CartItem, pk=pk, user=request.user)
    item.delete()
    messages.info(request, "Позиция удалена из корзины.")
    return redirect("catalog:cart")


@login_required
def checkout(request: HttpRequest) -> HttpResponse:
    items_qs = (
        CartItem.objects.filter(user=request.user)
        .select_related("equipment", "equipment__site", "equipment__workshop", "equipment__equipment_type")
        .order_by("-added_at")
    )
    if not items_qs.exists():
        messages.error(request, "Корзина пуста.")
        return redirect("catalog:cart")

    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            payload = []
            for item in items_qs:
                payload.append(
                    {
                        "equipment_id": item.equipment_id,
                        "equipment": str(item.equipment),
                        "type": str(item.equipment.equipment_type),
                        "site": str(item.equipment.site),
                        "workshop": str(item.equipment.workshop),
                        "quantity": item.quantity,
                    }
                )
            order = form.save(commit=False)
            order.user = request.user
            order.items = payload
            order.save()
            items_qs.delete()
            messages.success(request, "Заявка отправлена. Мы свяжемся с вами.")
            return redirect("catalog:equipment_list")
    else:
        initial = {
            "name": request.user.get_full_name() or request.user.username,
            "email": request.user.email,
        }
        form = CheckoutForm(initial=initial)

    return render(
        request,
        "catalog/checkout.html",
        {"checkout_form": form, "items": items_qs},
    )
