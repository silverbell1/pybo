# Generated by Django 3.1.3 on 2024-04-16 02:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pybo', '0006_auto_20240320_1619'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='imgfile',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='question',
            name='imgfile',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]