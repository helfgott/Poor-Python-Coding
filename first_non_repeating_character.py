# !/usr/bin/python
# miguel.ortiz
# Problem: https://www.codewars.com/kata/52bc74d4ac05d0945d00054e

def first_non_repeating_letter(s):

    char=''

    for x in s:
        if s.lower().count(x.lower()) == 1 :
            char=x
            break
            
    if char == '' :
        return  ''
    else :
        return char
