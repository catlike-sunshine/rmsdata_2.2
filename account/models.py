from django.db import models

# Create your models here.
from django.conf import settings 
 
# 建立一个用户信息模型，然后通过一对一关联字段，将用户信息模型和用户模型联系起来。
class Profile(models.Model): 
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) 
    date_of_birth = models.DateField(blank=True, null=True) 
    photo = models.ImageField(upload_to='user/%Y/%m/%d/', blank=True) 
 
    def __str__(self): 
        return "Profile for user {}".format(self.user.username)