# Generated by Django 4.1.5 on 2023-02-04 07:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=255)),
                ('slug', models.SlugField(max_length=250, unique=True)),
            ],
            options={
                'verbose_name_plural': 'categories',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('brand', models.CharField(max_length=250)),
                ('description', models.TextField(max_length=400)),
                ('slug', models.SlugField(max_length=255)),
                ('price', models.DecimalField(decimal_places=3, max_digits=6)),
                ('image', models.ImageField(upload_to='product-images/')),
                ('category', models.ManyToManyField(related_name='category', to='store.category')),
            ],
        ),
    ]
