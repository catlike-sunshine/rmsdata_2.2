from django.db import models
from data_platform.models import acmodel

# Create your models here.
#ATA章节
class ata(models.Model):
    id = models.AutoField(primary_key = True)
    chapter = models.DecimalField("章", max_digits=2, decimal_places=0)
    section = models.DecimalField("节", max_digits=2, decimal_places=0)
    subject = models.DecimalField("题", max_digits=2, decimal_places=0)
    title = models.CharField("系统名称", max_length = 100)
    zh_title = models.CharField("系统名称(中)", max_length = 100)

    class Meta:
        ordering = ('chapter',)
        verbose_name = 'ATA章节'
        verbose_name_plural = 'ATA章节'

    def __str__(self):
        return (self.zh_title)


#航空器
class aircraft(models.Model):
    id = models.AutoField(primary_key = True)
    aircraft_registration_number = models.CharField("航空器注册号", max_length = 100)
    production_serial_number = models.CharField('产品系列号', max_length = 100)
    acmodel = models.ForeignKey(acmodel, related_name='aircraft_acmodel', on_delete = models.CASCADE)

    class Meta:
        ordering = ('aircraft_registration_number',)
        verbose_name = '航空器'
        verbose_name_plural = '航空器'

    def __str__(self):
        return (self.aircraft_registration_number)

    
#发动机型号
class engine_type(models.Model):
    id = models.AutoField(primary_key = True)
    engine_type_number = models.CharField("发动机型号", max_length = 100)
    
    class Meta:
        ordering = ('engine_type_number',)
        verbose_name = '发动机型号'
        verbose_name_plural = '发动机型号'

    def __str__(self):
        return (self.engine_type_number)
    
    
#发动机
class engine(models.Model):
    id = models.AutoField(primary_key = True)
    engine_type = models.ForeignKey(engine_type, related_name='engine_engine_type', on_delete = models.CASCADE)
    aircraft = models.ForeignKey(aircraft, related_name='engine_aircraft', on_delete = models.CASCADE)
    engine_serial_number = models.CharField("发动机序号", max_length = 100)
    

    class Meta:
        ordering = ('engine_type',)
        verbose_name = '发动机'
        verbose_name_plural = '发动机'

    def __str__(self):
        return (self.engine_serial_number)

    
#航空器信息
class aircraft_info(models.Model):
    id = models.AutoField(primary_key = True)
    aircraft= models.ForeignKey(aircraft, related_name='aircraft_information_aircraft', on_delete = models.CASCADE,null=True)
    monthly_available_days = models.DecimalField("在用架日", max_digits=3, decimal_places=0)
    monthly_total_flight_hours = models.DecimalField("当月总飞行时间", max_digits=6, decimal_places=2)
    monthly_flight_times = models.DecimalField("当月总起落架次", max_digits=6, decimal_places=0)
    monthly_service_flight_hours = models.DecimalField("当月营运飞行时间", max_digits=6, decimal_places=2)
    monthly_service_flight_times = models.DecimalField("当月营运起落次数", max_digits=6, decimal_places=0)
    cumulative_flight_hours = models.DecimalField("累积飞行时间", max_digits=9, decimal_places=2)
    cumulative_flight_times = models.DecimalField("累积飞行起落次数", max_digits=9, decimal_places=0)
    date = models.DateField("日期")
    company = models.CharField("公司", max_length = 100)

    def __str__(self):
        return (self.acmodel)
    
    class Meta:
        ordering = ('aircraft',)
        verbose_name = '航空器信息'
        verbose_name_plural = '航空器信息'


#发动机使用记录
class engine_using_record(models.Model):
    id = models.AutoField(primary_key = True)
    engine = models.ForeignKey(engine, related_name='engine', on_delete=models.CASCADE)
    installed_position = models.CharField("装机位置", max_length=4)
    monthly_service_hours = models.DecimalField("当月使用时间", max_digits=6, decimal_places=2)
    monthly_service_cycles = models.DecimalField("当月使用循环", max_digits=6, decimal_places=0)
    if_overhaul = models.BooleanField('当月是否大修',default = False)
    service_hours_after_repair= models.DecimalField("修后使用时间", max_digits=6, decimal_places=2)
    service_cycles_after_repair = models.DecimalField("修后使用循环", max_digits=6, decimal_places=0)
    total_service_hours = models.DecimalField("总使用时间", max_digits=9, decimal_places=2)
    total_service_cycles = models.DecimalField("总使用循环", max_digits=9, decimal_places=0)
    date = models.DateField("日期")
    replacement_reason = models.TextField("拆换原因")
    maintenance = models.TextField("维修")
    scope_of_work = models.TextField("工作范围")

    def __str__(self):
        return (self.engine)
    
    class Meta:
        ordering = ('engine',)
        verbose_name = '发动机使用记录'
        verbose_name_plural = '发动机使用记录'
    

