from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="EquipmentType",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=255)),
                ("description", models.TextField(blank=True)),
                ("default_attributes", models.JSONField(blank=True, default=list, help_text="Список рекомендуемых характеристик для этого типа")),
                ("parent", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="children", to="catalog.equipmenttype")),
            ],
            options={
                "ordering": ["name"],
                "verbose_name": "Тип оборудования",
                "verbose_name_plural": "Типы оборудования",
            },
        ),
        migrations.CreateModel(
            name="Site",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=255, unique=True)),
                ("address", models.CharField(blank=True, max_length=255)),
            ],
            options={
                "ordering": ["name"],
                "verbose_name": "Площадка",
                "verbose_name_plural": "Площадки",
            },
        ),
        migrations.CreateModel(
            name="Workshop",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=255)),
                ("description", models.TextField(blank=True)),
                ("site", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="workshops", to="catalog.site")),
            ],
            options={
                "ordering": ["name"],
                "verbose_name": "Цех",
                "verbose_name_plural": "Цеха",
                "unique_together": {("site", "name")},
            },
        ),
        migrations.CreateModel(
            name="Equipment",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=255)),
                ("inventory_number", models.CharField(max_length=100, unique=True)),
                ("description", models.TextField(blank=True)),
                ("image", models.ImageField(blank=True, null=True, upload_to="equipment/")),
                ("attributes", models.JSONField(blank=True, default=dict)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("equipment_type", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="equipment", to="catalog.equipmenttype")),
                ("site", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="equipment", to="catalog.site")),
                ("workshop", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="equipment", to="catalog.workshop")),
            ],
            options={
                "ordering": ["name"],
                "verbose_name": "Оборудование",
                "verbose_name_plural": "Оборудование",
            },
        ),
        migrations.CreateModel(
            name="Passport",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("description", models.CharField(blank=True, max_length=255)),
                ("file", models.FileField(upload_to="passports/")),
                ("uploaded_at", models.DateTimeField(auto_now_add=True)),
                ("equipment", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="passports", to="catalog.equipment")),
            ],
            options={
                "ordering": ["-uploaded_at"],
                "verbose_name": "Паспорт",
                "verbose_name_plural": "Паспорта",
            },
        ),
        migrations.CreateModel(
            name="CartItem",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("quantity", models.PositiveIntegerField(default=1)),
                ("added_at", models.DateTimeField(auto_now_add=True)),
                ("equipment", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="cart_items", to="catalog.equipment")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="cart_items", to=settings.AUTH_USER_MODEL)),
            ],
            options={
                "ordering": ["-added_at"],
                "unique_together": {("user", "equipment")},
                "verbose_name": "Запись корзины",
                "verbose_name_plural": "Корзина",
            },
        ),
    ]
# Generated by Django 5.0.6 on 2025-12-26 11:56

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Site',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('address', models.CharField(blank=True, max_length=255)),
            ],
            options={
                'verbose_name': 'Площадка',
                'verbose_name_plural': 'Площадки',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='EquipmentType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('default_attributes', models.JSONField(blank=True, default=list, help_text='Список рекомендуемых характеристик для этого типа')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='children', to='catalog.equipmenttype')),
            ],
            options={
                'verbose_name': 'Тип оборудования',
                'verbose_name_plural': 'Типы оборудования',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Equipment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('inventory_number', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField(blank=True)),
                ('attributes', models.JSONField(blank=True, default=dict)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('equipment_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='equipment', to='catalog.equipmenttype')),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='equipment', to='catalog.site')),
            ],
            options={
                'verbose_name': 'Оборудование',
                'verbose_name_plural': 'Оборудование',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Passport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(blank=True, max_length=255)),
                ('file', models.FileField(upload_to='passports/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('equipment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='passports', to='catalog.equipment')),
            ],
            options={
                'verbose_name': 'Паспорт',
                'verbose_name_plural': 'Паспорта',
                'ordering': ['-uploaded_at'],
            },
        ),
        migrations.CreateModel(
            name='Workshop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='workshops', to='catalog.site')),
            ],
            options={
                'verbose_name': 'Цех',
                'verbose_name_plural': 'Цеха',
                'ordering': ['name'],
                'unique_together': {('site', 'name')},
            },
        ),
        migrations.AddField(
            model_name='equipment',
            name='workshop',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='equipment', to='catalog.workshop'),
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('added_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart_items', to=settings.AUTH_USER_MODEL)),
                ('equipment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart_items', to='catalog.equipment')),
            ],
            options={
                'verbose_name': 'Запись корзины',
                'verbose_name_plural': 'Корзина',
                'ordering': ['-added_at'],
                'unique_together': {('user', 'equipment')},
            },
        ),
    ]
