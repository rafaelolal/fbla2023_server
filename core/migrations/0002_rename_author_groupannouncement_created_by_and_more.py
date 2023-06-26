# Generated by Django 4.1.7 on 2023-06-25 04:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='groupannouncement',
            old_name='author',
            new_name='created_by',
        ),
        migrations.RemoveField(
            model_name='prize',
            name='student',
        ),
        migrations.RemoveField(
            model_name='student',
            name='leaderboard_points',
        ),
        migrations.AddField(
            model_name='groupmember',
            name='member',
            field=models.ForeignKey(default='d', on_delete=django.db.models.deletion.CASCADE, related_name='groups', to='core.student'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='prize',
            name='cost',
            field=models.PositiveSmallIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='prize',
            name='name',
            field=models.CharField(default='default name', max_length=256),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='adminannouncement',
            name='content',
            field=models.TextField(max_length=1024),
        ),
        migrations.AlterField(
            model_name='prizeredemption',
            name='prize',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='redemptions', to='core.prize'),
        ),
        migrations.AlterField(
            model_name='prizeredemption',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='redemptions', to='core.student'),
        ),
        migrations.CreateModel(
            name='GroupEvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='group_events', to='core.student')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='group_participants', to='core.event')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events', to='core.group')),
            ],
        ),
    ]