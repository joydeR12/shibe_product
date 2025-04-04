# Generated by Django 4.2.11 on 2025-03-30 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ShibeApp', '0004_alter_debtor_debtor_name_alter_debtor_debtor_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='debitororder',
            name='debt_paid',
            field=models.DecimalField(decimal_places=2, default='0.00', max_digits=10),
        ),
        migrations.AlterField(
            model_name='debitororder',
            name='debt_pending',
            field=models.DecimalField(decimal_places=2, default='0.00', max_digits=10),
        ),
        migrations.AlterField(
            model_name='debitororder',
            name='total_price',
            field=models.DecimalField(decimal_places=2, default='0.00', max_digits=10),
        ),
        migrations.AlterField(
            model_name='product',
            name='old_price',
            field=models.DecimalField(decimal_places=2, default='0.00', max_digits=10),
        ),
    ]
