# coding=utf-8

import os

file = './data/record.txt'

def get() :
    f = open(file, 'r')
    data = [];
    for line in f:
        data.append(line.strip())
    f.close()
    return data

def save(list) :
    f = open(file, 'w')
    for line in list:
        f.write(line+"\n")
    f.close()

