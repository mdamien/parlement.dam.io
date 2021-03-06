# Generated by Django 3.2 on 2020-12-08 09:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='follow',
            name='parlementaire_slug',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='follow',
            unique_together={('parlementaire_slug', 'email')},
        ),
        migrations.RemoveField(
            model_name='follow',
            name='parlementaire',
        ),
    ]
