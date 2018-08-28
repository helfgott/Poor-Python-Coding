#!/usr/bin/python
# miguel.ortiz
# Problem: https://www.codewars.com/kata/5254ca2719453dcc0b00027d

import itertools
def permutations(string):
    string=list(string)
    results=[]
    iterObject=itertools.permutations(string, len(string))
    for i in iterObject :
       results.append(''.join(i))
    myresult=set(results)
    return myresult
