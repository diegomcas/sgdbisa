# Generated by Django 3.0.7 on 2020-06-26 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documental', '0010_auto_20200626_1129'),
    ]

    operations = [
        migrations.AlterField(
            model_name='archivo',
            name='directorio',
            field=models.CharField(help_text='Directorio de almacenamiento del archivo', max_length=1000),
        ),
    ]
