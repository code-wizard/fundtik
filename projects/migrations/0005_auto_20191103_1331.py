# Generated by Django 2.2.4 on 2019-11-03 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0004_auto_20191103_1258'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fbmilestones',
            name='description',
            field=models.TextField(),
        ),
    ]
