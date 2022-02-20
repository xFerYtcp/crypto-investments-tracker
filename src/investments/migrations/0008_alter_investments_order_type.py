# Generated by Django 4.0.2 on 2022-02-13 23:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('investments', '0007_ordertype_alter_investments_order_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='investments',
            name='order_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='investments.ordertype', verbose_name='Order type'),
        ),
    ]
