from django.db import models
from taggit.managers import TaggableManager
from ckeditor.fields import RichTextField
# Create your models here.

#下载内容所用的分类
class file_category(models.Model):
    name = models.CharField('名称',max_length=200, db_index=True)
    slug = models.SlugField('简称',max_length=200, db_index=True, unique=True)
    content = RichTextField('说明')

    class Meta:
        ordering = ('name',)
        verbose_name = '数据分类'
        verbose_name_plural = '数据分类'

    def __str__(self):
        return self.name

class file(models.Model):
    slug = models. SlugField(max_length=200, db_index=True)
    category = models.ForeignKey(file_category, related_name='file_category', on_delete=models.CASCADE)
    content = RichTextField("数据说明")
    date = models.DateField("数据产生时间")
    file = models.FileField(upload_to='datafile/%Y/%m/%d', blank=True)

    class Meta:
        verbose_name = '数据列表'
        verbose_name_plural = '数据列表'

    def __str__(self):
        return self.content
