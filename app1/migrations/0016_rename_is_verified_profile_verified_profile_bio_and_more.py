# Generated by Django 4.1.7 on 2023-11-03 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0015_address_mobile_alter_cartorder_product_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='is_verified',
            new_name='verified',
        ),
        migrations.AddField(
            model_name='profile',
            name='bio',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='full_name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='image',
            field=models.ImageField(blank=True, default='category.jpg', null=True, upload_to='image'),
        ),
        migrations.AddField(
            model_name='profile',
            name='phone',
            field=models.CharField(default='123', max_length=200),
        ),
    ]
