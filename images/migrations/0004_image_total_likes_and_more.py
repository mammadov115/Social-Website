# Generated by Django 4.2.2 on 2023-07-13 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0003_alter_image_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='total_likes',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddIndex(
            model_name='image',
            index=models.Index(fields=['-total_likes'], name='images_imag_total_l_0bcd7e_idx'),
        ),
    ]
