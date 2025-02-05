younger.oninput = function() { countBenefit(); };
adult.oninput = function() { countBenefit(); };
older.oninput = function() { countBenefit(); };

districtBudget.oninput = function() { generalExpenses(); };
stateExpenses.oninput = function() { generalExpenses(); };
settlementBudget.oninput = function() { generalExpenses(); };
offBudgetExpenses.oninput = function() { generalExpenses(); };

stateSupport.oninput = function() { generalCost(); };
localBudget.oninput = function() { generalCost(); };
citizenMoney.oninput = function() { generalCost(); };
citizenWork.oninput = function() { generalCost(); };
citizenRooms.oninput = function() { generalCost(); };
citizenTechnical.oninput = function() { generalCost(); };
publicOrgMoney.oninput = function() { generalCost(); };
publicOrgWork.oninput = function() { generalCost(); };
publicOrgRooms.oninput = function() { generalCost(); };
publicOrgTechnical.oninput = function() { generalCost(); };
legalEntitiesMoney.oninput = function() { generalCost(); };
legalEntitiesWork.oninput = function() { generalCost(); };
legalEntitiesRooms.oninput = function() { generalCost(); };
legalEntitiesTechnical.oninput = function() { generalCost(); };

function countBenefit() {
    document.getElementById('countBenefit').value = 
        Number(document.getElementById('younger').value) + 
        Number(document.getElementById('adult').value) + 
        Number(document.getElementById('older').value);
}

function generalExpenses() {
    result = Number(document.getElementById('districtBudget').value) + 
        Number(document.getElementById('stateExpenses').value) + 
        Number(document.getElementById('settlementBudget').value) +
        Number(document.getElementById('offBudgetExpenses').value);
    document.getElementById('generalExpenses').value = Number(result.toFixed(2));
}

function generalCost() {
    result = Number(document.getElementById('stateSupport').value) + Number(document.getElementById('localBudget').value) + 
        Number(document.getElementById('citizenMoney').value) + Number(document.getElementById('citizenWork').value) + 
        Number(document.getElementById('citizenRooms').value) + Number(document.getElementById('citizenTechnical').value) +
        Number(document.getElementById('publicOrgMoney').value) + Number(document.getElementById('publicOrgWork').value) + 
        Number(document.getElementById('publicOrgRooms').value) + Number(document.getElementById('publicOrgTechnical').value) +
        Number(document.getElementById('legalEntitiesMoney').value) + Number(document.getElementById('legalEntitiesWork').value) + 
        Number(document.getElementById('legalEntitiesRooms').value) + Number(document.getElementById('legalEntitiesTechnical').value);
    document.getElementById('generalCost').value = Number(result.toFixed(2));
    
    offBudget = Number(document.getElementById('citizenMoney').value) + 
        Number(document.getElementById('citizenWork').value) + Number(document.getElementById('citizenRooms').value) + 
        Number(document.getElementById('citizenTechnical').value) + Number(document.getElementById('publicOrgMoney').value) + 
        Number(document.getElementById('publicOrgWork').value) + Number(document.getElementById('publicOrgRooms').value) + 
        Number(document.getElementById('publicOrgTechnical').value) + Number(document.getElementById('legalEntitiesMoney').value) + 
        Number(document.getElementById('legalEntitiesWork').value) + Number(document.getElementById('legalEntitiesRooms').value) + 
        Number(document.getElementById('legalEntitiesTechnical').value);
    document.getElementById('offBudget').value = Number(offBudget.toFixed(2));
    
    citizen = Number(document.getElementById('citizenMoney').value) + 
        Number(document.getElementById('citizenWork').value) + Number(document.getElementById('citizenRooms').value) + 
        Number(document.getElementById('citizenTechnical').value);
    document.getElementById('citizen').value = Number(citizen.toFixed(2));
   
    publicOrg = Number(document.getElementById('publicOrgMoney').value) + 
        Number(document.getElementById('publicOrgWork').value) + Number(document.getElementById('publicOrgRooms').value) + 
        Number(document.getElementById('publicOrgTechnical').value);
    document.getElementById('publicOrg').value = Number(publicOrg.toFixed(2));
    
    legalEntities = Number(document.getElementById('legalEntitiesMoney').value) + 
        Number(document.getElementById('legalEntitiesWork').value) + Number(document.getElementById('legalEntitiesRooms').value) + 
        Number(document.getElementById('legalEntitiesTechnical').value);
    document.getElementById('legalEntities').value = Number(legalEntities.toFixed(2));
}