# Generated by Django 5.1.4 on 2025-01-17 23:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campaigns', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='campaign',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='campaign',
            name='updated_at',
        ),
        migrations.AddField(
            model_name='campaign',
            name='campaign_url',
            field=models.URLField(blank=True, null=True, verbose_name='Campaign URL'),
        ),
        migrations.AlterField(
            model_name='campaign',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='campaign',
            name='platform',
            field=models.CharField(choices=[('Facebook', 'Facebook'), ('Google', 'Google Ads'), ('TikTok', 'TikTok Ads'), ('Instagram', 'Instagram'), ('LinkedIn', 'LinkedIn')], max_length=50, verbose_name='Advertising Platform'),
        ),
        migrations.AlterField(
            model_name='campaign',
            name='status',
            field=models.CharField(choices=[('Active', 'Active'), ('Paused', 'Paused'), ('Completed', 'Completed')], max_length=20, verbose_name='Status'),
        ),
    ]
