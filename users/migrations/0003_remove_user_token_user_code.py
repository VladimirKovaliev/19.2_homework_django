# Generated by Django 4.2.7 on 2023-12-28 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_user_email_verify_user_token'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='token',
        ),
        migrations.AddField(
            model_name='user',
            name='code',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='код'),
        ),
    ]
