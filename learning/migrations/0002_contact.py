# Generated by Django 3.1.2 on 2023-07-16 20:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learning', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=20, null=True)),
                ('message', models.TextField(null=True)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
    ]
