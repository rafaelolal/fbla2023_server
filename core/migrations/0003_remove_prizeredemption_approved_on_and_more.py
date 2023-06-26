# Generated by Django 4.1.7 on 2023-06-25 23:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_rename_author_groupannouncement_created_by_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='prizeredemption',
            name='approved_on',
        ),
        migrations.AddField(
            model_name='prizeredemption',
            name='is_approved',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='parent',
            name='kids',
            field=models.ManyToManyField(related_name='parents', to='core.student'),
        ),
    ]
