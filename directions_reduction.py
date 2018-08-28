#!/usr/bin/python 
# miguel.ortiz
# Problem: https://www.codewars.com/kata/550f22f4d758534c1100025a

def processInstr(arr) :
    nowhere=[('SOUTH','NORTH'), ('NORTH','SOUTH'), ('WEST','EAST'), ('EAST','WEST')]
    missleading=[]
    miss=''
    for i, j in enumerate(arr[:-1]):
        couple=(arr[i],arr[i+1])
        if couple in nowhere:
            missleading.append(i)
            missleading.append(i+1)
        else :
            pass
        miss=set(missleading)
        miss=list(miss)

    for i in sorted(miss, reverse=True) :
        try :
            if missleading[i] ==  missleading[i-1]:
                del missleading[missleading.index(i)]
                del missleading[i]
        except IndexError:
            pass
    for i in sorted(set(missleading), reverse=True) :
        del arr[i]
        del missleading[missleading.index(i)]
        
def dirReduc(arr):
    for i in arr :
        processInstr(arr)
    return arr
