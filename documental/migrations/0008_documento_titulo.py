# Generated by Django 3.0.7 on 2020-06-25 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documental', '0007_auto_20200624_2054'),
    ]

    operations = [
        migrations.AddField(
            model_name='documento',
            name='titulo',
            field=models.CharField(help_text='Título del documento', max_length=255, null=True, verbose_name='Título'),
        ),
    ]
