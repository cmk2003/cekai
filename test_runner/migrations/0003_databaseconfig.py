# Generated by Django 2.2.3 on 2024-05-20 07:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('test_runner', '0002_debugtalk'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataBaseConfig',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('name', models.CharField(max_length=100, verbose_name='数据库名称')),
                ('type', models.IntegerField(choices=[(1, 'pa'), (2, 'mysql')], verbose_name='数据库类型')),
                ('server', models.CharField(max_length=100, verbose_name='数据库地址')),
                ('account', models.CharField(max_length=50, verbose_name='数据库账号')),
                ('password', models.CharField(max_length=100, verbose_name='数据库密码')),
                ('desc', models.TextField(verbose_name='描述')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='test_runner.Project')),
            ],
            options={
                'verbose_name': '数据库配置表',
                'verbose_name_plural': '数据库配置表',
                'db_table': 'database',
            },
        ),
    ]
