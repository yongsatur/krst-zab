from .forms import *
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import FileResponse
import os.path
import xlsxwriter


@login_required(login_url = 'authorization')
def index(request):
    user = request.user
    passports = Passports.objects.filter(user = user)
    return render(request, 'index.html', { 'passports': passports })


@login_required(login_url = 'authorization')
def passport(request, id):
    passport = get_object_or_404(Passports, id = id)

    if not passport.file or not os.path.exists(passport.file.url):
        excel(request, passport.id)

    laborPart = LaborPart.objects.filter(passport = passport)
    targetGroup = TargetGroup.objects.filter(passport = passport)
    projectDesc = ProjectDesc.objects.filter(passport = passport)
    planeEvents = PlaneEvents.objects.filter(passport = passport)
    costEstimate = CostEstimate.objects.filter(passport = passport)
    totalResults = TotalResults.objects.filter(passport = passport)
    return render(request, 'passport.html', { 
        'passport': passport, 'laborPart': laborPart, 'targetGroup': targetGroup,
        'projectDesc': projectDesc, 'planeEvents': planeEvents, 
        'costEstimate': costEstimate, 'totalResults': totalResults
    })


@login_required(login_url = 'authorization')
def passport_add_first(request):
    user = request.user

    if request.method == 'POST':
        form = PassportForm(request.POST)
        if form.is_valid():
            passport = form.save(commit = False)
            passport.user = user
            passport.file = 'passports/Passport №' + str(passport.id) + '.xlsx'
            passport.save()
            return redirect('passport_add_second', passport.id)
        else:
            messages.success(request, ('Возникла ошибка! Пожалуйста, повторите позже.'))
            return redirect('passport_add_first')
    else:
        form = PassportForm()
        return render(request, 'passport_add.html', { 'form': form })
    

@login_required(login_url = 'authorization')
def passport_add_second(request, id):
    passport = get_object_or_404(Passports, id = id)
    totalResults, created = TotalResults.objects.get_or_create(passport = passport)
    laborPart_all = LaborPart.objects.filter(passport = passport)

    if request.method == 'POST':
        form = LaborPartForm(request.POST)
        if form.is_valid():
            laborPart = form.save(commit = False)
            laborPart.passport = passport
            laborPart.save()

            totalResults.totalLaborCost += laborPart.laborCost 
            totalResults.save()

            return render(request, 'passport_add.html', { 
                'form': form, 'passport': passport, 'laborPart': laborPart_all, 
                'totalResults': totalResults, 'tab_id': 2 
            })
        else:
            messages.success(request, ('Возникла ошибка! Пожалуйста, повторите позже.'))
            return redirect('passport_add_second', passport.id)
    else:
        form = PassportForm()
        return render(request, 'passport_add.html', { 'form': form, 'passport': passport, 'tab_id': 2 })
    

@login_required(login_url = 'authorization')
def passport_add_third(request, id):
    passport = get_object_or_404(Passports, id = id)

    if request.method == 'POST':
        form = TargetGroupForm(request.POST)
        if form.is_valid():
            targetGroup = form.save(commit = False)
            targetGroup.passport = passport
            targetGroup.save()
            return redirect('passport_add_forth', passport.id)
        else:
            messages.success(request, ('Возникла ошибка! Пожалуйста, повторите позже.'))
            return redirect('passport_add_third', passport.id)
    else:
        form = PassportForm()
        return render(request, 'passport_add.html', { 'form': form, 'passport': passport, 'tab_id': 3 })
    

@login_required(login_url = 'authorization')
def passport_add_forth(request, id):
    passport = get_object_or_404(Passports, id = id)
    typeEvents = TypeEvents.objects.all()

    if request.method == 'POST':
        form = ProjectDescForm(request.POST)
        if form.is_valid():
            projectDesc = form.save(commit = False)
            projectDesc.passport = passport
            projectDesc.save()
            return redirect('passport_add_fifth', passport.id)
        else:
            messages.success(request, ('Возникла ошибка! Пожалуйста, повторите позже.'))
            return redirect('passport_add_forth', passport.id)
    else:
        form = PassportForm()
        return render(request, 'passport_add.html', { 'form': form, 'passport': passport, 'tab_id': 4 })
    

