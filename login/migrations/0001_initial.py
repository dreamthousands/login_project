# Generated by Django 2.2 on 2019-05-20 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100, unique=True)),
                ('password', models.CharField(max_length=20)),
                ('sex', models.CharField(choices=[('male', '男'), ('female', '女')], default='男', max_length=10)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('reg_time', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'user_info',
                'ordering': ['reg_time'],
            },
        ),
    ]
