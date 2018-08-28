#!/usr/bin/python
# miguel.ortiz
# Problem: https://www.codewars.com/kata/515de9ae9dcfc28eb6000001

def solution(string):
    myList=[]
    if not string :
        return []
    elif len(string)%2 == 0 :
        for i in range(0,len(string)+1,2):
            myList.append(string[i-2:i])
        myList.remove('')
        return myList
    else :
        for i in range(0,len(string),2):
            myList.append(string[i-2:i])
        myList.append(string[-1]+'_')
        myList.remove('')
        return myList
