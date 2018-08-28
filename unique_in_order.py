#!/usr/bin/python
# miguel.ortiz
# Problem: https://www.codewars.com/kata/54e6533c92449cc251001667

from itertools import groupby
def unique_in_order(iterable):
    values =[]
    for ch in groupby(iterable) :
        values.append(ch[0])
    return values