#APU使用记录
class apu_using_record(models.Model):
    id = models.AutoField(primary_key = True)
    acmodel = models.ForeignKey(acmodel, related_name='apu_using_record_acmodel', on_delete = models.CASCADE)
    apu_part_number = models.CharField("APU件号", max_length = 20)
    monthly_service_hours = models.DecimalField("当月使用时间", max_digits=6, decimal_places=2)
    monthly_service_cycles = models.DecimalField("当月使用循环", max_digits=6, decimal_places=0)
    total_service_hours = models.DecimalField("总使用时间", max_digits=9, decimal_places=0)
    total_service_cycles = models.DecimalField("总使用循环", max_digits=9, decimal_places=0)
    scheduled_replacement = models.CharField("计划拆换", max_length=100)
    unscheduled_replacement = models.CharField("非计划拆换", max_length=100)
    date = models.DateField("日期")

    def __str__(self):
        return (self.apu_part_number)
    
    class Meta:
        ordering = ('apu_part_number',)
        verbose_name = 'APU使用记录'
        verbose_name_plural = 'APU使用记录'
    

#航空器信息变化表
class aircraft_info_change(models.Model):
    id = models.AutoField(primary_key = True)
    aircraft = models.ForeignKey(aircraft, related_name='aircraft_info_change_aircraft', on_delete = models.CASCADE)
    in_or_out = models.CharField('引进或转出', max_length=100)
    current_aircraft_operator = models.CharField('当前所属航空器运营人', max_length=100)
    original_aircraft_operator = models.CharField('原所属航空器运营人', max_length=100)
    in_or_out_reason = models.CharField('引入或转出原因', max_length=100)
    date = models.DateField('日期')
    method = models.CharField('方式', max_length=100)
    
    class Meta:
        ordering = ('date',)
        verbose_name = '航空器信息变化表'
        verbose_name_plural = '航空器信息变化表'

    def __str__(self):
        return (self.in_or_out)
    

#发动机信息变化表
class engine_info_change(models.Model):
    id = models.AutoField(primary_key = True)
    engine = models.ForeignKey(engine, related_name='engine_info_change_engine', on_delete = models.CASCADE)
    in_or_out = models.CharField('引进或转出', max_length=100)
    current_aircraft_operator = models.CharField('当前所属航空器运营人', max_length=100)
    original_aircraft_operator = models.CharField('原所属航空器运营人', max_length=100)
    in_or_out_reason = models.CharField('引入或转出原因', max_length=100)
    date = models.DateField('日期')
    
    class Meta:
        ordering = ('date',)
        verbose_name = '发动机信息变化表'
        verbose_name_plural = '发动机信息变化表'

    def __str__(self):
        return (self.in_or_out)


#发动机拆换记录
class record_of_engine_replaced(models.Model):
    id = models.AutoField(primary_key = True)
    engine = models.ForeignKey(engine, related_name='record_of_engine_replace_engine', on_delete = models.CASCADE)
    installed_position = models.CharField('装机位置', max_length=100)
    remove_time = models.DateField('拆下时间')
    replacement_type = models.CharField('拆卸类型', max_length=100)
    check_and_discovery = models.CharField('检查发现', max_length=100)
    maintenance_measure = models.CharField('维修措施', max_length=100)
    single_service_hours = models.DecimalField('本次使用时间', max_digits = 6, decimal_places = 2)
    single_service_cycles = models.DecimalField('本次使用循环', max_digits = 6, decimal_places = 0)
    total_service_hours = models.DecimalField('总使用时间', max_digits = 9, decimal_places = 2)
    total_service_cycles = models.DecimalField('总使用循环', max_digits = 9, decimal_places = 0)
    replacement_reason = models.CharField('拆换原因', max_length=100)
    scope_of_work = models.CharField('工作范围', max_length=100)
    
    class Meta:
        ordering = ('engine',)
        verbose_name = '发动机拆换记录'
        verbose_name_plural = '发动机拆换记录'

    def __str__(self):
        return (self.engine)
 
 
