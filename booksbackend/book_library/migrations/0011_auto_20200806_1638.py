# Generated by Django 3.0.8 on 2020-08-06 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book_library', '0010_auto_20200806_1637'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='title',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterUniqueTogether(
            name='book',
            unique_together=set(),
        ),
    ]
