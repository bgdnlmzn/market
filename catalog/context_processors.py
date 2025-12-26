from __future__ import annotations

from django.contrib.auth.models import AnonymousUser
from django.http import HttpRequest

from .models import CartItem


def catalog_context(request: HttpRequest) -> dict[str, int]:
    """Add reusable catalog context (e.g., cart counter) to templates."""
    user = request.user
    if isinstance(user, AnonymousUser) or not user.is_authenticated:
        return {"cart_count": 0, "can_add_equipment": False}
    cart_count = (
        CartItem.objects.filter(user=user)
        .only("id")  # lightweight query
        .count()
    )
    can_add = (
        user.is_superuser
        or user.is_staff
        or user.groups.filter(name="seller").exists()
    )
    return {"cart_count": cart_count, "can_add_equipment": can_add}

