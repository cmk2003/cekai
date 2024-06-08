import hashlib
import time
import random
from django.db import models
from django.contrib.auth.models import AbstractUser
from test_runner.models import Project, BaseModel


# Create your models here.
class TokenManager(models.Manager):
    def md5(self,s):
        h=hashlib.md5()
        h.update(s.encode(encoding='utf-8'))
        return h.hexdigest()
    def random_token(self):
        return self.md5(str(time.time())+str(random.randint(1,1000)))
    def create_token(self,user):
        return UserToken.objects.create(user=user,token=self.random_token())

class User(AbstractUser):
    name=models.CharField('用户真实姓名',max_length=20,null=False,default="管理员")

    belong_project=models.ManyToManyField(Project,
                                          blank=True,
                                          help_text="所属项目",
                                          related_name="user_set",
                                          related_query_name="user")





    class Meta:
        verbose_name="用户信息表"
        verbose_name_plural=verbose_name
        db_table='user'


class UserToken(models.Model):
    create_time=models.DateTimeField('创建时间',auto_now=True)
    update_time=models.DateTimeField('更新时间',auto_now=True)
    user=models.OneToOneField(to=User,on_delete=models.CASCADE)
    token=models.CharField('token',max_length=1000)

    objects=TokenManager()
    class Meta:
        verbose_name="用户登录token表"
        verbose_name_plural=verbose_name
        db_table='user_token'


