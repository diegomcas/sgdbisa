# Generated by Django 3.0.7 on 2020-06-30 12:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('calidad', '0003_auto_20200629_2016'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tipochequeo',
            options={'ordering': ['nombre'], 'permissions': (('list_tiposchequeo', 'Can list tipos chequeo'),)},
        ),
    ]