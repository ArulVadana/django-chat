# Generated by Django 4.1.1 on 2022-12-07 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0005_videocallmembers'),
    ]

    operations = [
        migrations.AddField(
            model_name='videocallmembers',
            name='uid',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='videocallmembers',
            name='name',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
