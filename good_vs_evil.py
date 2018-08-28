#!/usr/bin/python
# miguel.ortiz
# Problem: https://www.codewars.com/kata/52761ee4cffbc69732000738

def goodVsEvil(good, evil):

    gWorth=[1,2,3,3,4,10]
    eWorth=[1,2,2,2,3,5,10]

    goodF=[int(a) * int(w) for a,w in zip(good.split(),gWorth)]
    evilF=[int(a) * int(w) for a,w in zip(evil.split(),eWorth)]

    if sum(goodF) > sum(evilF) :
        return 'Battle Result: Good triumphs over Evil'
    elif sum(evilF) > sum(goodF) :
        return 'Battle Result: Evil eradicates all trace of Good'
    else :
        return 'Battle Result: No victor on this battle field'
