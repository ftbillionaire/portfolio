# Generated by Django 3.0.7 on 2020-07-31 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_auto_20200731_1634'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='createuser',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='createuser',
            name='last_name',
        ),
        migrations.AlterField(
            model_name='createuser',
            name='password',
            field=models.CharField(max_length=100),
        ),
    ]