@login_required(login_url = 'authorization')
def passport_add_fifth(request, id):
    passport = get_object_or_404(Passports, id = id)
    typeEvents = TypeEvents.objects.all()
    planeEvents_all = PlaneEvents.objects.filter(passport = passport)

    if request.method == 'POST':
        form = PlaneEventsForm(request.POST)
        if form.is_valid():
            planeEvents = form.save(commit = False)
            planeEvents.passport = passport

            planeEvents.save()
            return render(request, 'passport_add.html', { 
                'form': form, 'typeEvents': typeEvents, 'passport': passport, 
                'planeEvents': planeEvents_all, 'tab_id': 5 
            })
        else:
            messages.success(request, ('Возникла ошибка! Пожалуйста, повторите позже.'))
            return redirect('passport_add_fifth', passport.id)
    else:
        form = PassportForm()
        return render(request, 'passport_add.html', { 'form': form, 'typeEvents': typeEvents, 'passport': passport, 'tab_id': 5 })
    

@login_required(login_url = 'authorization')
def passport_add_sixth(request, id):
    passport = get_object_or_404(Passports, id = id)
    totalResults, created = TotalResults.objects.get_or_create(passport = passport)
    costEstimate_all = CostEstimate.objects.filter(passport = passport)

    if request.method == 'POST':
        form = CostEstimateForm(request.POST)
        if form.is_valid():
            costEstimate = form.save(commit = False)
            costEstimate.passport = passport
            costEstimate.save()

            totalResults.totalGeneralExpenses += costEstimate.generalExpenses
            totalResults.totalStateExpenses += costEstimate.stateExpenses
            totalResults.totalDistrictBudget += costEstimate.districtBudget
            totalResults.totalSettlementBudget += costEstimate.settlementBudget
            totalResults.totalOffBudgetExpenses += costEstimate.offBudgetExpenses
            totalResults.save()

            return render(request, 'passport_add.html', { 
                'form': form, 'passport': passport, 'tab_id': 6,
                'costEstimate': costEstimate_all, 'totalResults': totalResults
            })
        else:
            messages.success(request, ('Возникла ошибка! Пожалуйста, повторите позже.'))
            return redirect('passport_add_sixth', passport.id)
    else:
        form = PassportForm()
        return render(request, 'passport_add.html', { 'form': form, 'passport': passport, 'tab_id': 6 })
    

