# Generated by Django 2.2.4 on 2019-08-29 20:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('noticeapp', '0006_auto_20190830_0216'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notices',
            name='notice_file',
            field=models.FileField(blank=True, null=True, upload_to='Notices'),
        ),
    ]
