import os
from django.db import models
from users.models import *
from django.urls import reverse
from django.utils.html import format_html
from django.utils import timezone


class Passports(models.Model):
    user = models.ForeignKey(User, verbose_name = u"Район", on_delete = models.CASCADE)

    nameProject = models.CharField(verbose_name = u"Наименование проекта", max_length = 250, db_index = True)
    indicators = models.TextField(verbose_name = u"Количественные показатели (показатель) результатов проекта по объектам и мероприятиям, включенным в проект")
    address = models.TextField(verbose_name = u"Адрес или описание местоположения")
    borderArea = models.BooleanField(verbose_name = u"Приграничная территория (да/нет)", default = False)
    OKTMO = models.CharField(verbose_name = u"ОКТМО населенного (-ых) пункта (-ов)", max_length = 250)
    improvedArea = models.DecimalField(verbose_name = u"Благоустраиваемая площадь, на которой реализуется проект, кв.м", max_digits = 20, decimal_places = 2, blank = True, null = True)
    populationLocality = models.PositiveBigIntegerField(verbose_name = u"Численность населения на 1 января года подачи заявки в населенном (-ых) пункте (-ах), в котором реализуется проект, чел.", blank = True, null = True)
    countMonth = models.PositiveIntegerField(verbose_name = u"Продолжительность реализации проекта,  количество месяцев (до 31 декабря года, в котором получена субсидия)", blank = True, null = True)
    dateStartPlane = models.DateField(verbose_name = u"Планируемая дата начала реализации проекта", blank = True, null = True)
    dateEndPlane = models.DateField(verbose_name = u"Планируемая дата окончания реализации проекта", blank = True, null = True)
    initiativeGroup = models.TextField(verbose_name = u"Описание состава инициативной группы", blank = True, null = True)
    generalCost = models.DecimalField(verbose_name = u"Общие расходы по проекту, рублей:", max_digits = 15, decimal_places = 2)
    stateSupport = models.DecimalField(verbose_name = u"За счет средств государственной поддержки (федерального бюджета и бюджета Забайкальского края)", max_digits = 15, decimal_places = 3, blank = True, null = True)
    localBudget = models.DecimalField(verbose_name = u"За счет средств местного бюджета", max_digits = 15, decimal_places = 3, blank = True, null = True)
    offBudget = models.DecimalField(verbose_name = u"За счет средств внебюджетных источников (вклад граждан, юридических лиц, индивидуальных предпринимателей, общественных организаций)", max_digits = 15, decimal_places = 2, blank = True, null = True)
    citizen = models.DecimalField(verbose_name = u"Вклад граждан, рублей", max_digits = 15, decimal_places = 2, blank = True, null = True)
    citizenMoney = models.DecimalField(verbose_name = u"денежными средствами", max_digits = 15, decimal_places = 3, blank = True, null = True)
    citizenWork = models.DecimalField(verbose_name = u"трудовым участием", max_digits = 15, decimal_places = 3, blank = True, null = True)
    citizenRooms = models.DecimalField(verbose_name = u"предоставлением помещений", max_digits = 15, decimal_places = 3, blank = True, null = True)
    citizenTechnical = models.DecimalField(verbose_name = u"предоставлением технических средств", max_digits = 15, decimal_places = 3, blank = True, null = True)
    publicOrg = models.DecimalField(verbose_name = u"Вклад общественных, включая волонтерские, организаций, рублей", max_digits = 15, decimal_places = 2, blank = True, null = True)
    publicOrgMoney = models.DecimalField(verbose_name = u"денежными средствами", max_digits = 15, decimal_places = 3, blank = True, null = True)
    publicOrgWork = models.DecimalField(verbose_name = u"трудовым участием", max_digits = 15, decimal_places = 3, blank = True, null = True)
    publicOrgRooms = models.DecimalField(verbose_name = u"предоставлением помещений", max_digits = 15, decimal_places = 3, blank = True, null = True)
    publicOrgTechnical = models.DecimalField(verbose_name = u"предоставлением технических средств", max_digits = 15, decimal_places = 3, blank = True, null = True)
    legalEntities = models.DecimalField(verbose_name = u"Вклад юридических лиц (индивидуальных предпринимателей), рублей", max_digits = 15, decimal_places = 2, blank = True, null = True)
    legalEntitiesMoney = models.DecimalField(verbose_name = u"денежными средствами", max_digits = 15, decimal_places = 3, blank = True, null = True)
    legalEntitiesWork = models.DecimalField(verbose_name = u"трудовым участием", max_digits = 15, decimal_places = 3, blank = True, null = True)
    legalEntitiesRooms = models.DecimalField(verbose_name = u"предоставлением помещений", max_digits = 15, decimal_places = 3, blank = True, null = True)
    legalEntitiesTechnical = models.DecimalField(verbose_name = u"предоставлением технических средств", max_digits = 15, decimal_places = 3, blank = True, null = True)
    created = models.DateTimeField(verbose_name = u"Создано", auto_now_add = True)
    file = models.FileField(upload_to = '', blank = True, null = True)

    class Meta:
        ordering = ('created', )
        indexes = [models.Index(fields = ['id'])]
        verbose_name = 'Паспорт проекта'
        verbose_name_plural = 'Паспорта проектов'

    def __str__(self):
        return self.nameProject
    
    def get_absolute_url(self):
        return reverse('passport', kwargs = { 'id': self.id })
    
    def get_points(self):
        points = 0
        result_1 = 0
        result_2 = 0

        if self.generalCost != 0:
            result_1 = (self.citizen / self.generalCost) * 100
            result_2 = ((self.legalEntities + self.publicOrg) / self.generalCost) * 100

        if self.borderArea:
            points += 10

        if result_1 > 0 and result_1 <= 5:
            points += 10
        elif result_1 > 5 and result_1 <= 15:
            points += 15
        elif result_1 > 15 and result_1 <= 30:
            points += 20 
        elif result_1 > 30:
            points += 25

        if result_2 > 0 and result_2 <= 5:
            points += 10
        elif result_2 > 5 and result_2 <= 10:
            points += 15
        elif result_2 > 10 and result_2 <= 30:
            points += 20 
        elif result_2 > 30:
            points += 25
            
        return points
    
    def get_user(self):
        if self.user.region:
            return self.user.region.nameRegion
        else:
            return self.user.username
    get_user.short_description = u'Район'
    
    def get_total_points(self):
        return self.get_points() + self.groups.get_points() + self.desc.get_points()
    get_total_points.short_description = 'Баллы'
    get_total_points.admin_order_field = 'nameProject'
    
    def file_link(self):
        if not self.file or not os.path.exists('media/passports/Passport №' + str(self.id) + '.xlsx'):
            return 'Файл не существует'
        else:
            return format_html("<a href='%s'>Скачать</a>" % (self.file.url,))
    file_link.short_description = 'Скачать паспорт проекта'
    

