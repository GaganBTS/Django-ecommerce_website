# Generated by Django 4.1.5 on 2023-03-11 11:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0002_order_orderitem'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='email',
        ),
    ]
