# Generated by Django 2.2.4 on 2019-09-03 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20190903_1704'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reg_students',
            name='Fullname',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='reg_students',
            name='Gender',
            field=models.CharField(max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='reg_students',
            name='Regno',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='reg_students',
            name='Sem',
            field=models.CharField(max_length=1, null=True),
        ),
    ]
