# Generated by Django 3.1.3 on 2020-11-18 14:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ppefrais', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fichefrais',
            name='id_etat',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='ppefrais.etat'),
        ),
    ]
