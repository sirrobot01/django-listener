# Generated by Django 4.2.6 on 2023-11-02 10:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Source',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('url', models.URLField(max_length=1000)),
                ('is_active', models.BooleanField(default=True)),
                ('unique_id_field', models.CharField(default='id', max_length=255)),
                ('username', models.CharField(blank=True, max_length=255, null=True)),
                ('password', models.CharField(blank=True, max_length=255, null=True)),
                ('token', models.TextField(blank=True, null=True)),
                ('token_header', models.CharField(default='HTTP_AUTHORIZATION', max_length=255)),
                ('http_method', models.CharField(default='POST', max_length=255)),
                ('last_checked', models.DateTimeField(blank=True, null=True)),
                ('content_type', models.CharField(default='application/json', max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('body', models.TextField(blank=True, null=True)),
                ('headers', models.TextField(blank=True, null=True)),
                ('query_params', models.TextField(blank=True, null=True)),
                ('unique_id', models.CharField(blank=True, db_index=True, max_length=255, null=True)),
                ('processed', models.BooleanField(default=False)),
                ('processed_at', models.DateTimeField(blank=True, null=True)),
                ('source', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events',
                                             to='listener.source')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
