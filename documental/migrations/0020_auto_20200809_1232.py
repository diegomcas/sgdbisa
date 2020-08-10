# Generated by Django 3.0.7 on 2020-08-09 15:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mensajes', '0004_auto_20200809_1232'),
        ('documental', '0019_auto_20200729_1539'),
    ]

    operations = [
        migrations.AddField(
            model_name='archivo',
            name='tique_revision',
            field=models.ForeignKey(blank=True, default=None, help_text='Tique que generó la revisión', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='archivo_tique_revisado', to='mensajes.Tique'),
        ),
        migrations.AddField(
            model_name='documento',
            name='tique_revision',
            field=models.ForeignKey(blank=True, default=None, help_text='Tique que generó la revisión', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='documento_tique_revisado', to='mensajes.Tique'),
        ),
        migrations.AlterField(
            model_name='archivo',
            name='tique',
            field=models.ManyToManyField(blank=True, help_text='Tiques del Archivo', related_name='tiquesarch', to='mensajes.Tique'),
        ),
    ]
