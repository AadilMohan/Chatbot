
'''This module has functions to determine the asset allocation and the funds to use for investment decision'''
import logging
import sys
from math import sqrt
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
log = logging.getLogger(__name__)

allocation_equity = 0.0
allocation_bond = 0.0

def retirement_asset_allocation(age):
    try:
        log.info("Allocating asset based on age")

        if age <= 50 :
            allocation_equity = 0.8
            allocation_bond = 0.2

        elif (age > 50) and (age < 65):
            # use y= -4x + 80%
            age_pending_retirement = 65 - age #65 is retirement age
            allocation_equity = ((-4 * age_pending_retirement) + 80)/100
            allocation_bond = 1 - allocation_equity

        elif age > 65:
            allocation_equity = 0.2
            allocation_bond = 0.8

        return allocation_bond,allocation_equity
    except Exception as exp:
        log.debug("Allocating asset based on age failed - Excp - " + exp)

def analyse_bank_statement(df_bank_statement):
    #get income,expenditure and saving from bank statement
    #identify income
    #identify expenditure
    #identify saving

    pass

def investment_method(goal):

    if goal == "Retirement":
        return "SIP"
    elif goal == "Expenditure Goal":
        #ask user for the methodology - Lump sum or SIP
        pass

def decide_SIP_amount(saving,emergency_corpus,income):
    if emergency_corpus == True:
        if saving > (income * 0.33):# Choosing 33% to invest
            monthly_investment = (income * 0.33)
        elif saving < (income * 0.33):
            monthly_investment = saving * 0.7# Choosing 70%of saving to invest
    elif emergency_corpus == False:
            monthly_investment = saving * 0.3# Choosing 30%of saving to invest
    return monthly_investment

def adjust_asset_allocation_as_per_risk_profile(allocation_bond,allocation_equity,risk_profile):

    if "High" in risk_profile:
        pass
    elif "Medium" in risk_profile:
        if allocation_bond< 0.4:
            allocation_bond = 0.4
        if allocation_equity > 0.6:
            allocation_equity = 0.6
    elif "Low" in risk_profile:
        if allocation_bond < 0.8:
            allocation_bond = 0.8
        if allocation_equity > 0.2:
            allocation_equity = 0.2

    return allocation_bond,allocation_equity
















if __name__ == '__main__':
    allocation_bond,allocation_equity = retirement_asset_allocation(20)
    allocation_bond,allocation_equity = adjust_asset_allocation_as_per_risk_profile(allocation_bond,allocation_equity,"Medium Risk")
    SIP_amount = decide_SIP_amount(20000, True , 50000)
    print("Bond Allocation :"+ str(allocation_bond))
    print("Equity Allocation :"+ str(allocation_equity))
    print("SIP Amount :"+ str(SIP_amount))










