# Generated by Django 3.2.7 on 2021-09-24 23:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('codes', '0011_answer_question_quiz_result'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sub_name', models.CharField(max_length=30)),
                ('sub_img', models.ImageField(blank=True, null=True, upload_to='')),
                ('sub_desp', models.CharField(max_length=300)),
            ],
        ),
    ]
