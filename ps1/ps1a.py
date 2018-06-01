# -*- coding: utf-8 -*-
"""
Created on Fri Apr 20 19:26:53 2018

@author: Sunday
"""
#Set up return of investment( interest), current savings, and portion of down payment.
r = float(0.04)
portion_down_payment = 0.25
current_savings = float(0)
#Ask user provide information including price, current savings, and annual salary
total_cost = float(input("Please let me know your the price of your dream house? \n"))
annual_salary = float(input("What is your annual salary? \n"))
monthly_salary = annual_salary/12
#User enter a percentage. Program change to decimal.
portion_saved = float(input("What is the portion you are willing to save every month in percentage? _____% \n"))/100
#print("Just for your information, you invest your current savings very wisely. Your annual return is", str(r)+".")
#print("The down payment for your dream house is", str(portion_down_payment)+".")
#print("nd, I assume your current savings is 0")
#after n months
n = 1
#set user get salary at the end of month. 
#after n month, user's money for house is salary(in the month) + saving(before the month)*(1+r)
while monthly_salary*portion_saved+current_savings*(1+r/12) < total_cost*portion_down_payment:
    ###This is for test only
    ###print("Your money for", n, "month is", str(monthly_salary*portion_saved),'+', str(current_savings*(1+r/12))+".")
    #If salary + saving with return cannot meet the down payment, put them into savings
    #new current_saving is old current_saving + salary + return of old current_saving
    current_savings += monthly_salary*portion_saved+current_savings*(r/12)
    n += 1
if n == 1:
    print("Wow! You earn the down payment after work", n, "month.")
print("After", n, "months, you earn the down payment.\nWhen your money for house is", round(monthly_salary*portion_saved+current_savings*(1+r/12),2), ".")