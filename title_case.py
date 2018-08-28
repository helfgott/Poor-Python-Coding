#!/usr/bin/python
# miguel.ortiz
# Problem: https://www.codewars.com/kata/5202ef17a402dd033c000009

def title_case(*args):
    if not args[0] and not args[1]:
        return ''
    else :
        titleLower = args[0].lower() 
    if not 1 < len(args):
        return args[0].title()
    else :
        exceptionsLower = args[1].lower()
        newString=""        
        newString+= titleLower.split()[0].capitalize()
        for word in titleLower.split()[1:] :
            if not exceptionsLower :
                pass 
            elif word in exceptionsLower.split() :
                newString+= (' ' + word)
            else :
                newString+= (' ' + word.capitalize())

        return newString
