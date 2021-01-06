# Generated by Django 3.1.4 on 2021-01-06 16:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ppefrais', '0003_lignefraisforfait_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='lignefraisforfait',
            name='fiche',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.RESTRICT, to='ppefrais.fichefrais'),
        ),
        migrations.AddField(
            model_name='lignefraishorsforfait',
            name='fiche',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.RESTRICT, to='ppefrais.fichefrais'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='statut',
            field=models.CharField(choices=[('VST', 'Visiteur'), ('CPT', 'Comptable')], default='CPT', max_length=3),
        ),
    ]