#部件拆换记录
class record_of_part_replaced(models.Model):
    id = models.AutoField(primary_key = True)
    aircraft = models.ForeignKey(aircraft, related_name='record_of_part_replace_aircraft', on_delete = models.CASCADE)
    ata = models.ForeignKey(ata, related_name='record_of_part_replace_ata', on_delete = models.CASCADE)
    flight_number = models.CharField('航班号', max_length=100)
    date = models.DateField('时间')
    replacement_type = models.CharField('拆换类型', max_length=100)
    replacement_reason = models.CharField('拆换原因', max_length=100)
    failure_discovery = models.CharField('故障发现', max_length=100)
    failure_confirmation = models.CharField('故障确认', max_length=100)
    part_replaced_name = models.CharField('拆换件名称', max_length=100)
    part_replaced_numbers = models.CharField('拆下件数量', max_length=100)
    part_installed_numbers = models.CharField('安装件数量', max_length=100)
    part_removed_serial_number = models.CharField('拆下件序列号', max_length=100)
    part_installed_serial_number = models.CharField('安装件序列号', max_length=100)
    replacement_work_type = models.CharField('拆换工作类型', max_length=100, null = True)
    maintenance_level = models.CharField('维修级别', max_length=100)
    advanced_device = models.CharField('高级设备', max_length=100)
    failure_handling = models.CharField('故障处理', max_length=100)
    
    class Meta:
        ordering = ('part_replaced_name',)
        verbose_name = '部件拆换记录'
        verbose_name_plural = '部件拆换记录'

    def __str__(self):
        return (self.part_replaced_name)

    
#计划维修记录
class record_of_scheduled_maintenance(models.Model):
    id = models.AutoField(primary_key = True)
    aircraft = models.ForeignKey(aircraft, related_name='record_of_scheduled_maintenance_aircraft', on_delete = models.CASCADE)
    ata = models.ForeignKey(ata, related_name='record_of_scheduled_maintenance_ata', on_delete = models.CASCADE)
    task_number = models.CharField('工卡号/任务号', max_length=100)
    date = models.DateField('日期')
    task_description = models.CharField('任务描述', max_length=100)
    task_source = models.CharField('任务来源', max_length=100)
    check_intervals = models.CharField('检查间隔', max_length=100)
    reference_material = models.CharField('参考资料', max_length=100)
    cumulative_flight_hours = models.DecimalField('累计飞行时间', max_digits = 9, decimal_places = 2)
    cumulative_flight_times = models.DecimalField('累计起落次数', max_digits = 9, decimal_places = 0)
    flight_hours_after_last_check = models.DecimalField('上次检查后飞行时间', max_digits = 9, decimal_places = 2)
    flight_times_after_last_check = models.DecimalField('上次检查后起落次数', max_digits = 9, decimal_places = 0)
    check_discovery = models.CharField('检查发现', max_length=100)
    troubleshooting_measures = models.CharField('排故措施', max_length=100)
    
    class Meta:
        ordering = ('task_number',)
        verbose_name = '计划维修记录'
        verbose_name_plural = '计划维修记录'

    def __str__(self):
        return (self.task_number)
    
    
#发动机空中停车记录
class engine_air_stop_record(models.Model):
    id = models.AutoField(primary_key = True)
    engine = models.ForeignKey(engine, related_name='engine_air_stop_record_engine', on_delete= models.CASCADE)
    flight_number = models.CharField("航班号", max_length=8)
    installed_position = models.CharField("装机位置", max_length=4)
    air_stop_time = models.DateField("空中停车时间")
    occurrence_phase = models.CharField("发生阶段", max_length=8)
    occurrence_place = models.CharField("发生地点", max_length=8)
    event_description = models.TextField("事件描述")
    reason_analysis = models.TextField("原因分析")
    
    def __str__(self):
        return (self.engine)
    
    class Meta:
        ordering = ('engine',)
        verbose_name = '发动机停车记录'
        verbose_name_plural = '发动机停车记录'
        
        
