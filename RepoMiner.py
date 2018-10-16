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
    with open("Result.csv", "w") as fileName:
        writer = csv.writer(fileName)
        writer.writerow(["Commit SHA", "Java File", "Old function signature", "New function signature"])
        writer.writerows(Result)
    return



dataTypes = ['void', 'int', 'double', 'float', 'String', 'boolean', 'char', 'long', 'short', 'byte']


def isMethod(statement):
#    print(statement)
    for i in dataTypes:
        dataTypeIn = statement.find(i) #Should have a return data type
        openingParenthesis = statement.find('(')
        invalidCharacter = ['=', '.print', '//'] #Method Signature Can't contain these
        validation = 0
        for j in invalidCharacter:
            if statement.find(j)>=0:
                validation = validation | 1
        if dataTypeIn>0 and openingParenthesis > dataTypeIn and validation == 0:
            return True
    return False


def RepoMiner(gitName):
    WriteToCSV = []
    for commit in RepositoryMining(gitName).traverse_commits():
        for mod in commit.modifications:
            if (mod.filename).find('java')>0:
                totalRows = len(mod.diff.splitlines())
                lines = mod.diff.splitlines()
                for rowNumber in range(totalRows):
                    if lines[rowNumber][0]== '-' and isMethod(lines[rowNumber]): # - Stands for delete and + stands for addition
                        SourceCode = mod.source_code
                        Hash = commit.hash
                        OldMethodSignature = str(lines[rowNumber])
                        NewMethodSignature = str(lines[rowNumber+1])
                        upto = OldMethodSignature.find(')')+1
                        OldMethodSignature = OldMethodSignature[1:upto]
                        upto = NewMethodSignature.find(')')+1
                        NewMethodSignature = NewMethodSignature[1:upto]
                        WriteToCSV.append([Hash, SourceCode, OldMethodSignature, NewMethodSignature])
    return WriteToCSV


#if __name__== "main":
GitFileName = input()       #Repository name with Path
Result = RepoMiner(GitFileName) #Finds the Result
WriteReport(Result) #Print to CSV