class LaborPart(models.Model):
    passport = models.ForeignKey(Passports, on_delete = models.CASCADE)

    works = models.TextField(verbose_name = u'Описание работ')
    countManHour = models.DecimalField(verbose_name = u'Трудовые затраты, количество человеко-часов', 
                                       max_digits = 10, decimal_places = 2, blank = True, null = True)
    costManHour = models.DecimalField(verbose_name = u'Стоимость одного человека-часа, рублей', 
                                      max_digits = 15, decimal_places = 3, blank = True, null = True)
    laborCost = models.DecimalField(verbose_name = u'Стоимость трудовых затрат, рублей', 
                                    max_digits = 15, decimal_places = 3, blank = True, null = True)

    class Meta:
        verbose_name = 'Расчет трудового участия граждан'
        verbose_name_plural = 'Расчет трудового участия граждан'

    def __str__(self):
        return 'Паспорт проекта №' + str( self.passport.id)
    

class TargetGroup(models.Model):
    passport = models.OneToOneField(Passports, related_name = 'groups', on_delete = models.CASCADE)

    populationVoted = models.PositiveIntegerField(verbose_name = u'Численность населения, проголосовавших за проект, чел.', 
                                                  blank = True, null = True)
    populationPart = models.PositiveIntegerField(verbose_name = u'Численность населения, подтвердившего участие в реализации проекта, чел.', 
                                                 blank = True, null = True)
    younger = models.PositiveIntegerField(verbose_name = u'от 0-18 лет', blank = True, null = True)
    adult = models.PositiveIntegerField(verbose_name = u'от 18-35 лет', blank = True, null = True)
    older = models.PositiveIntegerField(verbose_name = u'старше 36 лет', blank = True, null = True)
    countBenefit = models.PositiveIntegerField(verbose_name = u'Количество выгодоприобретателей (жителей, которые получат пользу от проекта, пользователей объектами, созданными (обустроенными) в рамках проекта), чел.', 
                                               blank = True, null = True)

    class Meta:
        verbose_name = 'Целевая группа'
        verbose_name_plural = 'Целевая группа'

    def __str__(self):
        return 'Паспорт проекта №' + str( self.passport.id)
    
    def get_points(self):
        points = 0
        result_1 = 0

        if self.passport.populationLocality != 0:
            result_1 = (self.populationPart / self.passport.populationLocality) * 100

        if result_1 > 0 and result_1 <= 10 and self.passport.populationLocality <= 1000:
            points = 10
        elif result_1 > 0 and result_1 <= 5 and 1000 <= self.passport.populationLocality <= 5000:
            points = 10
        elif result_1 > 0 and result_1 <= 3 and self.passport.populationLocality > 5000:
            points = 10
        elif result_1 > 10 and result_1 <= 15 and self.passport.populationLocality <= 1000:
            points = 15
        elif result_1 > 5 and result_1 <= 8 and 1000 <= self.passport.populationLocality <= 5000:
            points = 15
        elif result_1 > 3 and result_1 <= 5 and self.passport.populationLocality > 5000:
            points = 15
        elif result_1 > 15 and result_1 <= 20 and self.passport.populationLocality <= 1000:
            points = 20
        elif result_1 > 8 and result_1 <= 10 and 1000 <= self.passport.populationLocality <= 5000:
            points = 20
        elif result_1 > 5 and result_1 <= 7 and self.passport.populationLocality > 5000:
            points = 20
        elif result_1 > 20 and self.passport.populationLocality <= 1000:
            points = 25
        elif result_1 > 10 and 1000 <= self.passport.populationLocality <= 5000:
            points = 25
        elif result_1 > 7 and self.passport.populationLocality > 5000:
            points = 25

        result_2 = (self.countBenefit / self.passport.populationLocality) * 100
        if result_2 > 0 and result_2 <= 30:
            points += 10
        elif result_2 > 30 and result_2 <= 60:
            points += 15
        elif result_2 > 60:
            points += 20

        return points
    

