# Generated by Django 3.0.8 on 2020-07-20 20:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20200720_2316'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image_url',
            field=models.CharField(default='https://upload.wikimedia.org/wikipedia/commons/8/89/Portrait_Placeholder.png', max_length=200, null=True),
        ),
    ]
