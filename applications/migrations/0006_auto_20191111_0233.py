# Generated by Django 2.2.4 on 2019-11-11 02:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0005_auto_20191111_0048'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fbapplication',
            name='status',
            field=models.CharField(blank=True, choices=[('not submitted', 'Not Submitted')], default='not submitted', max_length=255, null=True),
        ),
    ]
