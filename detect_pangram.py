#!/usr/bin/python
# miguel.ortiz
# Problem https://www.codewars.com/kata/545cedaa9943f7fe7b000048

import string
def is_pangram(s):
    p = [ w for w in string.ascii_lowercase if w not in s.lower() ]
    if not p :
        return True
    else :
        return False
