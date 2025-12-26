from __future__ import annotations

from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, serializers, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import CartItem, Equipment, EquipmentType, Passport, Site, Workshop


class IsAdminOrSellerOwner(permissions.BasePermission):
    """
    SAFE methods: allow all.
    Write: admin/staff always; seller group allowed; delete/update only if owner.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        user = request.user
        if not user.is_authenticated:
            return False
        if user.is_staff or user.is_superuser:
            return True
        return user.groups.filter(name="seller").exists()

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        user = request.user
        if user.is_staff or user.is_superuser:
            return True
        owner = getattr(obj, "created_by", None)
        if owner and owner == user:
            return True
        return False


class EquipmentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipmentType
        fields = ["id", "name", "parent", "description", "default_attributes"]


class SiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Site
        fields = ["id", "name", "address"]


class WorkshopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workshop
        fields = ["id", "name", "description", "site"]


class PassportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Passport
        fields = ["id", "equipment", "description", "file", "uploaded_at"]
        read_only_fields = ["uploaded_at"]


class EquipmentSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField(read_only=True)
    equipment_type = EquipmentTypeSerializer(read_only=True)
    equipment_type_id = serializers.PrimaryKeyRelatedField(
        source="equipment_type",
        queryset=EquipmentType.objects.all(),
        write_only=True,
    )
    site = SiteSerializer(read_only=True)
    site_id = serializers.PrimaryKeyRelatedField(
        source="site",
        queryset=Site.objects.all(),
        write_only=True,
    )
    workshop = WorkshopSerializer(read_only=True)
    workshop_id = serializers.PrimaryKeyRelatedField(
        source="workshop",
        queryset=Workshop.objects.all(),
        write_only=True,
    )
    passports = PassportSerializer(many=True, read_only=True)

    class Meta:
        model = Equipment
        fields = [
            "id",
            "name",
            "inventory_number",
            "equipment_type",
            "equipment_type_id",
            "site",
            "site_id",
            "workshop",
            "workshop_id",
            "description",
            "attributes",
            "created_at",
            "updated_at",
            "created_by",
            "passports",
        ]
        read_only_fields = ["created_at", "updated_at", "passports", "created_by"]

    def validate(self, attrs):
        # Leverage model clean for cross-field validation
        instance = Equipment(**attrs)
        instance.clean()
        return attrs


class EquipmentTypeViewSet(viewsets.ModelViewSet):
    queryset = EquipmentType.objects.all()
    serializer_class = EquipmentTypeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "description"]
    ordering_fields = ["name"]


class SiteViewSet(viewsets.ModelViewSet):
    queryset = Site.objects.all()
    serializer_class = SiteSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "address"]
    ordering_fields = ["name"]


class WorkshopViewSet(viewsets.ModelViewSet):
    queryset = Workshop.objects.select_related("site")
    serializer_class = WorkshopSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "description", "site__name"]
    ordering_fields = ["name"]


class EquipmentViewSet(viewsets.ModelViewSet):
    queryset = (
        Equipment.objects.all()
        .select_related("equipment_type", "site", "workshop")
        .prefetch_related("passports")
    )
    serializer_class = EquipmentSerializer
    permission_classes = [IsAdminOrSellerOwner]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    search_fields = ["name", "description", "inventory_number", "equipment_type__name"]
    ordering_fields = ["name", "inventory_number", "updated_at"]
    filterset_fields = ["equipment_type", "site", "workshop"]

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        request = self.request
        eq_type = request.query_params.get("equipment_type")
        site = request.query_params.get("site")
        workshop = request.query_params.get("workshop")
        attr_key = request.query_params.get("attribute_key")
        attr_val = request.query_params.get("attribute_value")
        if eq_type:
            queryset = queryset.filter(equipment_type_id=eq_type)
        if site:
            queryset = queryset.filter(Q(site__id=site) | Q(site__name__icontains=site))
        if workshop:
            queryset = queryset.filter(
                Q(workshop__id=workshop) | Q(workshop__name__icontains=workshop)
            )
        if attr_key and attr_val:
            queryset = queryset.filter(attributes__contains={attr_key: attr_val})
        return queryset

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=["get"])
    def passports(self, request, pk=None):
        equipment = self.get_object()
        serializer = PassportSerializer(equipment.passports.all(), many=True)
        return Response(serializer.data)


class PassportViewSet(viewsets.ModelViewSet):
    queryset = Passport.objects.select_related("equipment")
    serializer_class = PassportSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["description", "equipment__name", "equipment__inventory_number"]
    ordering_fields = ["uploaded_at"]


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ["id", "user", "equipment", "quantity", "added_at"]
        read_only_fields = ["user", "added_at"]

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)


class CartItemViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user).select_related(
            "equipment", "equipment__site", "equipment__workshop"
        )

