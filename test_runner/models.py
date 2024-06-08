from django.db import models

# Create your models here.
class BaseModel(models.Model):
    id = models.AutoField(primary_key=True)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        abstract = True  # 将模型抽象，不会在数据库中生存对应的表


class Project(BaseModel):
    name = models.CharField("项目名称", max_length=100, null=False, unique=True)
    desc = models.CharField("项目描述", max_length=100, null=False)
    responsible = models.CharField("创建人", max_length=50, null=False)

    class Meta:
        verbose_name = "项目信息表"
        verbose_name_plural = verbose_name
        db_table = 'project'

    def __str__(self):  # 导出api时在Excel中显示项目名称
        return self.name


class Debugtalk(models.Model):
    code = models.TextField("python代码", default="# write you code", null=False)
    project = models.OneToOneField(to=Project, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "驱动文件表"
        verbose_name_plural = verbose_name
        db_table = 'debugtalk'

#实验手册7
class DataBaseConfig(BaseModel):
    database_type = (
        (1, "pa"),
        (2, "mysql"),
    )
    name = models.CharField("数据库名称", null=False, max_length=100)
    type = models.IntegerField("数据库类型", null=False, choices=database_type)
    server = models.CharField("数据库地址", null=False, max_length=100)
    account = models.CharField("数据库账号", null=False, max_length=50)
    password = models.CharField("数据库密码", null=False, max_length=100)
    desc = models.TextField("描述", null=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "数据库配置表"
        verbose_name_plural = verbose_name
        db_table = "database"

#实验手册8
class Variable(BaseModel):
    key = models.CharField("变量名称", null=False, max_length=100)
    value = models.CharField("变量值", null=False, max_length=1024)
    desc = models.CharField("简要介绍", max_length=500, null=True)
    create_user = models.CharField("创建人", null=True, max_length=20)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "全局变量表"
        verbose_name_plural = verbose_name
        db_table = "variable"

#实验手册10
class HostIP(BaseModel):
    name = models.CharField("HOST配置名称", null=False, max_length=100)
    value = models.TextField("配置值", null=False)
    create_user = models.CharField("创建人", null=True, max_length=20)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "环境配置表"
        verbose_name_plural = verbose_name
        db_table = "hostip"

#实验手册11
class Config(BaseModel):
    name = models.CharField("配置名称", null=False, max_length=100)
    body = models.TextField("主体信息", null=False)
    base_url = models.CharField("请求地址", null=False, max_length=100)
    configdesc = models.CharField("简要介绍", max_length=500, null=True, blank=True)
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE)
    create_user = models.CharField("创建人", null=True, max_length=20)

    class Meta:
        verbose_name = "配置信息表"
        verbose_name_plural = verbose_name
        db_table = "config"

class Pycode(BaseModel):
    code = models.TextField("python代码", default="# _*_ coding:utf-8 _*_", null=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField("驱动文件名", max_length=30, null=False)
    desc = models.CharField("简要介绍", max_length=100, null=True, blank=True)
    create_user = models.CharField("创建人", null=True, max_length=20)
    class Meta:
        db_table = "pycode"
        verbose_name = "驱动文件库"
        verbose_name_plural = verbose_name
        # 联合唯一
        unique_together = [['project', 'name']]

class Relation(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    tree = models.TextField("结构主题", null=False, default=[])
    type = models.IntegerField("树类型", default=1)#1表示API树，2表示测试用例树

    class Meta:
        verbose_name = "树形结构关系"
        verbose_name_plural = verbose_name
        db_table = "relation"

class Api(BaseModel):
    name = models.CharField("接口名称", null=False, max_length=500)
    body = models.TextField("主体信息", null=False)
    url = models.CharField("请求地址", null=False, max_length=500)
    method = models.CharField("请求方式", null=False, max_length=10)
    create_user = models.CharField("创建人", null=True, max_length=20)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    relation = models.CharField("节点id", null=False, max_length=50)

    class Meta:
        verbose_name = "API信息表"
        verbose_name_plural = verbose_name
        db_table = "api"


class Case(BaseModel):
    tag = (
        (1, "冒烟用例"),
        (2, "集成用例"),
        (3, "监控脚本"),
        (4, "回归用例"),
        (5, "系统用例"),
        (6, "空库用例")
    )
    apicaseid = models.CharField("api用例id", null=True, max_length=50)
    name = models.CharField("用例名称", null=False, max_length=200)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    relation = models.CharField("节点id", null=False, max_length=50)
    length = models.IntegerField("API个数", null=False)
    tag = models.IntegerField("用例标签", choices=tag, default=2)
    create_user = models.CharField("创建人", null=True, max_length=20)

    class Meta:
        verbose_name = "用例信息表"
        verbose_name_plural = verbose_name
        db_table = "case"

class CaseStep(BaseModel):
    name = models.CharField("用例名称", null=False, max_length=200)
    body = models.TextField("主体信息", null=False)
    url = models.CharField("请求地址", null=False, max_length=500)
    method = models.CharField("请求方式", null=False, max_length=10)
    case = models.ForeignKey(Case, on_delete=models.CASCADE)
    step = models.IntegerField("顺序", null=False)

    class Meta:
        verbose_name = "用例执行步骤表"
        verbose_name_plural = verbose_name
        db_table = "casestep"

class Report(BaseModel):
    report_type = (
        (1, "调试"),
        (2, "异步"),
        (3, "定时")
    )
    name = models.CharField("报告名称", null=False, max_length=100)
    type = models.IntegerField("报告类型", choices=report_type)
    summary = models.TextField("简要主体信息", null=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    report_id = models.CharField("报告ID", null=True, max_length=36)

    class Meta:
        verbose_name = "测试报告表"
        verbose_name_plural = verbose_name
        db_table = "report"

class ReportDetail(BaseModel):
    name = models.CharField("报告名称", null=False, max_length=100)
    summary = models.TextField("主体信息", null=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    report = models.OneToOneField(Report, on_delete=models.CASCADE)
    class Meta:
        verbose_name = "测试报告详情表"
        verbose_name_plural = verbose_name
        db_table = "reportDetail"