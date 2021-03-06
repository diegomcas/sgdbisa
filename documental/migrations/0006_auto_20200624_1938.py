# Generated by Django 3.0.7 on 2020-06-24 22:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('documental', '0005_auto_20200624_1902'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='documento',
            options={'ordering': ['numero', 'revision'], 'permissions': (('revision_documento', 'Add revision to Document'),)},
        ),
        migrations.AlterField(
            model_name='documento',
            name='proyecto',
            field=models.ForeignKey(blank=True, help_text='Proyecto al que pertenece el Documento', null=True, on_delete=django.db.models.deletion.SET_NULL, to='documental.Proyecto'),
        ),
    ]
