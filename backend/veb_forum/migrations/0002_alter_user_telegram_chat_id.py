# Generated by Django 4.2 on 2023-09-18 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('veb_forum', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='telegram_chat_id',
            field=models.CharField(max_length=10),
        ),
    ]
