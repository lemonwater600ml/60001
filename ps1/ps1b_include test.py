# -*- coding: utf-8 -*-
"""
Created on Fri Apr 20 19:26:53 2018

@author: Sunday
"""
#return of investment(compound interest)
r = float(0.04)
portion_down_payment = 0.25
current_savings = float(0)
#User enter information
annual_salary = float(input("Enter your annual salary: "))
portion_saved = float(input("Enter the percent of your salary to save, as a decimal: "))
total_cost = float(input("Enter the cost of your dream home: "))
semi_annual_raise = (float(input("Enter the semiannual raise, as a decimal: ")))
# n number of months
n = 1
#The money a user have is the salary of the month + current savings
#after n month, user's money for house is salary(in the month) + saving(before the month)*(1+r)
while annual_salary/12*portion_saved+current_savings*(1+r/12) < total_cost*portion_down_payment:
    #If salary + saving with return cannot meet the down payment, put them into savings
    #new current_saving is old current_saving + salary + return of old current_saving
    current_savings += annual_salary/12*portion_saved+current_savings*(r/12)
    n += 1
    if (n-1) % 6 == 0:
        annual_salary += annual_salary*semi_annual_raise
print("The number of months:",n)
