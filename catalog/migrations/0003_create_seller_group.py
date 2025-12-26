from django.db import migrations


def create_seller_group(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    Permission = apps.get_model("auth", "Permission")
    ContentType = apps.get_model("contenttypes", "ContentType")

    equipment_ct = ContentType.objects.get(app_label="catalog", model="equipment")
    passport_ct = ContentType.objects.get(app_label="catalog", model="passport")

    seller_group, _ = Group.objects.get_or_create(name="seller")

    equipment_perms = ["add_equipment", "change_equipment", "delete_equipment"]
    passport_perms = ["add_passport", "change_passport", "delete_passport"]

    for code in equipment_perms:
        perm = Permission.objects.get(content_type=equipment_ct, codename=code)
        seller_group.permissions.add(perm)
    for code in passport_perms:
        perm = Permission.objects.get(content_type=passport_ct, codename=code)
        seller_group.permissions.add(perm)


def remove_seller_group(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    Group.objects.filter(name="seller").delete()


class Migration(migrations.Migration):
    dependencies = [
        ("catalog", "0002_equipment_image"),
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.RunPython(create_seller_group, remove_seller_group),
    ]

