# Generated by Django 2.2.4 on 2019-11-03 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fund', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='fbfunding',
            name='document_id',
            field=models.CharField(default='kfldsfks', max_length=255),
            preserve_default=False,
        ),
    ]
