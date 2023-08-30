# Generated by Django 3.1.2 on 2022-12-22 21:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0006_auto_20220723_1406'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='replies',
        ),
        migrations.AddField(
            model_name='comment',
            name='status',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='comment',
            name='that_comment_id',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='article',
            name='photo',
            field=models.ImageField(default='images/default_img/carrefour.jpg', null=True, upload_to='images'),
        ),
        migrations.AlterField(
            model_name='article',
            name='pub_date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.DeleteModel(
            name='Reponse',
        ),
    ]
