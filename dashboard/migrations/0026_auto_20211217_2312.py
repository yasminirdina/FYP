# Generated by Django 3.2.2 on 2021-12-17 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0025_auto_20211217_1120'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parent',
            name='name',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='homeroomClass',
            field=models.CharField(choices=[('1 ARIF', '1 ARIF'), ('1 BESTARI', '1 BESTARI'), ('1 CENDEKIA', '1 CENDEKIA'), ('1 DINAMIK', '1 DINAMIK'), ('1 EFEKTIF', '1 EFEKTIF'), ('1 FIKRAH', '1 FIKRAH'), ('1 GEMILANG', '1 GEMILANG'), ('1 HIKMAH', '1 HIKMAH'), ('1 ILHAM', '1 ILHAM'), ('1 JAKSA', '1 JAKSA'), ('2 ARIF', '2 ARIF'), ('2 BESTARI', '2 BESTARI'), ('2 CENDEKIA', '2 CENDEKIA'), ('2 DINAMIK', '2 DINAMIK'), ('2 EFEKTIF', '2 EFEKTIF'), ('2 FIKRAH', '2 FIKRAH'), ('2 GEMILANG', '2 GEMILANG'), ('2 HIKMAH', '2 HIKMAH'), ('2 ILHAM', '2 ILHAM'), ('2 JAKSA', '2 JAKSA'), ('2 KALIBER', '2 KALIBER'), ('3 ARIF', '3 ARIF'), ('3 BESTARI', '3 BESTARI'), ('3 CENDEKIA', '3 CENDEKIA'), ('3 DINAMIK', '3 DINAMIK'), ('3 EFEKTIF', '3 EFEKTIF'), ('3 FIKRAH', '3 FIKRAH'), ('3 GEMILANG', '3 GEMILANG'), ('3 HIKMAH', '3 HIKMAH'), ('3 ILHAM', '3 ILHAM'), ('3 JAKSA', '3 JAKSA'), ('4 ARIF', '4 ARIF'), ('4 BESTARI', '4 BESTARI'), ('4 CENDEKIA', '4 CENDEKIA'), ('4 DINAMIK', '4 DINAMIK'), ('4 EFEKTIF', '4 EFEKTIF'), ('4 FIKRAH', '4 FIKRAH'), ('4 GEMILANG', '4 GEMILANG'), ('4 HIKMAH', '4 HIKMAH'), ('4 ILHAM', '4 ILHAM'), ('4 JAKSA', '4 JAKSA'), ('5 ARIF', '5 ARIF'), ('5 BESTARI', '5 BESTARI'), ('5 CENDEKIA', '5 CENDEKIA'), ('5 DINAMIK', '5 DINAMIK'), ('5 EFEKTIF', '5 EFEKTIF'), ('5 FIKRAH', '5 FIKRAH'), ('5 GEMILANG', '5 GEMILANG'), ('5 HIKMAH', '5 HIKMAH'), ('5 ILHAM', '5 ILHAM'), ('5 JAKSA', '5 JAKSA'), ('NA', 'NA')], default='NA', max_length=25),
        ),
    ]
