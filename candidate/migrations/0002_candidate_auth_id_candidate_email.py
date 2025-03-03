# Generated by Django 5.1.6 on 2025-02-28 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('candidate', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidate',
            name='auth_id',
            field=models.UUIDField(default=None, editable=False, null=True),
        ),
        migrations.AddField(
            model_name='candidate',
            name='email',
            field=models.EmailField(default=None, max_length=254, null=True, unique=True),
        ),
    ]
