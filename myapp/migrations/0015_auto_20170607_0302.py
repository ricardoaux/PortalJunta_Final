# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-07 03:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0014_auto_20170603_2036'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requerimento',
            name='estado',
            field=models.CharField(choices=[('ANALISE', 'Em Análise'), ('PAGAMENTO', 'Aguarda Pagamento'), ('PAGO', 'Pagamento Efetuado'), ('DIFERIDO', 'Diferido'), ('RECUSADO', 'Recusado')], max_length=20),
        ),
    ]
