# Generated by Django 3.0.6 on 2020-05-19 19:04

from django.db import migrations, models
import facerecognition.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Config',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attendance_frame_threshold', models.IntegerField(default=5)),
                ('detection_sensitivity', models.DecimalField(decimal_places=2, default=0.45, max_digits=4)),
                ('stayback_frame_theshold', models.IntegerField(default=2)),
                ('no_teacher_frame_threshold', models.IntegerField(default=2)),
                ('frame_rate', models.IntegerField(default=1)),
                ('ai_model', models.CharField(default='mtcnn', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('identification', models.CharField(max_length=200, primary_key=True, serialize=False, unique=True)),
                ('Front_Face', models.ImageField(upload_to=facerecognition.models.get_person_folder)),
                ('Top_Face', models.ImageField(upload_to=facerecognition.models.get_person_folder)),
                ('Right_Face', models.ImageField(upload_to=facerecognition.models.get_person_folder)),
                ('Left_Face', models.ImageField(upload_to=facerecognition.models.get_person_folder)),
                ('Bottom_Face', models.ImageField(upload_to=facerecognition.models.get_person_folder)),
                ('Front_Face_masked', models.ImageField(blank=True, upload_to=facerecognition.models.get_person_folder)),
                ('Top_Face_masked', models.ImageField(blank=True, upload_to=facerecognition.models.get_person_folder)),
                ('Right_Face_masked', models.ImageField(blank=True, upload_to=facerecognition.models.get_person_folder)),
                ('Left_Face_masked', models.ImageField(blank=True, upload_to=facerecognition.models.get_person_folder)),
                ('Bottom_Face_masked', models.ImageField(blank=True, upload_to=facerecognition.models.get_person_folder)),
                ('time_reg', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]