# Generated by Django 4.2.11 on 2025-03-28 11:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ShibeApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='debtor',
            options={'ordering': ('-date_created',)},
        ),
        migrations.RemoveField(
            model_name='debtor',
            name='date_updated',
        ),
        migrations.RemoveField(
            model_name='debtor',
            name='total_debt',
        ),
        migrations.RemoveField(
            model_name='debtor',
            name='total_paid',
        ),
        migrations.AlterField(
            model_name='debtor',
            name='balance',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='debtor',
            name='debtor_name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='product',
            name='title',
            field=models.CharField(choices=[('lishe 3kg', 'Lishe 3kg'), ('lishe dozen', 'Lishe dozen'), ('Unga 25kg', 'Unga 25kg'), ('Unga 10kg', 'Unga 10kg'), ('Unga 5kg', 'Unga 5kg'), ('kande 25kg', 'Kande 25kg')], max_length=255),
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
                ('debitor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ShibeApp.debtor')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ShibeApp.product')),
            ],
        ),
    ]
