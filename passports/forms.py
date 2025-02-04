from django import forms
from .models import *


class PassportForm(forms.ModelForm):
    class Meta:
        model = Passports
        fields = ['nameProject', 'indicators', 'borderArea', 'address', 'OKTMO', 'populationLocality', 
                  'improvedArea', 'initiativeGroup', 'countMonth', 'dateStartPlane', 'dateEndPlane', 
                  'generalCost', 'stateSupport', 'localBudget', 'offBudget', 'citizen', 'citizenMoney', 
                  'citizenWork', 'citizenRooms', 'citizenTechnical', 'publicOrg', 'publicOrgMoney', 'publicOrgWork', 
                  'publicOrgRooms', 'publicOrgTechnical', 'legalEntities', 'legalEntitiesMoney', 'legalEntitiesWork', 
                  'legalEntitiesRooms', 'legalEntitiesTechnical']
        

class LaborPartForm(forms.ModelForm):
    class Meta:
        model = LaborPart
        fields = ['works', 'countManHour', 'costManHour', 'laborCost']


class TargetGroupForm(forms.ModelForm):
    class Meta:
        model = TargetGroup
        fields = ['populationVoted', 'populationPart', 'younger', 'adult', 'older', 'countBenefit']


class ProjectDescForm(forms.ModelForm):
    class Meta:
        model = ProjectDesc
        fields = ['targetProject', 'tasksProject', 'events', 'troubles', 
                  'stateMainEvents', 'nameStateMainEvents', 'stateEvents', 'nameStateEvents', 
                  'security', 'justification', 'forms', 'supportEvents', 'mechanisms']
        

class PlaneEventsForm(forms.ModelForm):
    class Meta:
        model = PlaneEvents
        fields = ['typeEvent', 'nameEvent', 'dedlineStart', 'dedlineEnd', 'performer']


class CostEstimateForm(forms.ModelForm):
    class Meta:
        model = CostEstimate
        fields = ['expenseItem', 'generalExpenses', 'stateExpenses', 'districtBudget', 
                  'settlementBudget', 'offBudgetExpenses']