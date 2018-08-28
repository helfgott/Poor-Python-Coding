# /usr/bin/python
# miguel.ortiz
# Problem: https://www.codewars.com/kata/5629db57620258aa9d000014

from itertools import groupby
def mix(s1, s2):

    s1dic={}
    s2dic={}
    s1Letters,s2Letters=filter(str.islower, s1),filter(str.islower, s2)
    s1=[s1dic.update({i:s1Letters.count(i)}) for i in set(s1Letters)]
    s2=[s2dic.update({i:s2Letters.count(i)}) for i in set(s2Letters)]
    results=[]

    for key,value in s1dic.iteritems():
        try :
            if value > s2dic[key] :
                results.append('1:'+str(key*value))
                del s2dic[key]
            elif value < s2dic[key]:
                results.append('2:'+str(key*s2dic[key]))
                del s2dic[key]
        except KeyError :
            if value > 1 :
                results.append('1:'+str(key*value))
            pass

    for key,value in s2dic.iteritems():
        try:
            if value == s1dic[key] and len(str(key*value)) > 1:
                results.append('3:' + str(key*value))
        except KeyError:
            if value > 1 :
                results.append('2:'+str(key*value))
            pass

    results=sorted(results,key=len, reverse=True)
    results= [list(g) for k, g in groupby(results, key=len)]

    ordered=[]

    for sublist in results :
        ordered += sorted(sublist, key=lambda x: x.split()[0])
    string='/'.join(ordered)
    finalString=string.replace('3','=')
    return finalString
