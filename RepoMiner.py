#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 15 19:23:02 2018

@author: Habibur Rahman
@email: habib[dot]rahman[at]uits[dot]edu[dot]bd
"""
import csv
from pydriller import RepositoryMining


def WriteReport(Result):
    with open("Result.csv", "wb") as fileName:
        writer = csv.writer(fileName)
        for row in Result:
            print(row)
            writer.writerows(row)



dataTypes = ['void', 'int', 'double', 'float', 'String', 'boolean', 'char', 'long', 'short', 'byte']


def isMethod(statement):
#    print(statement)
    for i in dataTypes:
        dataTypeIn = statement.find(i)
        openingParenthesis = statement.find('(')
        invalidCharacter = '='
        validation = statement.find(invalidCharacter)
        if dataTypeIn>0 and openingParenthesis > dataTypeIn and validation < 0 :
            return True;


def RepoMiner(gitName):
    WriteToCSV = []
    for commit in RepositoryMining(gitName).traverse_commits():
    #    print(commit.hash)
#        print(commit.author.name)
    #    print(commit.author_date)
        for mod in commit.modifications:
    #        print(mod.filename)
    #        print((mod.filename).find('java')>0)
            if (mod.filename).find('java')>0:
    #            print(mod.filename + " is changed!")
                totalRows = len(mod.diff.splitlines())
    #            print(totalRows)
                lines = mod.diff.splitlines()
                for rowNumber in range(totalRows):
                    if lines[rowNumber][0]== '-' and isMethod(lines[rowNumber]):
#                        print(mod.source_code)
#                        print(lines[rowNumber])
#                        print(lines[rowNumber+1])
                        SourceCode = ""+mod.source_code
                        Hash = commit.hash

                        OldMethodSignature = ""+str(lines[rowNumber])
                        NewMethodSignature = ""+str(lines[rowNumber+1])
                        upto = OldMethodSignature.find[')']+1
                        print(upto)
                        print(""+str(Hash)+" "+OldMethodSignature[1:upto])
                        WriteToCSV.append([Hash, SourceCode, OldMethodSignature, NewMethodSignature])
    return WriteToCSV


#if __name__== "main":
GitFileName = input()
Result = RepoMiner(GitFileName)
#print(Result)
#WriteReport(Result)