#故障报告记录
class failure_report_record(models.Model):
    id = models.AutoField(primary_key = True)
    aircraft = models.ForeignKey(aircraft, related_name='failure_report_record_aircraft', on_delete= models.CASCADE)
    ata = models.ForeignKey(ata, related_name='failure_report_record_ata', on_delete= models.CASCADE)
    flight_number = models.CharField("航班号", max_length=8) 
    occurrence_time = models.DateField("发生时间")
    occurrence_place = models.CharField("发生地点", max_length=8)
    failure_report_number = models.CharField("故障报告编号", max_length=8)
    occurrence_phase = models.CharField("发生阶段", max_length=8)
    report_source = models.TextField("报告来源")
    failure_name_code = models.CharField("故障名称/编码", max_length=8)
    failure_description = models.TextField("故障描述")
    failure_phenomenon = models.TextField("故障现象")
    troubleshooting_measures = models.TextField("处理措施")
    maintenance_level = models.CharField("维修级别", max_length=8)
    failure_class = models.CharField("故障类别", max_length=8)
    importance_degree = models.CharField("重要程度", max_length=8)
    information_category_content = models.TextField("信息类别内容")
    failure_type = models.CharField("故障类别", max_length=8)
    airport_terminal = models.CharField("航站", max_length=8)
    
    def __str__(self):
        return (self.failure_report_number)
    
    class Meta:
        ordering = ('importance_degree',)
        verbose_name = '故障报告记录'
        verbose_name_plural = '故障报告记录'
        
        
#航班不正常报告
class abnormal_flight_report(models.Model):
    id = models.AutoField(primary_key = True)
    aircraft = models.ForeignKey(aircraft, related_name='abnormal_flight_report_aircraft', on_delete= models.CASCADE)
    ata = models.ForeignKey(ata, related_name='abnormal_flight_report_ata', 
                            on_delete= models.CASCADE)
    flight_number = models.CharField("航班号", max_length=8) 
    occurrence_time = models.DateField("发生时间")
    occurrence_place = models.CharField("发生地点", max_length=8)
    occurrence_phase = models.CharField("发生阶段", max_length=8)
    failure_report_number = models.CharField("故障报告编号", max_length=8)
    failure_description = models.TextField("故障描述")
    delay_hours = models.DecimalField('延误时间/分钟', max_digits = 9, 
                                      decimal_places = 2)
    consequence = models.TextField("后果")
    part_replaced_name = models.CharField("拆换件名称", max_length=8)
    part_replaced_number = models.CharField("拆换件件号", max_length=8)
    part_replaced_serial_number = models.CharField("拆换件序号", max_length=8)
    TSR = models.CharField(max_length=8)
    TSN = models.CharField(max_length=8)
    event_survey_summary = models.TextField("事件调查总结")
    belong_to_region = models.CharField("所属区域", max_length=8)
    wether_to_start = models.BooleanField('是否始发',default = False)
    event_analysis = models.TextField("事件分析")
    delay_quality = models.CharField("延误定性", max_length=8)
    improvement_measures_resolutions = models.TextField("改进措施与决议")
    departure_planned_time = models.DateField("计划起飞时间")
    departure_actual_time = models.DateField("实际起飞时间")
    major = models.CharField("专业", max_length=8)
    
    def __str__(self):
        return (self.failure_report_number)
    
    class Meta:
        ordering = ('delay_quality',)
        verbose_name = '航班不正常报告'
        verbose_name_plural = '航班不正常报告'

    
#使用困难报告
class use_difficult_report(models.Model):
    id = models.AutoField(primary_key = True)
    aircraft = models.ForeignKey(aircraft, related_name='use_difficult_report_aircraft', on_delete= models.CASCADE)
    ata = models.ForeignKey(ata, related_name='use_difficult_report_ata', on_delete= models.CASCADE)
    flight_number = models.CharField("航班号", max_length=8)
    report_number = models.CharField("报告编号", max_length=8)
    service_varity = models.CharField("运营种类", max_length=8)
    occurrence_time = models.DateField("发生时间")
    occurrence_place = models.CharField("发生地点", max_length=8)
    occurrence_phase = models.CharField("发生阶段", max_length=8)
    event_description_improvement_measures = models.TextField("问题描述和纠正措施")
    preventive_emergency_measures = models.TextField("预防紧急措施")
    failure_exchange_part_name = models.CharField("故障件/更换件名称",
                                                  max_length=8)
    
    def __str__(self):
        return (self.report_number)
    
    class Meta:
        ordering = ('service_varity',)
        verbose_name = '使用困难报告'
        verbose_name_plural = '使用困难报告'

    
