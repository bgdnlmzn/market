from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("catalog", "0003_create_seller_group"),
    ]

    operations = [
        migrations.AddField(
            model_name="equipment",
            name="created_by",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=models.SET_NULL,
                related_name="created_equipment",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]

