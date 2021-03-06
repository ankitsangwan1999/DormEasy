# Generated by Django 2.2.3 on 2019-09-12 11:13

import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Complaint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=60)),
                ('complaint', ckeditor.fields.RichTextField(max_length=500)),
                ('status', models.CharField(choices=[(0, 'Pending'), (1, 'Acknowledged'), (2, 'Resolved')], max_length=1)),
                ('concerned_authority', models.CharField(max_length=60)),
                ('number', models.PositiveIntegerField(default=1)),
                ('first_complainer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Complainers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('complaint_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='complain.Complaint')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