class ProjectDesc(models.Model):
    passport = models.OneToOneField(Passports, related_name = 'desc', on_delete = models.CASCADE)

    targetProject = models.CharField(verbose_name = u'Цель проекта', max_length = 250)
    tasksProject = models.TextField(verbose_name = u'Задачи проекта', blank = True, null = True)
    events = models.TextField(verbose_name = u'Описание мероприятий предпроектного исследования (в случае его проведения)', blank = True, null = True)
    troubles = models.TextField(verbose_name = u'Описание проблемы, на решение которой направлен проект, с приложением эскизного проекта размещения элементов благоустройства, карты-схемы расположения объектов благоустройства в населенном пункте',
                                blank = True, null = True)
    stateMainEvents = models.BooleanField(verbose_name = u'Участие в мероприятиях государственной программы Российской Федерации «Комплексное развитие сельских территорий», утвержденной постановлением Правительства Российской Федерации от 31 мая 2019 г. № 696, в течении 3 лет, предшествующих году предоставления субсидии на реализацию проекта', default = False)
    nameStateMainEvents = models.TextField(verbose_name = u'Если да, описываются реализованные мероприятия на территории реализации проекта',
                                           blank = True, null = True)
    stateEvents = models.BooleanField(verbose_name = u'Участие в мероприятиях других государственных программ Российской Федерации, Забайкальского края, муниципальных программ и проектах, в течении 3 лет, предшествующих году предоставления субсидии на реализацию проекта', default = False)
    nameStateEvents = models.TextField(verbose_name = u'Если да, описываются реализованные мероприятия на территории реализации проекта',
                                       blank = True, null = True)
    security = models.TextField(verbose_name = u'Соответствие нормам безопасности и законодательству Российской Федерации, включая ссылки на соответствующие нормативы (в случае использования типовой проектной документации дается информация о ее источнике)',
                                blank = True, null = True)
    justification = models.TextField(verbose_name = u'Качество и обоснованность архитектурных и планировочных решений', 
                                     blank = True, null = True)
    forms = models.CharField(verbose_name = u'Формы проведения процедур по выбору подрядчика либо закупок', max_length = 250, blank = True, null = True)
    supportEvents = models.TextField(verbose_name = u'Мероприятия по поддержанию и/или развитию полученных в рамках проекта результатов', 
                                     blank = True, null = True)
    mechanisms = models.TextField(verbose_name = u'Механизмы содержания и эксплуатации объектов по благоустройству',
                                  blank = True, null = True)

    class Meta:
        verbose_name = 'Описание проекта'
        verbose_name_plural = 'Описание проекта'

    def __str__(self):
        return 'Паспорт проекта №' + str( self.passport.id)
    
    def get_points(self):
        points = 0

        if self.stateMainEvents:
            points += 5
        if self.stateEvents:
            points += 5

        return points
    

class TypeEvents(models.Model):
    typeEvent = models.CharField(verbose_name = 'Тип мероприятия', max_length = 250)

    class Meta:
        verbose_name = 'Тип мероприятия'
        verbose_name_plural = 'Типы мероприятий'

    def __str__(self):
        return self.typeEvent
    

