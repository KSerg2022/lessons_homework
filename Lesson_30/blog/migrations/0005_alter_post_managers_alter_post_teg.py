# Generated by Django 4.1.4 on 2022-12-26 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_alter_teg_options_alter_teg_teg_name'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='post',
            managers=[
            ],
        ),
        migrations.AlterField(
            model_name='post',
            name='teg',
            field=models.ManyToManyField(blank=True, help_text='Выберите тег', null=True, to='blog.teg', verbose_name='Теги'),
        ),
    ]