#故障模式库
class failure_mode_bank(models.Model):
    id = models.AutoField(primary_key = True)
    acmodel = models.ForeignKey(acmodel, related_name='failure_mode_bank_acmodel', on_delete = models.CASCADE, default = 1)
    failure_mode = models.TextField("故障模式")
    ata = models.ForeignKey(ata, related_name = 'failure_mode_bank_ata', on_delete = models.CASCADE)
    failure_consequence = models.TextField("故障影响后果")
    failure_reason = models.TextField("故障原因")
    failure_troubleshooting = models.TextField("故障解决措施")

    class Meta:
        ordering = ('failure_mode',)
        verbose_name = '故障模式库'
        verbose_name_plural = '故障模式库'

    def __str__(self):
        return (self.failure_mode)


#-----------------------------------------------------------------------------
#相似机型第二批数据
#飞行时间和起落次数表
class flight_hours_and_upAndDown_amounts_table(models.Model):
    id = models.AutoField(primary_key = True)
    aircraft = models.OneToOneField(aircraft, related_name='flight_hours_and_upAndDown_amounts_table_aircraft', 
																		on_delete= models.CASCADE)
    total_flight_hours = models.DecimalField('总飞行时间', max_digits = 9, decimal_places = 2)
    total_flight_cycles = models.DecimalField('总飞行循环', max_digits = 9, decimal_places = 0)
    total_flight_days = models.DecimalField('总飞行天数', max_digits = 9, decimal_places = 0)
    monthly_record_amounts = models.DecimalField('本月记录次数', max_digits = 9, decimal_places = 0)
    monthly_air_flight_hours = models.DecimalField('本月飞行小时（空中）', max_digits = 9, decimal_places = 2)
    monthly_flight_cycles = models.DecimalField('本月飞行循环', max_digits = 9, decimal_places = 0)
    monthly_space_flight_hours = models.DecimalField('本月飞行小时（空地）', max_digits = 9, decimal_places = 2)
    monthly_service_flight_hours = models.DecimalField('本月营运飞行小时', max_digits = 9, decimal_places = 2)
    monthly_non_service_flight_hours = models.DecimalField('本月非营运飞行小时', max_digits = 9, decimal_places = 2)
    monthly_available_days = models.DecimalField('本月可用架日', max_digits = 9, decimal_places = 0)
    monthly_service_flight_cycles = models.DecimalField('本月营运飞行循环', max_digits = 9, decimal_places = 0)
    monthly_non_service_flight_cycles = models.DecimalField('本月非营运飞行循环', max_digits = 9, decimal_places = 0)
    monthly_flight_amounts = models.DecimalField('本月航班数', max_digits = 9, decimal_places = 0)
    date = models.DateField("日期", max_length=8)
    year = models.DecimalField('年份', max_digits = 9, decimal_places = 0)
    month = models.DecimalField('月份', max_digits = 9, decimal_places = 0)
    monthly_successive_upAndDown = models.DecimalField('本月连续起落', max_digits = 9, decimal_places = 0)
    
    
    def __str__(self):
        return (self.aircraft)
    
    class Meta:
        ordering = ('total_flight_hours',)
        verbose_name = '飞行时间和起落次数表'
        verbose_name_plural = verbose_name
				
				
