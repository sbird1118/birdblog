# Generated by Django 4.1.3 on 2022-11-20 06:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_alter_article_user'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='article',
            options={'ordering': ['-create_time'], 'verbose_name': '文章', 'verbose_name_plural': '文章'},
        ),
        migrations.AlterField(
            model_name='article',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='articles', to='blog.category', verbose_name='分类'),
        ),
    ]