@login_required(login_url = 'authorization')
def excel(request, id):
    passport = get_object_or_404(Passports, id = id)

    laborPart = LaborPart.objects.filter(passport = passport)
    targetGroup = TargetGroup.objects.filter(passport = passport)
    projectDesc = ProjectDesc.objects.filter(passport = passport)
    planeEvents = PlaneEvents.objects.filter(passport = passport)
    costEstimate = CostEstimate.objects.filter(passport = passport)
    totalResults = TotalResults.objects.filter(passport = passport)

    workbook = xlsxwriter.Workbook('media/passports/Passport №' + str(passport.id) + '.xlsx')

    header = workbook.add_format({
        'bold': True, 'align': 'center', 'valign': 'vcenter', 
        'font_size': 14, 'font_name': 'Times New Roman'
    })
    header_sheet = workbook.add_format({
        'bold': True, 'align': 'center', 'valign': 'vcenter', 
        'border': 1, 'bg_color': '#D0F0C0', 'font_name': 'Times New Roman'
    })
    center = workbook.add_format({
        'align': 'center', 'valign': 'vcenter', 'font_name': 'Times New Roman'
    })
    bold = workbook.add_format({ 
        'bold': True, 'border': 1, 'font_size': 12, 
        'valign': 'vcenter', 'font_name': 'Times New Roman'
    })
    bold.set_text_wrap()
    border = workbook.add_format({ 
        'border': 1, 'font_size': 12, 'valign': 'vcenter', 
        'font_name': 'Times New Roman' 
    })
    border.set_text_wrap()
    border_center = workbook.add_format({ 
        'border': 1, 'font_size': 12, 'font_name': 'Times New Roman',
        'valign': 'vcenter', 'align': 'center' 
    })
    border_center.set_text_wrap()
    result = workbook.add_format({ 
        'border': 1, 'bg_color': '#d3e6fa', 'bold': True, 'font_size': 12, 
        'valign': 'vcenter', 'font_name': 'Times New Roman' })
    wrap_text = workbook.add_format({ 'font_name': 'Times New Roman' })
    wrap_text.set_text_wrap()
    sign = workbook.add_format({ 'font_name': 'Times New Roman', 'font_size': 12, 'valign': 'vcenter' })
    date_format = workbook.add_format({
        'num_format': 'd mmmm yyyy', 'border': 1, 'font_name': 'Times New Roman', 
        'font_size': 12, 'valign': 'vcenter', 'align': 'center'
    })
    
    worksheet_1 = workbook.add_worksheet('Общая характеристика')

    worksheet_1.set_column(0, 1, 70)

    worksheet_1.set_row(0, 50)
    worksheet_1.set_row(1, 30)
    worksheet_1.set_row(2, 20)
    worksheet_1.set_row(3, 25)
    worksheet_1.set_row(4, 70)
    worksheet_1.set_row(5, 50)
    worksheet_1.set_row(7, 35)
    worksheet_1.set_row(9, 35)
    worksheet_1.set_row(11, 50)
    worksheet_1.set_row(12, 35)
    worksheet_1.set_row(17, 35)
    worksheet_1.set_row(19, 35)
    worksheet_1.set_row(31, 35)
    worksheet_1.set_row(36, 235)
    worksheet_1.set_default_row(22)
    
    worksheet_1.merge_range("A1:B1", "Паспорт\n проекта по благоустройству общественных пространств на сельских территориях", header)
    worksheet_1.merge_range("A2:B2", "в 2025 году", center)
    worksheet_1.merge_range("A4:B4", "I. Общая характеристика", header_sheet)

    worksheet_1.write('A5', 'Наименование проекта', border)
    worksheet_1.write('B5', passport.nameProject, border)
    worksheet_1.write('A6', 'Количественные показатели (показатель) результатов проекта по объектам и мероприятиям, включенным в проект¹', border)
    worksheet_1.write('B6', passport.indicators, border)
    worksheet_1.write('A7', 'Приграничная территория (да/нет)', border)
    if passport.borderArea:
        worksheet_1.write('B7', 'Да', border_center)
    else:
        worksheet_1.write('B7', 'Нет', border_center)
    worksheet_1.write('A8', 'Адрес или описание местоположения', border)
    worksheet_1.write('B8', passport.address, border)
    worksheet_1.write('A9', 'ОКТМО населенного (-ых) пункта (-ов)', border)
    worksheet_1.write('B9', passport.OKTMO, border)
    worksheet_1.write('A10', 'Численность населения на 1 января года подачи заявки в населенном (-ых) пункте (-ах), в котором реализуется проект, чел.²', border)
    worksheet_1.write('B10', passport.populationLocality, border)
    worksheet_1.write('A11', 'Благоустраиваемая площадь, на которой реализуется проект, кв.м', border)
    worksheet_1.write('B11', passport.improvedArea, border)
    worksheet_1.write('A12', 'Описание состава инициативной группы³', border)
    worksheet_1.write('B12', passport.initiativeGroup, border)
    worksheet_1.write('A13', 'Продолжительность реализации проекта, количество месяцев (до 31 декабря года, в котором получена субсидия)', border)
    worksheet_1.write('B13', passport.countMonth, border)
    worksheet_1.write('A14', 'Планируемая дата начала реализации проекта', border)
    worksheet_1.write_datetime('B14', passport.dateStartPlane, date_format)
    worksheet_1.write('A15', 'Планируемая дата окончания реализации проекта', border)
    worksheet_1.write_datetime('B15', passport.dateEndPlane, date_format)
    worksheet_1.write('A16', 'Общие расходы по проекту, рублей:', bold)
    worksheet_1.write('B16', passport.generalCost, result)
    worksheet_1.write('A17', 'в том числе за счет средств:', border)
    worksheet_1.write('B17', '', border)
    worksheet_1.write('A18', 'государственной поддержки (федерального бюджета и бюджета Забайкальского края)⁴', border)
    worksheet_1.write('B18', passport.stateSupport, border)
    worksheet_1.write('A19', 'местного бюджета⁵', border)
    worksheet_1.write('B19', passport.localBudget, border)
    worksheet_1.write('A20', 'внебюджетных источников (вклад граждан, юридических лиц, индивидуальных предпринимателей, общественных организаций)⁶', border)
    worksheet_1.write('B20', passport.offBudget, result)
    worksheet_1.write('A21', 'из них:', border)
    worksheet_1.write('B21', '', border)
    worksheet_1.write('A22', 'вклад граждан, рублей:', bold)
    worksheet_1.write('B22', passport.citizen, result)
    worksheet_1.write('A23', 'денежными средствами', border)
    worksheet_1.write('B23', passport.citizenMoney, border)
    worksheet_1.write('A24', 'трудовым участием', border)
    worksheet_1.write('B24', passport.citizenWork, border)
    worksheet_1.write('A25', 'предоставлением помещений', border)
    worksheet_1.write('B25', passport.citizenRooms, border)
    worksheet_1.write('A26', 'предоставлением технических средств', border)
    worksheet_1.write('B26', passport.citizenTechnical, border)
    worksheet_1.write('A27', 'вклад общественных, включая волонтерские, организаций, рублей', bold)
    worksheet_1.write('B27', passport.publicOrg, result)
    worksheet_1.write('A28', 'денежными средствами', border)
    worksheet_1.write('B28', passport.publicOrgMoney, border)
    worksheet_1.write('A29', 'трудовым участием', border)
    worksheet_1.write('B29', passport.publicOrgWork, border)
    worksheet_1.write('A30', 'предоставлением помещений', border)
    worksheet_1.write('B30', passport.publicOrgRooms, border)
    worksheet_1.write('A31', 'предоставлением технических средств', border)
    worksheet_1.write('B31', passport.publicOrgTechnical, border)
    worksheet_1.write('A32', 'вклад юридических лиц (индивидуальных предпринимателей), рублей', bold)
    worksheet_1.write('B32', passport.legalEntities, result)
    worksheet_1.write('A33', 'денежными средствами', border)
    worksheet_1.write('B33', passport.legalEntitiesMoney, border)
    worksheet_1.write('A34', 'трудовым участием', border)
    worksheet_1.write('B34', passport.legalEntitiesWork, border)
    worksheet_1.write('A35', 'предоставлением помещений', border)
    worksheet_1.write('B35', passport.legalEntitiesRooms, border)
    worksheet_1.write('A36', 'предоставлением технических средств', border)
    worksheet_1.write('B36', passport.legalEntitiesTechnical, border)
    worksheet_1.merge_range('A37:B37', 'Примечание: \n¹Указывается краткое наименование: детская площадка, спортивная площадка, зона отдыха, \
площадка для лиц с ограниченными возможностями здоровья, освещение территории, подсветка зданий, пешеходный тротуар, \
велосипедная дорожка, автомобильная парковка, велосипедная парковка, ремонт дороги, ограждение, оформление фасада, \
ливневый сток, колодец, колонка, площадка накопления твердых коммунальных отходов, природный ландшафт, водоем, \
памятник.\
\n²Указывается на основании официальной статистической информации. \
\n³а) население муниципального образования, представители органанов территориального общественного самоуправления, \
общественных организаций и объединений; б) хозяйствующие субъекты, осуществляющие деятельность на территории \
соответствующего муниципального образования; в) бюджетные учреждения, в том числе в сфере образования, \
здравоохранения, культуры, социальной защиты, физической культуры и спорта, общественные организации и иные \
некоммерческие организации.\
\n⁴Сумма средств федерального бюджета и бюджета Забайкальского края не превышает 3 млн. \
рублей и составляет не более 70% общего объема финансового обеспечения реализации проекта.\
\n⁵Сумма средств бюджетов муниципального района (муниципального или городского округа) и сельского (городского) \
поселения составляет не менее 3% от объема привлекаемых на реализацию проекта средств без учета запрашиваемых \
средств государственной поддержки. При этом, уровень софинансирования Забайкальским краем объема расходного \
обязательства  района (муниципального или городского округа) составляет не более 99%. \
\n⁶Сумма средств внебюджетных источников составляет разницу от общего объема финансового обеспечения реализации \
проекта суммы средств государственной поддержки и местных бюджетов.', wrap_text)

    worksheet_2 = workbook.add_worksheet('Расчет трудового участия')

    worksheet_2.set_column(0, 0, 50)
    worksheet_2.set_column(1, 3, 25)
    worksheet_2.set_row(0, 25)
    worksheet_2.set_row(1, 70)
    worksheet_2.set_default_row(35)

    worksheet_2.merge_range("A1:D1", "II. Расчет трудового участия граждан", header_sheet)

    worksheet_2.write('A2', 'Описание работ', border_center)
    worksheet_2.write('B2', 'Трудовые затраты, количество человеко-часов', border_center)
    worksheet_2.write('C2', 'Стоимость одного человека-часа, рублей', border_center)
    worksheet_2.write('D2', 'Стоимость трудовых затрат, рублей', border_center)

    row = 2

    for item in laborPart:
        worksheet_2.write(row, 0, item.works, border)
        worksheet_2.write(row, 1, item.countManHour, border)
        worksheet_2.write(row, 2, item.countManHour, border)
        worksheet_2.write(row, 3, item.laborCost, border)
        row += 1

    worksheet_2.write(row, 0, 'Всего:', bold)

    for item in totalResults:
        worksheet_2.write(row, 1, '', border)
        worksheet_2.write(row, 2, '', border)
        worksheet_2.write(row, 3, item.totalLaborCost, result)

    worksheet_3 = workbook.add_worksheet('Целевая группа')

    worksheet_3.set_column(0, 0, 60)
    worksheet_3.set_column(1, 1, 40)
    worksheet_3.set_row(0, 25)
    worksheet_3.set_row(2, 35)
    worksheet_3.set_row(3, 50)
    worksheet_3.set_row(8, 50)
    worksheet_3.set_default_row(22)

    worksheet_3.merge_range("A1:B1", "III. Целевая группа", header_sheet)

    for item in targetGroup:
        worksheet_3.write('A2', 'Численность населения, проголосовавших за проект, чел.', border)
        worksheet_3.write('B2', item.populationVoted, border)
        worksheet_3.write('A3', 'Численность населения, подтвердившего участие в реализации проекта, чел.', border)
        worksheet_3.write('B3', item.populationPart, border)
        worksheet_3.write('A4', 'Количество выгодоприобретателей (жителей, которые получат пользу от проекта, пользователей объектами, созданными (обустроенными) в рамках проекта), чел.', border)
        worksheet_3.write('B4', item.countBenefit, result)
        worksheet_3.write('A5', 'в том числе:¹', border)
        worksheet_3.write('B5', '', border)
        worksheet_3.write('A6', 'от 0 до 18 лет', border)
        worksheet_3.write('B6', item.younger, border)
        worksheet_3.write('A7', 'от 18 до 35 лет', border)
        worksheet_3.write('B7', item.adult, border)
        worksheet_3.write('A8', 'старше 35 лет', border)
        worksheet_3.write('B8', item.older, border)

    worksheet_3.merge_range("A9:B9", 'Примечание: \n¹Молодежь до 35 лет, граждане с ограниченными возможностями \
здоровья, дети в возрасте от ___ до____ лет и др.', wrap_text)

    worksheet_4 = workbook.add_worksheet('Описание проекта')

    worksheet_4.set_column(0, 1, 70)
    worksheet_4.set_row(0, 25)
    worksheet_4.set_row(2, 60)
    worksheet_4.set_row(3, 50)
    worksheet_4.set_row(4, 300)
    worksheet_4.set_row(6, 70)
    worksheet_4.set_row(8, 70)
    worksheet_4.set_row(9, 70)
    worksheet_4.set_row(10, 40)
    worksheet_4.set_row(12, 100)
    worksheet_4.set_row(13, 50)
    worksheet_4.set_row(14, 250)
    worksheet_4.set_default_row(22)

    worksheet_4.merge_range("A1:B1", "IV. Описание проекта", header_sheet)

    for item in projectDesc:
        worksheet_4.write('A2', 'Цель проекта', border)
        worksheet_4.write('B2', item.targetProject, border)
        worksheet_4.write('A3', 'Задачи проекта', border)
        worksheet_4.write('B3', item.tasksProject, border)
        worksheet_4.write('A4', 'Описание мероприятий предпроектного исследования (в случае его проведения)¹', border)
        worksheet_4.write('B4', item.events, border)
        worksheet_4.write('A5', 'Описание проблемы, на решение которой направлен проект, с приложением эскизного проекта \
размещения элементов благоустройства, карты-схемы расположения объектов благоустройства в населенном пункте', border)
        worksheet_4.write('B5', item.troubles, border)
        worksheet_4.merge_range("A6:A7", 'Участие в мероприятиях государственной программы Российской Федерации «Комплексное\
развитие сельских территорий», утвержденной постановлением Правительства Российской Федерации \
от 31 мая 2019 г. № 696, в течении 3 лет, предшествующих году предоставления субсидии на \
реализацию проекта', border)
        if item.stateMainEvents:
            worksheet_4.write('B6', 'Да', border_center)
        else:
            worksheet_4.write('B6', 'Нет', border_center)
        worksheet_4.write('B7', item.nameStateMainEvents, border)
        worksheet_4.merge_range("A8:A9", 'Участие в мероприятиях других государственных программ Российской Федерации, \
Забайкальского края, муниципальных программ и проектах, в течении 3 лет, предшествующих \
году предоставления субсидии на реализацию проекта', border)
        if item.stateEvents:
            worksheet_4.write('B8', 'Да', border_center)
        else:
            worksheet_4.write('B8', 'Нет', border_center)
        worksheet_4.write('B9', item.nameStateEvents, border)
        worksheet_4.write('A10', 'Соответствие нормам безопасности и законодательству Российской Федерации, включая ссылки \
на соответствующие нормативы (в случае использования типовой проектной документации дается информация \
о ее источнике)', border)
        worksheet_4.write('B10', item.security, border_center)
        worksheet_4.write('A11', 'Качество и обоснованность архитектурных и планировочных решений²', border)
        worksheet_4.write('B11', item.justification, border)
        worksheet_4.write('A12', 'Формы проведения процедур по выбору подрядчика либо закупок', border)
        worksheet_4.write('B12', item.forms, border)
        worksheet_4.write('A13', 'Мероприятия по поддержанию и/или развитию полученных в рамках проекта результатов³', border)
        worksheet_4.write('B13', item.supportEvents, border)
        worksheet_4.write('A14', 'Механизмы содержания и эксплуатации объектов по благоустройству', border)
        worksheet_4.write('B14', item.mechanisms, border)

    worksheet_4.merge_range("A15:B15", 'Примечание:\
\n¹Указываются: исходные данные по населенному пункту, точки притяжения, границы участка размещения \
объекта (ов), группа пользователей, заинтересованных в развитии территории, проблемы по благоустройству \
территории, опрос (голосование) жителей с целью определения приоритетных направлений развития территории, \
информационная кампания по привлечению граждан в формировании проекта, общественное обсуждение проекта, \
механизмы согласования выбора направлений для включения в проекты, информация, подтверждающая участие в \
процессе граждан, информация о принятии участия представителей различных некоммерческих организаций, \
бюджетных учреждений, учреждений образования и культуры, религиозных организаций, активных групп жителей, \
бизнес-сообщества и др., информация о привлечении архитектурных и ландшафтных дизайнеров, специалистов по \
благоустройству (разработан эскиз проекта), информация о публикации отчета по итогам обсуждения.\
\n²Указываются: учитывают ли принятые решения функции территории в соответствии с результатами \
предпроектного исследования, позволяют ли решения использовать территорию более 6 месяцев в году, \
учитывают ли решения интересы различных социальных и возрастных групп жителей населенного пункта, \
предусматривая востребованные ими сценарии использования территории, соответствуют ли решения \
техническим регламентам, правилам и нормам по благоустройству территорий (СНиП, ГОСТ, ПЗЗ и др.), \
при подготовке проекта использована ли типовая или повторного применения проектная документация, \
отдается ли предпочтение качественным, природным, экологическим материалам, энергосберегающим технологиям.\
\n³Указываются: обоснованные изменения, которые произойдут в населенном пункте в течение 3-5 лет в \
случае реализации проекта, благоустраиваемая территория является или будет являться зоной активного \
пешеходного транзита, на благоустраиваемой территории находятся здания и(или) зоны, расположенные в \
точках притяжения населенного пункта, благоустраиваемая территория связана или будет связана с \
туристскими маршрутами, местами массового отдыха населения, имеется потенциал для размещения объектов \
предпринимательской и социальной активности.', wrap_text)

    worksheet_5 = workbook.add_worksheet('План реализации проекта')

    worksheet_5.set_column(0, 0, 55)
    worksheet_5.set_column(1, 2, 20)
    worksheet_5.set_column(3, 3, 30)
    worksheet_5.set_row(0, 25)
    worksheet_5.set_row(1, 50)
    worksheet_5.set_row(3, 50)
    worksheet_5.set_row(5, 50)
    worksheet_5.set_row(7, 70)
    worksheet_5.set_default_row(22)

    worksheet_5.merge_range("A1:D1", "V. План реализации мероприятий проекта", header_sheet)

    worksheet_5.write('A2', 'Наименование мероприятия ', border_center)
    worksheet_5.write('B2', 'Сроки реализации\n (начало)', border_center)
    worksheet_5.write('C2', 'Сроки реализации\n (конец)', border_center)
    worksheet_5.write('D2', 'Ответственный исполнитель', border_center)

    row = 2
            
    worksheet_5.merge_range(row, 0, row, 3, '1. Подготовительные работы:', border)
    row += 1

    for item in planeEvents:
        if item.typeEvent.typeEvent == 'Подготовительные работы':
            worksheet_5.write(row, 0, item.nameEvent, border)
            worksheet_5.write_datetime(row, 1, item.dedlineStart, date_format)
            worksheet_5.write_datetime(row, 2, item.dedlineEnd, date_format)
            worksheet_5.write(row, 3, item.performer, border_center)
            row += 1

    worksheet_5.merge_range(row, 0, row, 3, '2. Приобретение оборудования:', border)
    row += 1

    for item in planeEvents:
        if item.typeEvent.typeEvent == 'Приобретение оборудования':
            worksheet_5.write(row, 0, item.nameEvent, border)
            worksheet_5.write_datetime(row, 1, item.dedlineStart, date_format)
            worksheet_5.write_datetime(row, 2, item.dedlineEnd, date_format)
            worksheet_5.write(row, 3, item.performer, border_center)
            row += 1

    worksheet_5.merge_range(row, 0, row, 3, '3. Ремонтно-строительные работы:', border)
    row += 1

    for item in planeEvents:
        if item.typeEvent.typeEvent == 'Ремонтно-строительные работы':
            worksheet_5.write(row, 0, item.nameEvent, border)
            worksheet_5.write_datetime(row, 1, item.dedlineStart, date_format)
            worksheet_5.write_datetime(row, 2, item.dedlineEnd, date_format)
            worksheet_5.write(row, 3, item.performer, border_center)
            row += 1

    worksheet_5.merge_range(row, 0, row, 3, '4. Прочая деятельность (указать наименование):', border)
    row += 1

    for item in planeEvents:
        if item.typeEvent.typeEvent == 'Прочая деятельность (указать наименование)':
            worksheet_5.write(row, 0, item.nameEvent, border)
            worksheet_5.write_datetime(row, 1, item.dedlineStart, date_format)
            worksheet_5.write_datetime(row, 2, item.dedlineEnd, date_format)
            worksheet_5.write(row, 3, item.performer, border_center)
            row += 1

    worksheet_6 = workbook.add_worksheet('Смета расходов')

    worksheet_6.set_column(0, 0, 50)
    worksheet_6.set_column(1, 5, 20)
    worksheet_6.set_row(0, 25)
    worksheet_6.set_row(4, 100)
    worksheet_6.set_default_row(22)

    worksheet_6.merge_range("A1:F1", "VI. Смета расходов по проекту¹", header_sheet)

    worksheet_6.merge_range("A2:A5", "Статьи расходов", border_center)
    worksheet_6.merge_range("B2:B5", "Общие расходы по проекту", border_center)
    worksheet_6.merge_range("C2:C5", "Запрашиваемые средства государственной поддержки", border_center)
    worksheet_6.merge_range("D2:F2", "Вклад инициатора проекта", border_center)
    worksheet_6.merge_range("D3:E3", "Местный бюджет", border_center)
    worksheet_6.merge_range("D4:E4", "в том числе:", border_center)
    worksheet_6.merge_range("F3:F5", "Внебюджетные источники", border_center)
    worksheet_6.write('D5', 'бюджет муниципального района (муниципального или городского округа)²', border_center)
    worksheet_6.write('E5', 'бюджет сельского (городского) поселения', border_center)

    row = 5

    for item in costEstimate:
        worksheet_6.write(row, 0, item.expenseItem, border)
        worksheet_6.write(row, 1, item.generalExpenses, border)
        worksheet_6.write(row, 2, item.stateExpenses, border)
        worksheet_6.write(row, 3, item.districtBudget, border)
        worksheet_6.write(row, 4, item.settlementBudget, border)
        worksheet_6.write(row, 5, item.offBudgetExpenses, border)
        row += 1

    worksheet_6.write(row, 0, 'Итого:', bold)

    for item in totalResults:
        worksheet_6.write(row, 1, item.totalGeneralExpenses, border)
        worksheet_6.write(row, 2, item.totalStateExpenses, border)
        worksheet_6.write(row, 3, item.totalDistrictBudget, border)
        worksheet_6.write(row, 4, item.totalSettlementBudget, border)
        worksheet_6.write(row, 5, item.totalOffBudgetExpenses, border)
    
    row += 1

    worksheet_6.set_row(row, 90)

    worksheet_6.merge_range(row, 0, row, 5, 'Примечание:\
\n¹Объемы средств государственной поддержки, местного бюджета и внебюджетных источников (в случае их \
вклада денежными средствами и включения в стоимость контракта (договора) со средствами государственной \
поддержки и местного бюджета) рассчитываются пропорционально по каждой статье расходов, предусмотренных \
проектом.\
\n²Объемы средств муниципального района (муниципального или городского округа) рассчитываются с соблюдением \
уровня софинансирования из бюджета Забайкальского края не более 99%.', wrap_text)
    
    row += 2

    worksheet_6.write(row, 0, 'И.о. (заполните поле)', sign)
    worksheet_6.write(row, 3, '(заполните поле)', sign)

    row += 1

    worksheet_6.write(row, 1, '(М.П., подпись)', sign)
    worksheet_6.write(row, 3, '(расшифровка)', sign)

    row += 2

    worksheet_6.write(row, 0, 'Исполнитель:', sign)

    row += 1

    worksheet_6.write(row, 0, 'И.о. (заполните поле)', sign)
    worksheet_6.write(row, 3, '(заполните поле)', sign)

    row += 1

    worksheet_6.write(row, 0, '(номер телефона)', sign)
    worksheet_6.write(row, 1, '(подпись)', sign)
    worksheet_6.write(row, 3, '(расшифровка)', sign)

    workbook.close()

    passport.file = 'passports/Passport №' + str(passport.id) + '.xlsx'
    passport.save()


@login_required(login_url = 'authorization')
def export(request, id):
    passport = get_object_or_404(Passports, id = id)
    
    if not os.path.exists(passport.file.url):
        excel(request, passport.id)

    response = FileResponse(open('media/passports/Passport №' + str(passport.id) + '.xlsx', 'rb'))

    return response