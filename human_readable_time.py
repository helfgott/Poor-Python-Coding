#!/usr/bin/python
# miguel.ortiz
# Problem: https://www.codewars.com/kata/52685f7382004e774f0001f7

import re
def make_readable(seconds):
    patt=re.compile("\d+\d+")
    hours = seconds / 3600
    seconds = seconds % 3600
    minutes = seconds / 60
    seconds = seconds % 60

    mHours=patt.match(str(hours))
    mMinutes=patt.match(str(minutes))
    mSeconds=patt.match(str(seconds))

    if mHours == None :
        hours='0' + str(hours)
    if mMinutes == None  :
        minutes='0' + str(minutes)
    if mSeconds == None :
        seconds = '0' + str(seconds)

    return str(hours) + ':' +  str(minutes) + ':' + str(seconds)
