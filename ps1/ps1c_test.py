# -*- coding: utf-8 -*-
"""
Created on Sun Apr 22 19:16:26 2018

@author: Sunday
"""
semi_annual_raise = .07
r = 0.04
portion_down_payment = 0.25
total_cost = 1000000
current_savings = float(0)
annual_salary = 120000
guess_portion_saved = 1875

for i in range(1,37):
    (annual_salary/12)*(guess_portion_saved/10000)+current_savings*(1+r/12)
    #print(annual_salary/12*guess_portion_saved/10000, current_savings*(1+r/12))
    current_savings += annual_salary/12*(guess_portion_saved/10000)+current_savings*(r/12)
    if i % 6 == 0:
        annual_salary += annual_salary*semi_annual_raise
        
print(current_savings)