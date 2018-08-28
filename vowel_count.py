#!/usr/bin/python
# miguel.ortiz
# Problem: https://www.codewars.com/kata/54ff3102c1bad923760001f3

def getCount(inputStr):
    num_vowels = 0
    vowels = ['a','e','i','o','u']
    # con "in" se puede iterar la lista para buscar y se abrevia codigo.
    for letter in inputStr :
        if letter in vowels :
            num_vowels = num_vowels + 1
        else :
            pass
    return num_vowels