#航班总数据
class flight_data(models.Model):
	id = models.AutoField(primary_key = True)
	acmodel = models.ForeignKey(acmodel, related_name='flight_data_acmodel', 
										 on_delete= models.CASCADE)
	flight_number = models.CharField("航班号", max_length=8)	
	date = models.DateField("日期", max_length=8)
	character = models.CharField("性质", max_length=8)
	cockpit_layout = models.CharField("座舱布局", max_length=8)
	passenger_amounts = models.DecimalField('旅客人数', max_digits = 9, decimal_places = 0)
	airport_of_departure = models.CharField("起飞机场", max_length=8)
	airport_of_destination = models.CharField("到达机场", max_length=8)
	scheduled_departure_hours = models.DateTimeField('计划离岗', max_length=8)
	actual_departure_hours = models.DateTimeField('实际离岗', max_length=8)
	flight_departure = models.DateTimeField('航班起飞', max_length=8)
	flight_arrival = models.DateTimeField('航班到达', max_length=8)
	scheduled_arrival_hours  = models.DateTimeField('计划到港', max_length=8)
	actual_arrival_hours  = models.DateTimeField('实际到港', max_length=8)
	door_closing_hours  = models.DateTimeField('关舱时间', max_length=8)
	door_opening_hours  = models.DateTimeField('开舱时间', max_length=8)
    
    
	def __str__(self):
		return (self.acmodel)
    
	class Meta:
		ordering = ('date',)
		verbose_name = '航班总数据'
		verbose_name_plural = verbose_name
		
		
#非计划拆换记录
class unscheduled_replacement_record(models.Model):
	id = models.AutoField(primary_key = True)
	aircraft = models.ForeignKey(aircraft, related_name='unscheduled_replacement_record_aircraft', 
										 on_delete= models.CASCADE)
	ata= models.ForeignKey(ata, related_name='unscheduled_replacement_record_ata', on_delete= models.CASCADE)
	part_number = models.CharField("件号", max_length = 100)
	sequence_number = models.CharField("序号", max_length=8)
	unscheduled = models.CharField("非计划", max_length=8)
	failure_confirmation = models.CharField("故障确认", max_length=8)
	replacement_reason = models.TextField("拆换原因") 
	installation_date = models.DateField("安装日期", max_length = 8)
	part_installed_flight_hours = models.DecimalField('部件装上飞行小时数', max_digits = 9, decimal_places = 2)
	part_installed_flight_cycles = models.DecimalField('部件装上飞行循环', max_digits = 9, decimal_places = 0)
	part_installed_using_hours = models.DecimalField('部件装上使用小时数', max_digits = 9, decimal_places = 2)
	part_installed_using_cycles = models.DecimalField('部件装上使用循环数', max_digits = 9, decimal_places = 0)
	replacement_date = models.DateField("拆换日期", max_length = 8)
	month = models.DecimalField('月份', max_digits = 9, decimal_places = 0)
	part_removed_flight_hours = models.DecimalField('部件拆下飞行小时数', max_digits = 9, decimal_places = 2)
	part_removed_flight_cycles  = models.DecimalField('部件拆下飞行循环数', max_digits = 9, decimal_places = 0)
	part_removed_using_hours = models.DecimalField('部件拆下使用小时数', max_digits = 9, decimal_places = 2)
	part_removed_using_cycles  = models.DecimalField('部件拆下使用循环数', max_digits = 9, decimal_places = 0)
	failure_description = models.TextField("故障描述")
	part_installed_this_using_hours = models.DecimalField('部件本次装机使用小时', max_digits = 9, decimal_places = 2)
	failure_handing = models.TextField("故障处理")
	part_installed_this_using_cycles = models.DecimalField('部件本次装机使用循环', max_digits = 9, decimal_places = 0)
	part_installed_number = models.CharField("装上部件件号", max_length = 100)
	part_installed_sequence_number = models.CharField("装上部件序号", max_length = 100)
	recently_repair_company = models.DecimalField('最近送修公司', max_digits = 9, decimal_places = 2)
	CY_TSN = models.DecimalField('CY_TSN', max_digits = 9, decimal_places = 0)
	FH_TSN = models.DecimalField('FH_TSN', max_digits = 9, decimal_places = 2)
	repair_to_remove_hours = models.DecimalField('送修至拆下时间', max_digits = 9, decimal_places = 2)
	repair_to_remove_cycles = models.DecimalField('送修至拆下时间', max_digits = 9, decimal_places = 0)
	part_number_description = models.CharField("件号描述", max_length = 100)

	
	def __str__(self):
		return (self.aircraft)
    
	
	class Meta:
		ordering = ('ata',)
		verbose_name = '非计划拆换记录'
		verbose_name_plural = verbose_name
		
		
