# Generated by Django 5.2 on 2025-05-11 17:43

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0006_alter_word_word_alter_word_unique_together'),
    ]

    operations = [
        migrations.AddField(
            model_name='tabooset',
            name='session_key',
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
        migrations.AlterField(
            model_name='tabooset',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='taboo_sets', to=settings.AUTH_USER_MODEL),
        ),
    ]
