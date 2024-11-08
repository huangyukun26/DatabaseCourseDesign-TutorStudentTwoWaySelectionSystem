# Generated by Django 4.2.16 on 2024-11-07 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mentor_student', '0004_rename_sid_card_number_applicant_id_card_number'),
    ]

    operations = [
        migrations.RenameField(
            model_name='applicant',
            old_name='id_card_number',
            new_name='Sid_card_number',
        ),
        migrations.AddField(
            model_name='applicant',
            name='first_subject_id',
            field=models.IntegerField(blank=True, null=True, verbose_name='一级科目报考志愿ID'),
        ),
        migrations.AddField(
            model_name='applicant',
            name='second_subject_id',
            field=models.IntegerField(blank=True, null=True, verbose_name='二级科目报考志愿ID'),
        ),
    ]