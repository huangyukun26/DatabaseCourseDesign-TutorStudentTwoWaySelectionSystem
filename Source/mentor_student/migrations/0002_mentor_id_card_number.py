# Generated by Django 4.2.16 on 2024-11-07 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mentor_student', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='mentor',
            name='id_card_number',
            field=models.CharField(default=0, max_length=20, unique=True, verbose_name='导师身份证号'),
            preserve_default=False,
        ),
    ]