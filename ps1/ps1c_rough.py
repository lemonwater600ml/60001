# -*- coding: utf-8 -*-
"""
Created on Fri Apr 20 19:26:53 2018

@author: Sunday
"""
#return of investment(compound interest)
semi_annual_raise = .07
r = 0.04
portion_down_payment = 0.25
total_cost = 1000000
current_savings = float(0)
#User enter information
annual_salary = float(input("Enter your annual salary: "))
portion_saved = int(10000)

#pick up a portion


#calculate money after 36 months
for i in range(1,37):
    (annual_salary/12)*(portion_saved/10000)+current_savings*(1+r/12)
    #print(annual_salary/12*portion_saved/10000, current_savings*(1+r/12))
    current_savings += annual_salary/12*(portion_saved/10000)+current_savings*(r/12)
    if i % 6 == 0:
        annual_salary += annual_salary*semi_annual_raise



###############
#step = 1        
#while current_savings > total_cost*portion_down_payment :
#    print(current_savings, portion_saved)
#    #calculate for next test
#    portion_saved = portion_saved/2
#    current_savings = 0
#    for i in range(1,37):
#        annual_salary/12*(portion_saved/10000)+current_savings*(1+r/12)
#        current_savings += annual_salary/12*(portion_saved/10000)+current_savings*(r/12)
#        if i % 6 == 0:
#            annual_salary += annual_salary*semi_annual_raise
#    step += 1
##instruct to right number    
#portion_saved = portion_saved*2
#step = step -1
#print('best savings rate: ', portion_saved)
#print('Steps in bisection search: ', step)
################
#n=1 #months
#while annual_salary/12*portion_saved+current_savings*(1+r/12) < total_cost*portion_down_payment:
#    current_savings += annual_salary/12*portion_saved+current_savings*(r/12)
#    n += 1
#    if (n-1) % 6 == 0:
#        annual_salary += annual_salary*semi_annual_raise
#print("The number of months:",n)
##For test
##print('condition is:', total_cost*portion_down_payment)
##print('money is:', annual_salary/12*portion_saved+current_savings*(1+r/12))