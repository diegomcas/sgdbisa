# Generated by Django 3.0.7 on 2020-07-03 18:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('documental', '0017_auto_20200703_1044'),
        ('calidad', '0005_auto_20200703_1031'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chequeo',
            name='documento',
            field=models.ForeignKey(default=0, help_text='Documento al que pertenece el check', on_delete=django.db.models.deletion.CASCADE, related_name='chequeo_documento', to='documental.Documento'),
        ),
        migrations.AlterField(
            model_name='chequeo',
            name='tipo_chequeo',
            field=models.ForeignKey(help_text='Verificación a realizar', on_delete=django.db.models.deletion.DO_NOTHING, related_name='chequeo_tipo_chequeo', to='calidad.TipoChequeo'),
        ),
        migrations.AlterField(
            model_name='listachequeo',
            name='tipos_chequeo',
            field=models.ManyToManyField(blank=True, help_text='Verificación a realizar', related_name='listachequeo_tipos_chequeo', to='calidad.TipoChequeo'),
        ),
    ]
