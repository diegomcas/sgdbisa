# Generated by Django 3.0.7 on 2020-06-19 19:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('documental', '0003_auto_20200619_1623'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='proyecto',
            options={'ordering': ['fecha', 'orden_trabajo'], 'permissions': (('list_proyectos', 'Can list proyectos'), ('finalize_proyecto', 'Can finalize proyecto'))},
        ),
    ]
