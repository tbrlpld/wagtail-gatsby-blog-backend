# Generated by Django 2.2.13 on 2020-06-24 04:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0012_blogcategoryindexpage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogcategoryindexpage',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='blog.BlogCategory'),
        ),
    ]
