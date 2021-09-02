# -*- coding: utf-8 -*-
"""
Created on Tue Jun 22 13:18:44 2021

@author: kisha
"""
investment = 6000000
interest_rate = 13.07/100
total_interest = 0

for x in range(0, 35):
    total_interest += interest_rate*investment
    
investment += total_interest
    
print("The total investment after 35 years would be Rs.", investment)
