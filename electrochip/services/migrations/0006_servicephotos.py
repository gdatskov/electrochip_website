# Generated by Django 4.2.4 on 2023-08-16 20:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0005_serviceadditionaldescription'),
    ]

    operations = [
        migrations.CreateModel(
            name='ServicePhotos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.URLField()),
                ('description', models.TextField(blank=True, max_length=100, null=True)),
            ],
        ),
    ]
