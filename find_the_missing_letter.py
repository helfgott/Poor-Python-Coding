#!/usr/bin/python
# miguel.ortiz
# Problem: https://www.codewars.com/kata/5839edaa6754d6fec10000a2

def find_missing_letter(chars):
    
    alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    substring = []

    for letter in chars :
        if letter in alphabet :
            substring.append(alphabet.index(letter))

    last = substring[-1] + 1
    substring = alphabet[substring[0]:last]
    missingLetter = [x for x in substring if x not in chars]

    return missingLetter[0]

