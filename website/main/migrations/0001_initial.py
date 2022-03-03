# Generated by Django 4.0.2 on 2022-03-03 00:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='ServiceProvider',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('provider_name', models.CharField(max_length=30)),
                ('website', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='thirdParty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('third_party_name', models.CharField(max_length=30)),
                ('website', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=30)),
                ('password', models.CharField(max_length=30)),
                ('address', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=9)),
                ('client_permissions', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='main.client')),
                ('provider_permissions', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='main.serviceprovider')),
                ('thirdParty_permissions', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='main.thirdparty')),
            ],
        ),
    ]
