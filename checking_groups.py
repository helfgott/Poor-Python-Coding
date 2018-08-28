#!/usr/bin/python
# miguel.ortiz
# Problem: https://www.codewars.com/kata/54b80308488cb6cd31000161

def group_check(s):
    
    import re
    specialChars={'}':'{',')':'(',']':'['}
    newSh=[]
    errStr=0
    
    for i in range(0,len(s)):
        s = re.sub(r'\[\]|\(\)|\{\}', '', s)
        if bool(re.sub(r'\[\]|\(\)|\{\}', '', s)) == False :
            break
    
    fh, sh = s[:len(s)/2], s[len(s)/2:]
    sh = sh[::-1]

    if not s :
        return True
    elif len(s)%2 != 0 :
        return False
    else :

        for ch in sh :
            if ch in specialChars :
                newSh.append(specialChars[ch])
            else :
                newSh.append(ch)

        for i in range(0,len(newSh)) :

            if fh[i] != newSh[i] :
                errStr = errStr + 1
                print fh[i], '<-'
                print newSh[i] ,'<-'
            else :
                pass
    if errStr != 0 :
        return False
    else :
        return True
        
