# Generated by Django 2.2.4 on 2019-09-03 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_reg_students'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reg_students',
            name='regno',
            field=models.PositiveIntegerField(),
        ),
    ]
