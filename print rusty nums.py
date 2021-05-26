import sys
import os

def sumDigits(num):
    result = 0
    while num >=10:
        result += num%10
        num = num // 10
    return result + num

with open(os.path.join(sys.path[0], "test.txt"), "r") as inputf:
    balls = [int(b) for b in inputf.readline().rstrip().split()]
    for ball in balls:
        print(ball, sumDigits(ball))
        
