# Generated by Django 3.0.2 on 2020-02-12 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0003_auto_20200212_1846'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='slug',
            field=models.SlugField(editable=False, unique=True),
        ),
    ]