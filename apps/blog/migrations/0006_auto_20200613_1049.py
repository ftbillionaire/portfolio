# Generated by Django 3.0.7 on 2020-06-13 07:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20200613_1041'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='date_pub',
            field=models.DateField(auto_now_add=True),
        ),
    ]