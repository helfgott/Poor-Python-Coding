#!/usr/bin/python
# miguel.ortiz
# Problem: https://www.codewars.com/kata/55908aad6620c066bc00002a

def xo(s):

    if not s :
        return True
    else :
        s = s.lower()
        my_dict = {i:s.count(i) for i in s}
        if 'x' not in my_dict and 'o' not in my_dict :
            return False
        elif 'x' in my_dict and 'o' in my_dict and my_dict['x'] == my_dict['o'] :
            return True
        elif 'x' in my_dict and 'o' in my_dict and my_dict['x'] != my_dict['o'] :
            return False
        else :
           return True
