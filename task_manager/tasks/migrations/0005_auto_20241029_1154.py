# Generated by Django 5.1.1 on 2024-10-29 11:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0004_alter_task_performer'),
    ]

    operations = [
        migrations.RenameField('Task', 'performer', 'executor'),
    ]
