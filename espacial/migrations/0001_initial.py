# Generated by Django 3.0.7 on 2020-07-03 19:05

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ElementoEspacial',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_elemento', models.CharField(choices=[('PT', 'Puntos'), ('PL', 'Poligono')], default='PL', max_length=2)),
                ('puntos', django.contrib.gis.db.models.fields.MultiPointField(srid=4326)),
                ('poligono', django.contrib.gis.db.models.fields.PolygonField(srid=4326)),
            ],
        ),
    ]