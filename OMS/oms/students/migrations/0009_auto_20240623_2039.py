# Generated by Django 3.2.25 on 2024-06-23 12:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('students', '0008_auto_20240620_2159'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tablestudents',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('StudentID', models.CharField(max_length=10, unique=True)),
                ('Firstname', models.CharField(max_length=100)),
                ('Middlename', models.CharField(max_length=100)),
                ('Lastname', models.CharField(max_length=100)),
                ('Prefix', models.CharField(blank=True, max_length=100, null=True)),
                ('Email', models.EmailField(max_length=254, unique=True)),
                ('Course', models.CharField(max_length=100)),
                ('Year', models.CharField(max_length=50)),
                ('Username', models.CharField(max_length=100, unique=True)),
                ('Password', models.CharField(max_length=100)),
                ('is_approved', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='timelog',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='students.tablestudents'),
        ),
        migrations.DeleteModel(
            name='Tablestudent',
        ),
    ]
