from django.db import models

# Create your models here.
#机型
class aircraft_type(models.Model):
    id = models.AutoField(primary_key = True)
    aircraft_type_number = models.TextField("机型编号")
    
    def __str__(self):
        return (self.aircraft_type_number)
    
    class Meta:
        ordering = ('aircraft_type_number',)
        verbose_name = '机型'
        verbose_name_plural = verbose_name

#ATA章节
class ATA(models.Model):
    id = models.AutoField(primary_key = True)
    major = models.TextField('专业')
    chapter = models.DecimalField('章', max_digits = 3, decimal_places = 0)
    section = models.DecimalField('节', max_digits = 3, decimal_places = 0)
    subject = models.DecimalField('题', max_digits = 3, decimal_places = 0)
    
    def __str__(self):
        return (self.chapter+'.'+self.section+'.'+self.subject)
    
    class Meta:
        ordering = ('chapter','section','subject')
        verbose_name = 'ATA章节'
        verbose_name_plural = verbose_name
   
 #航空器信息
class aircraft_info(models.Model):
    aircraft_serial_number = models.DecimalField(primary_key = True, max_digits = 9, decimal_places = 0)
    aircraft_operator = models.TextField('飞机拥有者')
    flight_cycles = models.DecimalField('飞行循环',max_digits = 7, decimal_places = 0)
    flight_hours = models.DecimalField('飞行小时',max_digits = 9, decimal_places = 2)
    record_time = models.DateField("飞行记录时间")
    
    def __str__(self):
        return str(self.aircraft_serial_number)
    
    class Meta:
        ordering = ('aircraft_serial_number',)
        verbose_name = '航空器信息'
        verbose_name_plural = verbose_name

 #事件清单
class event_list(models.Model):
    internal_number = models.TextField('内部编号', primary_key = True)
    attachment_info = models.TextField('附件信息')
    corrective_action = models.TextField('纠正文本')
    event_descrption = models.TextField('问题描述')
    failure_number = models.TextField('故障编号')
    failure_part_name = models.TextField('故障件名称')
    failure_part_number = models.TextField('故障件件号')
    flight_phase = models.TextField('飞行阶段')
    handling_suggestion = models.TextField('问题关闭情况')
    if_tech_question = models.BooleanField('是否技术问题', default = False)
    occurrence_time = models.DateField('发生时间')
    other_number = models.TextField('其他编号')
    task_classification = models.TextField('任务分类')
    task_number = models.TextField('任务编号')
    troubleshooting = models.TextField('排故概况')
    
    def __str__(self):
        return (self.task_number)
    
    class Meta:
        ordering = ('event_descrption','task_number')
        verbose_name = '事件清单'
        verbose_name_plural = verbose_name