#!/usr/bin/python
# miguel.ortiz
# Problem: https://www.codewars.com/kata/523a86aa4230ebb5420001e1

def anagrams(word, words):
    print word, '<--oword'
    validAnagrams = []
    for anagram in words :
        compare = list(set(anagram) - set(word))
        if len(word) != len(anagram) :
            pass
        elif not compare and len(set(anagram)) == len(set(word)) :
            validAnagrams.append(anagram)
    
    return validAnagrams
