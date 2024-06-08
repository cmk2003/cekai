from import_export import resources
from import_export.fields import Field

from test_runner.models import Variable, Api


class VariablesResource(resources.ModelResource):
    key = Field(attribute='key', column_name='变量名')
    value = Field(attribute='value', column_name='变量值')
    desc = Field(attribute='desc', column_name='描述')
    create_user = Field(attribute='create_user', column_name='创建人')

    class Meta:
        model = Variable
        fields = ('key', 'value', 'desc', 'create_user')
        export_order = ('key', 'value', 'desc', 'create_user')


class ApiResource(resources.ModelResource):
    name = Field(attribute='name', column_name='接口名称',)
    url = Field(attribute='url', column_name='接口路径')
    method = Field(attribute='method', column_name='请求类型')
    create_user = Field(attribute='create_user', column_name='创建人')
    project = Field(attribute='project', column_name='项目')
    body = Field(attribute='body', column_name='主体信息')

    class Meta:
        model = Api
        fields = ("name","url","method","body","create_user","project")
        export_order = ("name","url","method","body","create_user","project")