class PlaneEvents(models.Model):
    passport = models.ForeignKey(Passports, on_delete = models.CASCADE)
    typeEvent = models.ForeignKey(TypeEvents, verbose_name = 'Тип мероприятия', on_delete = models.CASCADE)

    nameEvent = models.CharField(verbose_name = u'Наименование мероприятия ', max_length = 250)
    dedlineStart = models.DateField(verbose_name = u'Сроки реализации (начало)', blank = True, null = True)
    dedlineEnd = models.DateField(verbose_name = u'Сроки реализации (конец)', blank = True, null = True)
    performer = models.CharField(verbose_name = u'Ответственный исполнитель', max_length = 250, blank = True, null = True)

    class Meta:
        verbose_name = 'План реализации мероприятий проекта'
        verbose_name_plural = 'План реализации мероприятий проекта'

    def __str__(self):
        return 'Паспорт проекта №' + str( self.passport.id)


class CostEstimate(models.Model):
    passport = models.ForeignKey(Passports, on_delete = models.CASCADE)

    expenseItem = models.CharField(verbose_name = 'Статьи расходов', max_length = 250)
    generalExpenses = models.DecimalField(verbose_name = 'Общие расходы по проекту', 
                                          max_digits = 15, decimal_places = 3, blank = True, null = True)
    stateExpenses = models.DecimalField(verbose_name = 'Запрашиваемые средства государственной поддержки',
                                        max_digits = 15, decimal_places = 3, blank = True, null = True)
    districtBudget = models.DecimalField(verbose_name = 'Бюджет муниципального района (муниципального или городского округа)', 
                                         max_digits = 15, decimal_places = 3, blank = True, null = True)
    settlementBudget = models.DecimalField(verbose_name = 'Бюджет сельского (городского) поселения', 
                                           max_digits = 15, decimal_places = 3, blank = True, null = True)
    offBudgetExpenses = models.DecimalField(verbose_name = 'Внебюджетные источники', 
                                            max_digits = 15, decimal_places = 3, blank = True, null = True)

    class Meta:
        verbose_name = 'Смета расходов по проекту'
        verbose_name_plural = 'Смета расходов по проекту'

    def __str__(self):
        return 'Паспорт проекта №' + str( self.passport.id)
    

class TotalResults(models.Model):
    passport = models.OneToOneField(Passports, on_delete = models.CASCADE)

    totalLaborCost = models.DecimalField(max_digits = 15, decimal_places = 3, default = 0, blank = True, null = True)
    totalGeneralExpenses = models.DecimalField(max_digits = 15, decimal_places = 3, default = 0, blank = True, null = True)
    totalStateExpenses = models.DecimalField(max_digits = 15, decimal_places = 3, default = 0, blank = True, null = True)
    totalDistrictBudget = models.DecimalField(max_digits = 15, decimal_places = 3, default = 0, blank = True, null = True)
    totalSettlementBudget = models.DecimalField(max_digits = 15, decimal_places = 3, default = 0, blank = True, null = True)
    totalOffBudgetExpenses = models.DecimalField(max_digits = 15, decimal_places = 3, default = 0, blank = True, null = True)

    class Meta:
        verbose_name = 'Итоговые вычисления'
        verbose_name_plural = 'Итоговые вычисления'

    def __str__(self):
        return 'Паспорт проекта №' + str( self.passport.id)
    

class ProjectRegister(models.Model):
    passport = models.OneToOneField(Passports, on_delete = models.CASCADE, verbose_name = u'Наименование проекта')

    date = models.DateField(verbose_name = u'Дата', default = timezone.now)
    state = models.DecimalField(verbose_name=u"ФБ", max_digits = 15, decimal_places = 3, blank = True, null = True)
    region = models.DecimalField(verbose_name=u"КБ", max_digits = 15, decimal_places = 3, blank = True, null = True)
    local = models.DecimalField(verbose_name=u"МБ", max_digits = 15, decimal_places = 3, blank = True, null = True)
    off = models.DecimalField(verbose_name=u"ВБ", max_digits = 15, decimal_places = 3, blank = True, null = True)

    class Meta:
        verbose_name = 'Реестр проектов'
        verbose_name_plural = 'Реестр проектов'

    def __str__(self):
        return 'Реестр проектов'

    def get_subsidy(self):
        return self.state + self.region
    get_subsidy.short_description = 'Субсидия, рублей'
    get_subsidy.admin_order_field = 'passport'
    
    def get_general_cost(self):
        return self.state + self.region + self.local + self.off
    get_general_cost.short_description = 'Общая стоимость проекта, рублей'
    get_general_cost.admin_order_field = 'passport'