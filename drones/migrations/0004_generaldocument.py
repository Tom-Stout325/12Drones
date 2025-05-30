# Generated by Django 4.2.20 on 2025-04-13 03:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drones', '0003_sopdocument_standardoperatingprocedure_slug_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='GeneralDocument',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('category', models.CharField(choices=[('Insurance', 'Insurance'), ('Event', 'Event Instructions'), ('Compliance', 'Compliance'), ('Legal', 'Legal'), ('Other', 'Other')], max_length=50)),
                ('description', models.TextField(blank=True)),
                ('file', models.FileField(upload_to='general_documents/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
