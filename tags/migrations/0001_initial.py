# Generated by Django 2.2.1 on 2019-05-13 06:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('unique_name', models.SlugField(max_length=200, unique=True)),
                ('type', models.IntegerField(choices=[(0, '其他'), (1, '数据结构'), (2, '公司'), (3, '算法'), (4, '面试'), (5, '导航'), (6, '课程')], default=0)),
                ('order', models.IntegerField(default=0)),
            ],
        ),
    ]
