from .models import *
from .forms import *
from django.contrib import admin
from django.http import FileResponse
from django.utils import timezone, dateformat
import xlsxwriter


admin.site.register(TypeEvents)


class LaborPartInline(admin.StackedInline):
    extra = 0
    model = LaborPart
    fields = ['works', ('countManHour', 'costManHour', 'laborCost')]


class TargetGroupInline(admin.StackedInline):
    extra = 0
    model = TargetGroup
    fields = [('populationVoted', 'populationPart', 'countBenefit'), ('younger', 'adult', 'older')]


class ProjectDescInline(admin.StackedInline):
    extra = 0
    model = ProjectDesc


class PlaneEventsInline(admin.StackedInline):
    extra = 0
    model = PlaneEvents
    fields = ['typeEvent', 'nameEvent', ('dedlineStart', 'dedlineEnd'), 'performer']


class CostEstimateInline(admin.StackedInline):
    extra = 0
    model = CostEstimate
    fields = ['expenseItem', 'generalExpenses', ('stateExpenses', 'districtBudget', 
                  'settlementBudget', 'offBudgetExpenses')]


class TotalResultsInline(admin.StackedInline):
    extra = 0
    model = TotalResults


class PassportsAdmin(admin.ModelAdmin):
    list_display = ('nameProject', 'user', 'get_total_points', 'file_link')
    fieldsets = (
        ('Общая характеристика', {
            'fields': ('user', 'nameProject', 'indicators', 'borderArea', 'address', 'OKTMO', ('populationLocality', 
                'improvedArea'), 'initiativeGroup', 'countMonth', ('dateStartPlane', 'dateEndPlane'), 
                'generalCost', ('stateSupport', 'localBudget', 'offBudget'), 'citizen', ('citizenMoney', 
                'citizenWork', 'citizenRooms', 'citizenTechnical'), 'publicOrg', ('publicOrgMoney', 'publicOrgWork', 
                'publicOrgRooms', 'publicOrgTechnical'), 'legalEntities', ('legalEntitiesMoney', 'legalEntitiesWork', 
                'legalEntitiesRooms', 'legalEntitiesTechnical'))
        }),
    )
    inlines = [LaborPartInline, TargetGroupInline, ProjectDescInline,
               PlaneEventsInline, CostEstimateInline]
admin.site.register(Passports, PassportsAdmin)


@admin.action(description="Экспорт данных в .XLSX")
def export_result(modeladmin, request, queryset):
    workbook = xlsxwriter.Workbook('media/results/Реестр проектов ' + dateformat.format(timezone.now(), 'Y-m-d') + '.xlsx')
    worksheet = workbook.add_worksheet('Реестр проектов')

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
    bold = workbook.add_format({ 
        'bold': True, 'border': 1, 'font_size': 12, 'align': 'center',
        'valign': 'vcenter', 'font_name': 'Times New Roman'
    })
    bold.set_text_wrap()

    worksheet.set_column(0, 0, 5)
    worksheet.set_column(1, 1, 40)
    worksheet.set_column(2, 7, 17)
    worksheet.set_column(8, 8, 10)
    worksheet.set_column(9, 9, 30)

    worksheet.set_row(1, 35)
    worksheet.set_row(3, 15)
    worksheet.set_default_row(22)

    worksheet.merge_range('B1:I1', 'Реестр допущенных', border_center)
    worksheet.merge_range('A2:A3', '№ п/п', border_center)
    worksheet.merge_range('B2:B3', 'Наименование проекта', border_center)
    worksheet.merge_range('C2:C3', 'Общая стоимость проекта, рублей', border_center)
    worksheet.merge_range('D2:D3', 'Субсидия, рублей', border_center)
    worksheet.merge_range('E2:H2', 'Финансирование, рублей', border_center)
    worksheet.write('E3', 'ФБ', border_center)
    worksheet.write('F3', 'КБ', border_center)
    worksheet.write('G3', 'МБ', border_center)
    worksheet.write('H3', 'ВБ', border_center)
    worksheet.merge_range('I2:I3', 'Баллы', border_center)
    worksheet.merge_range('J1:J3', 'Районы/округа', border_center)

    row = 4

    for item in queryset:
        count = 1
        worksheet.write(row, 0, count, border_center)
        worksheet.write(row, 1, item.passport.nameProject, border)
        worksheet.write(row, 2, item.get_general_cost(), border_center)
        worksheet.write(row, 3, item.get_subsidy(), border_center)
        worksheet.write(row, 4, item.state, border_center)
        worksheet.write(row, 5, item.region, border_center)
        worksheet.write(row, 6, item.local, border_center)
        worksheet.write(row, 7, item.off, border_center)
        worksheet.write(row, 8, item.passport.get_total_points(), border_center)
        worksheet.write(row, 9, item.passport.get_user(), border_center)
        count += 1
        row += 1

    worksheet.write(row, 0, '', border)
    worksheet.write(row, 1, 'Всего:', bold)
    worksheet.write_formula(row, 2, '=SUM(C5:C' + str(row) + ')', bold)
    worksheet.write_formula(row, 3, '=SUM(D5:D' + str(row) + ')', bold)
    worksheet.write_formula(row, 4, '=SUM(E5:E' + str(row) + ')', bold)
    worksheet.write_formula(row, 5, '=SUM(F5:F' + str(row) + ')', bold)
    worksheet.write_formula(row, 6, '=SUM(G5:G' + str(row) + ')', bold)
    worksheet.write_formula(row, 7, '=SUM(H5:H' + str(row) + ')', bold)
    worksheet.write(row, 8, '', border)
    worksheet.write(row, 9, '', border)

    workbook.close()

    response = FileResponse(open('media/results/Реестр проектов ' + dateformat.format(timezone.now(), 'Y-m-d') + '.xlsx', 'rb'))

    return response


class ProjectRegisterAdmin(admin.ModelAdmin):
    list_display = ('passport', 'date', 'get_general_cost', 'get_subsidy', 'state', 'region', 'local', 'off', 'get_total_points')
    actions = [export_result]

    def get_total_points(self, object):
        return object.passport.get_total_points()
    get_total_points.short_description = u'Баллы'
admin.site.register(ProjectRegister, ProjectRegisterAdmin)