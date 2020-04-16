from django.db import models

# Create your models here.
from dadashop13.tools.models import BaseModel


class UserProfile(BaseModel):

    username = models.CharField(max_length=11,verbose_name='用户名',unique=True)
    password = models.CharField(max_length=32,verbose_name='密码')
    email = models.EmailField()
    phone = models.CharField(max_length=11)
    is_avtive = models.BooleanField(default=False,verbose_name='激活状态')

    class Meta:
        db_table = 'user_user_profile'

    def __str__(self):
        return '%s-%s'%(self.id,self.username)
