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
    with open("Outputs/Result.csv", "w") as fileName:
        writer = csv.writer(fileName)
        writer.writerow(["Commit SHA", "Java File", "Old function signature", "New function signature"])
        writer.writerows(Result)
    return


def isParameterAdded(fromStatement, toStatement):                               #Old Method , New Method
    uptoOpen = fromStatement.find('(')
    uptoClose = fromStatement.find(')')
    subFromStatement = fromStatement[1:uptoOpen]                                #Substring without the - sign and upto opening paranthesis
    paraFromStatement = (fromStatement[uptoOpen:uptoClose]).split(',')          #List the Parameters to Method
    uptoOpen = toStatement.find('(')
    uptoClose = toStatement.find(')')
    subToStatement = toStatement[1:uptoOpen]
    paraToStatement = (toStatement[uptoOpen:uptoClose]).split(',')
    if subFromStatement == subToStatement and len(paraFromStatement) < len(paraToStatement): # Same Method and Parameter Addtion Condition
        return True
    return False


def isAnyInvalidCharacter(fromStatement):                                       # Return 0 if there is not invalid substring for method, 1 otherwise
    invalidCharacter = ['=', '.print', '//', '%', '""', '" "', '.']             #Method Signature Can't contain these
    validation = 0
    for j in invalidCharacter:
        if fromStatement.find(j)>=0:
            validation = validation | 1
    return validation


dataTypes = ['void', 'int', 'double', 'float', 'String', 'boolean', 'char', 'long', 'short', 'byte'] #Possible Datatypes a method can have


def isMethod(fromStatement, toStatement):                                       #Deleted Statement and Added statement are methods or not
    if isParameterAdded(fromStatement, toStatement) == True:
#        print(fromStatement)
#        print(toStatement)
        for i in dataTypes:
            dataTypeIn = fromStatement.find(i) #Should have a return data type
            openingParenthesis = fromStatement.find('(')
            validation = isAnyInvalidCharacter(fromStatement) # Has invalid character or not
            if dataTypeIn>0 and openingParenthesis > dataTypeIn and validation == 0: #Datatype should present, opening paranthesis after the datatype, and no invalid substring, all these ensures the method
                return True
    return False


def RepoMiner(gitName):
    WriteToCSV = []
    for commit in RepositoryMining(gitName).traverse_commits():                 #For every commits
        for mod in commit.modifications:                                        #For every modifications
            if (mod.filename).find('.java')>=0:                                 #Only for Java Files
                totalRows = len(mod.diff.splitlines())
                lines = mod.diff.splitlines()
                for rowNumber in range(totalRows):
                    if rowNumber < (totalRows-1):
                        if len(lines[rowNumber])>0 and len(lines[rowNumber+1]) > 0:
                            if lines[rowNumber][0]== '-' and lines[rowNumber+1][0]=='+' and isMethod(lines[rowNumber], lines[rowNumber+1]): # A deletion and after that an addition of methods with parameter addition
                                SourceCode = mod.source_code                    #New Source code
                                Hash = commit.hash                              # Commit SHA
                                OldMethodSignature = str(lines[rowNumber])
                                NewMethodSignature = str(lines[rowNumber+1])
                                upto = OldMethodSignature.find(')')+1
                                OldMethodSignature = OldMethodSignature[1:upto] #Extracting the old function Signature
                                upto = NewMethodSignature.find(')')+1
                                NewMethodSignature = NewMethodSignature[1:upto] #Extracting the new function signature
                                WriteToCSV.append([Hash, SourceCode, OldMethodSignature, NewMethodSignature]) # Ready for report printing
    return WriteToCSV


if __name__== "__main__":
    GitFileName = input("Enter the git name with path: ")       #Repository name with Path
    Result = RepoMiner(GitFileName) #Finds the Result
    WriteReport(Result) #Print to CSV
    print("\nOutput printed successfully...")

