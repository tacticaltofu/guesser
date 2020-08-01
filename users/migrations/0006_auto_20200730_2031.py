# Generated by Django 2.2.14 on 2020-07-31 00:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20200730_2030'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='attempted',
            field=models.ManyToManyField(blank=True, null=True, related_name='attempted', to='punchline.Post'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='correct',
            field=models.ManyToManyField(blank=True, null=True, related_name='correct', to='punchline.Post'),
        ),
    ]
