# -*- coding: utf-8 -*-
"""
Created on Fri Apr 20 19:26:53 2018

@author: Sunday
"""

semi_annual_raise = .07 #compound interest
r = 0.04
portion_down_payment = 0.25
total_cost = 1000000
down_payment = total_cost*portion_down_payment

high = 10000 #bisection
low = 0
epsilon = 100
guess = high
step = 0

current_savings = float(0) #initializing guess
annual_salary = float(input("Enter your annual salary: "))
ori_annual_salary = annual_salary
for i in range(1,37):
    current_savings += annual_salary / 12 * guess / 10000 + current_savings * (r / 12)
    if i % 6 == 0:
        annual_salary += annual_salary * semi_annual_raise

while abs(current_savings - down_payment) > epsilon :
    if current_savings < down_payment: #bisection
        low = guess
    else:
        high = guess
     
    if guess == (high+low)//2:  #infinite loop check    
          break        
        
    guess = (high+low)//2 #next guess
    current_savings = 0
    annual_salary = ori_annual_salary
    for i in range(1,37):
        current_savings += annual_salary / 12 * guess / 10000 + current_savings*(r/12)
        if i % 6 == 0:
            annual_salary += annual_salary*semi_annual_raise
            
    step += 1    

if abs(current_savings - down_payment) > epsilon: #possible check
    print('It is not possible to pay the down payment in three years.') 
else:
    print('best savings rate: ', guess / 10000)
    print('Steps in bisection search: ', step)

    
    




