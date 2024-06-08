# Generated by Django 5.0.6 on 2024-06-08 11:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("test_runner", "0009_casestep"),
    ]

    operations = [
        migrations.CreateModel(
            name="Report",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "create_time",
                    models.DateTimeField(auto_now_add=True, verbose_name="创建时间"),
                ),
                (
                    "update_time",
                    models.DateTimeField(auto_now=True, verbose_name="更新时间"),
                ),
                ("name", models.CharField(max_length=100, verbose_name="报告名称")),
                (
                    "type",
                    models.IntegerField(
                        choices=[(1, "调试"), (2, "异步"), (3, "定时")], verbose_name="报告类型"
                    ),
                ),
                ("summary", models.TextField(verbose_name="简要主体信息")),
                (
                    "report_id",
                    models.CharField(max_length=36, null=True, verbose_name="报告ID"),
                ),
                (
                    "project",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="test_runner.project",
                    ),
                ),
            ],
            options={
                "verbose_name": "测试报告表",
                "verbose_name_plural": "测试报告表",
                "db_table": "report",
            },
        ),
        migrations.CreateModel(
            name="ReportDetail",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "create_time",
                    models.DateTimeField(auto_now_add=True, verbose_name="创建时间"),
                ),
                (
                    "update_time",
                    models.DateTimeField(auto_now=True, verbose_name="更新时间"),
                ),
                ("name", models.CharField(max_length=100, verbose_name="报告名称")),
                ("summary", models.TextField(verbose_name="主体信息")),
                (
                    "project",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="test_runner.project",
                    ),
                ),
                (
                    "report",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="test_runner.report",
                    ),
                ),
            ],
            options={
                "verbose_name": "测试报告详情表",
                "verbose_name_plural": "测试报告详情表",
                "db_table": "reportDetail",
            },
        ),
    ]
