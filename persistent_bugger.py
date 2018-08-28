#!/usr/bin/python
# miguel.ortiz
# Problem: https://www.codewars.com/kata/55bf01e5a717a0d57e0000ec

def multip(numbers) :
    product= 1
    for i in str(numbers) :
        product *= int(i)
    return product
    
def persistence(n):
    counter=1
    if len(str(n)) > 1 :
        while True :
            product=multip(n)
            if len(str(product)) > 1:
                print 'this product can be proccesed again', product
                counter += 1
                n = product
            else :
                return counter
    else :
        return 0