#MTBUR
class MTBUR(models.Model):
	id = models.AutoField(primary_key = True)
	ata= models.ForeignKey(ata, related_name='MTBUR_ata', on_delete= models.CASCADE)
	part_number = models.CharField("件号", max_length = 100)
	part_number_description = models.CharField("件号描述", max_length = 100)
	year = models.DecimalField('年份', max_digits = 9, decimal_places = 0)
	QPA = models.DecimalField('QPA', max_digits = 9, decimal_places = 2)
	unscheduled_replacement_amounts = models.DecimalField('非计划拆换数', max_digits = 9, decimal_places = 0)
	confirmed_failure_amounts = models.DecimalField('确认故障数', max_digits = 9, decimal_places = 0)
	part_flight_hours = models.DecimalField('部件飞行小时', max_digits = 9, decimal_places = 2)
	MTBUR = models.DecimalField('MTBUR', max_digits = 9, decimal_places = 2)
	MTBF = models.DecimalField('MTBF', max_digits = 9, decimal_places = 2)
	    
	
	def __str__(self):
		return (self.MTBUR)
    
	
	class Meta:
		ordering = ('year',)
		verbose_name = 'MTBUR'
		verbose_name_plural = verbose_name
		
		
#航线维修工统计
class airline_maintenance_hours_statistics(models.Model):
	id = models.AutoField(primary_key = True)
	aircraft = models.ForeignKey(aircraft, related_name='airline_maintenance_hours_statistics_aircraft', 
										 on_delete= models.CASCADE)
	ata= models.ForeignKey(ata, related_name='airline_maintenance_hours_statistics_ata', on_delete= models.CASCADE)
	date = models.DateField("日期", max_length=8)
	working_hours = models.DecimalField('工时', max_digits = 9, decimal_places = 0)
	maintenance_hours = models.DecimalField('维修花费时间', max_digits = 9, decimal_places = 2)
	failure_phenomenon = models.TextField("故障现象")
	failure_handing = models.TextField("故障处理")
	    
	
	def __str__(self):
		return (self.maintenance_hours)
    
	
	class Meta:
		ordering = ('date',)
		verbose_name = '航线维修工统计'
		verbose_name_plural = verbose_name
		
		
#工作包信息
class work_package_information(models.Model):
	id = models.AutoField(primary_key = True)
	aircraft = models.ForeignKey(aircraft, related_name='work_package_information_aircraft', 
										 on_delete= models.CASCADE)
	work_package_name = models.CharField("工作包名称", max_length = 100)
	work_package_type = models.CharField("工作包类型", max_length = 100)
	achievement_hours = models.DateField("完工时间", max_length=8)
	working_hour_amounts = models.DecimalField('工时数', max_digits = 9, decimal_places = 2)
	aviation_material_price = models.DecimalField('航材定价', max_digits = 9, decimal_places = 2)
	    
	
	def __str__(self):
		return (self.work_package_name)
    
	
	class Meta:
		ordering = ('achievement_hours',)
		verbose_name = '工作包信息'
		verbose_name_plural = verbose_name
        
#事故事件
class accident(models.Model):
    id = models.AutoField(primary_key = True)
    aircraft = models.ForeignKey(aircraft, related_name='accident_aircraft', 
										 on_delete= models.CASCADE)
    title = models.TextField("事故名称")
    flight_number = models.TextField("航班号")
    manufacture_country = models.TextField("运营商所属国家")
    operator = models.TextField("运营商")
    occurrence_time = models.DateField("事故时间")
    flight_type = models.TextField("飞行性质")
    flight_phase = models.TextField("阶段")
    death_toll = models.DecimalField("死亡人数", max_digits = 6, decimal_places = 0)
    occurrence_region = models.TextField("事故地区")
    occurrence_place = models.TextField("事故地点")
    departure = models.TextField("出发地")
    destination = models.TextField("目的地")
    accident_factor = models.TextField("事故因素分类")
    accident_level = models.TextField("事故等级")
    description = models.TextField("事故描述")
    reason = models.TextField("原因分析")
    measurement = models.TextField("采取的措施")
    design_suggestion = models.TextField("设计建议")
    safety_suggestion = models.TextField("安全性建议")
    
    def __str__(self):
        return (self.title)
    

    class Meta:
        ordering = ('title','death_toll')
        verbose_name = '事故事件'
        verbose_name_plural = verbose_name