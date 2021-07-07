# Generated by Django 3.2.4 on 2021-06-29 01:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ccip', '0010_auto_20210628_2149'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='gender',
            field=models.CharField(blank=True, choices=[('Masculino', 'Masculino'), ('Feminino', 'Feminino'), ('Outro', 'Outro')], max_length=50),
        ),
        migrations.AlterField(
            model_name='surgery',
            name='pmu',
            field=models.CharField(choices=[('Protocolo', 'Protocolo'), ('Múltipla', 'Múltipla'), ('Unitária', 'Unitária')], default='Unitária', max_length=20),
        ),
    ]
