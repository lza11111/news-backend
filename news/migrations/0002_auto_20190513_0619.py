# Generated by Django 2.2.1 on 2019-05-13 06:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tags', '0001_initial'),
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, max_length=255, unique=True)),
                ('cover_image', models.URLField(blank=True, max_length=255, null=True)),
                ('content', models.TextField(blank=True, null=True)),
                ('tags', models.ManyToManyField(blank=True, to='tags.Tag')),
            ],
        ),
        migrations.DeleteModel(
            name='Article',
        ),
    ]
