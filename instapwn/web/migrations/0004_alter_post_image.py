# Generated by Django 4.1 on 2022-08-26 07:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0003_post_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(null=True, upload_to='images/'),
        ),
    ]
