# Generated by Django 5.1.1 on 2024-10-16 19:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='name',
            field=models.CharField(default='', max_length=100, unique=True, verbose_name='name'),
        ),
    ]
