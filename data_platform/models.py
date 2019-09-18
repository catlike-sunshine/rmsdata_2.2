from django.db import models
from taggit.managers import TaggableManager

# Create your models here.

#单独建立的用户模型
class  user(models.Model):
  id = models.AutoField(primary_key = True)
  name =  models.CharField(max_length = 100)
  info = models.CharField(max_length = 200, default = "na")


#机型数据模型
class acmodel(models.Model):
    id = models.AutoField(primary_key = True)
    aircraft_type = models.CharField("基本型号", max_length = 100)
    aircraft_serial_number = models.CharField("扩展型号", max_length = 100)
    if_intra_ac = models.BooleanField(default = False)

    class Meta:
        ordering = ('aircraft_type',)
        verbose_name = '飞机型号'
        verbose_name_plural = '飞机型号'

    def __str__(self):
        return (self.aircraft_type)
    
