# Generated by Django 4.2.14 on 2024-08-06 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_announcement_delete_announcementtable'),
    ]

    operations = [
        migrations.CreateModel(
            name='RenderingHoursTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course', models.CharField(choices=[('BS Information Technology', 'BS Information Technology'), ('BS Computer Science', 'BS Computer Science')], max_length=100, unique=True)),
                ('required_hours', models.PositiveIntegerField()),
            ],
        ),
    ]