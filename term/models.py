from django.db import models
from taggit.managers import TaggableManager
from data_platform.models import acmodel

# Create your models here.

#术语所用的分类
class term_category(models.Model):
    id = models.AutoField(primary_key = True)
    name = models.CharField('名称',max_length=200, db_index=True)
    slug = models.SlugField('简称',max_length=200, db_index=True, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = '术语分类'
        verbose_name_plural = '术语分类'

    def __str__(self):
        return self.name


#缩略语所用的分类
class acr_category(models.Model):
    id = models.AutoField(primary_key = True)
    name = models.CharField('名称',max_length=200, db_index=True)
    slug = models.SlugField('简称',max_length=200, db_index=True, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = '缩略语分类'
        verbose_name_plural = '缩略语分类'

    def __str__(self):
        return self.name

#术语定义部分内容
class term(models.Model):
    id = models.AutoField(primary_key = True)
    category = models.ForeignKey(term_category, related_name='acr_category', on_delete=models.CASCADE, default = '无分类')
    title = models.CharField("词条", max_length = 200)
    content = models.TextField("词条说明")
    acmodel = models.ForeignKey(acmodel, related_name='适用机型',on_delete = models.CASCADE, limit_choices_to={'if_intra_ac': True})
    tag = TaggableManager("标签",blank=True)
    source = models.TextField("词条来源")

    class Meta:
        ordering = ('title',)
        verbose_name = '术语'
        verbose_name_plural = '术语'

    def __str__(self):
        return (self.title)

#缩略语
class acronym(models.Model):
    id = models.AutoField(primary_key = True)
    name = models.CharField("缩略语", max_length = 200)
    category = models.ForeignKey(acr_category, related_name='acr_category', on_delete=models.CASCADE, default = '无分类')
    full_name = models.TextField("英文全称")
    zh_name = models.TextField("中文全称")
    tag = TaggableManager("标签",blank=True)

    class Meta:
        ordering = ('name',)
        verbose_name = '缩略语'
        verbose_name_plural = '缩略语'

    def __str__(self):
        return (self.name)
