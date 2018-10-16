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


def isParameterAdded(fromStatement, toStatement):
    uptoOpen = fromStatement.find('(')
    uptoClose = fromStatement.find(')')
    subFromStatement = fromStatement[1:uptoOpen]
    paraFromStatement = (fromStatement[uptoOpen:uptoClose]).split(',')
    uptoOpen = toStatement.find('(')
    uptoClose = toStatement.find(')')
    subToStatement = toStatement[1:uptoOpen]
    paraToStatement = (toStatement[uptoOpen:uptoClose]).split(',')
    if subFromStatement == subToStatement and len(paraFromStatement) != len(paraToStatement):
        return True
    return False


def isAnyInvalidCharacter(fromStatement):
    invalidCharacter = ['=', '.print', '//'] #Method Signature Can't contain these
    validation = 0
    for j in invalidCharacter:
        if fromStatement.find(j)>=0:
            validation = validation | 1
    return validation


dataTypes = ['void', 'int', 'double', 'float', 'String', 'boolean', 'char', 'long', 'short', 'byte']


def isMethod(fromStatement, toStatement):
#    print(statement)
    if isParameterAdded(fromStatement, toStatement) == True:
        for i in dataTypes:
            dataTypeIn = fromStatement.find(i) #Should have a return data type
            openingParenthesis = fromStatement.find('(')
            validation = isAnyInvalidCharacter(fromStatement) # Has invalid character or not
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
                    if rowNumber < (totalRows-1):
                        if lines[rowNumber][0]== '-' and isMethod(lines[rowNumber], lines[rowNumber+1]): # - Stands for delete and + stands for addition
                            SourceCode = ""
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

