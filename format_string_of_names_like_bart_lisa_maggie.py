#!/usr/bin/python
# miguel.ortiz
# Problem: https://www.codewars.com/kata/53368a47e38700bd8300030d

def namelist(names):

    s = []
    f = []
    
    for i in  names[:-2] :
            s.append(i['name'])
    for i in names[-2:] :
            f.append(i['name'])
    if len(names) == 0 :
            return ''
    elif len(names) == 1 :
             return names[0].values()[0]
    elif len(names) == 2 :
            return ' & '.join(f)
    elif len(names) > 2 :
            return ', '.join(s) + ', ' + ' & '.join(f)
