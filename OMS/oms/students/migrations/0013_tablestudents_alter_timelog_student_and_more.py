# Generated by Django 4.2.14 on 2024-07-28 06:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('students', '0012_auto_20240629_2000'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tablestudents',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('StudentID', models.CharField(max_length=16, unique=True)),
                ('Firstname', models.CharField(max_length=100)),
                ('Middlename', models.CharField(blank=True, max_length=100, null=True)),
                ('Lastname', models.CharField(max_length=100)),
                ('Prefix', models.CharField(blank=True, max_length=100, null=True)),
                ('Email', models.EmailField(max_length=254, unique=True)),
                ('Address', models.CharField(max_length=250)),
                ('Number', models.CharField(max_length=11)),
                ('Course', models.CharField(max_length=100)),
                ('Year', models.CharField(max_length=50)),
                ('Image', models.ImageField(blank=True, null=True, upload_to='profileImage/')),
                ('Username', models.CharField(max_length=100, unique=True)),
                ('Password', models.CharField(max_length=100)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending', max_length=10)),
                ('archivedStudents', models.CharField(choices=[('notarchive', 'Notarchive'), ('archive', 'Archive'), ('unarchive', 'Unarchive')], default='notarchive', max_length=30)),
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
