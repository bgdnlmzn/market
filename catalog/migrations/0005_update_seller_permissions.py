from django.db import migrations


def update_seller_permissions(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    Permission = apps.get_model("auth", "Permission")
    ContentType = apps.get_model("contenttypes", "ContentType")

    seller_group, _ = Group.objects.get_or_create(name="seller")

    content_types = {
        "equipment": ("catalog", "equipment"),
        "passport": ("catalog", "passport"),
        "site": ("catalog", "site"),
        "workshop": ("catalog", "workshop"),
        "equipmenttype": ("catalog", "equipmenttype"),
    }

    perms_to_add = []
    for model_key, (app_label, model) in content_types.items():
        ct = ContentType.objects.get(app_label=app_label, model=model)
        for codename in ("add", "change", "delete"):
            perms_to_add.append(Permission.objects.get(content_type=ct, codename=f"{codename}_{model}"))

    for perm in perms_to_add:
        seller_group.permissions.add(perm)


def noop(apps, schema_editor):
    # Don't remove permissions on reverse to avoid data loss
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("catalog", "0004_equipment_created_by"),
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.RunPython(update_seller_permissions, noop),
    ]

