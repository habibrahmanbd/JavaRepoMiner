#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 15 19:23:02 2018

@author: Habibur Rahman
@email: habib[dot]rahman[at]uits[dot]edu[dot]bd
"""
import csv

from pydriller import RepositoryMining


def WriteReport(Result, ResultFileName):
    with open("Outputs/"+ResultFileName+".csv", "w") as fileName:
        writer = csv.writer(fileName)
        writer.writerow(["Commit SHA", "Java File", "Old function signature", "New function signature"])
        writer.writerows(Result)
    return


def isParameterAdded(fromStatement, toStatement):  # Old Method , New Method
    uptoOpen = fromStatement.find('(')
    uptoClose = fromStatement.find(')')
    subFromStatement = fromStatement[1:uptoOpen]  # Substring without the - sign and upto opening paranthesis
    paraFromStatement = (fromStatement[uptoOpen:uptoClose]).split(',')  # List the Parameters to Method
    uptoOpen = toStatement.find('(')
    uptoClose = toStatement.find(')')
    subToStatement = toStatement[1:uptoOpen]
    paraToStatement = (toStatement[uptoOpen:uptoClose]).split(',')
    if subFromStatement == subToStatement and len(paraFromStatement) < len(
            paraToStatement):  # Same Method and Parameter Addtion Condition
        return True
    return False


def isClassAdded(fromStatement, toStatement):  # Old Class, New Class
    uptoOpen = fromStatement.find('{')
    fromClass = fromStatement.find('Class ')
    subFrom = fromStatement[fromClass:uptoOpen]  # Substring between 'Class' and '{'
    uptoOpen = toStatement.find('{')
    fromClass = toStatement.find('Class ')
    subTo = toStatement[fromClass:uptoOpen]  # Substring between 'Class' and '{'
    if (subFrom != subTo):
        return True
    return False


def isLibraryAdded(fromStatement, toStatement):  # Old Class, New Class
    uptoOpen = fromStatement.find(';')
    fromClass = fromStatement.find('import ')
    subFrom = fromStatement[fromClass:uptoOpen]  # Substring between 'Class' and '{'
    uptoOpen = toStatement.find(';')
    fromClass = toStatement.find('import ')
    subTo = toStatement[fromClass:uptoOpen]  # Substring between 'Class' and '{'
    if (subFrom != subTo):
        return True
    return False


def isFor(fromStatement, toStatement):  # Old Loop, New Loop
    fP = fromStatement.find('for')
    bP1 = fromStatement.find('(')
    sP1 = fromStatement.find(';')
    sP2 = fromStatement.find(';')
    bP2 = fromStatement.find(')')

    fP_to = toStatement.find('for')
    bP1_to = toStatement.find('(')
    sP1_to = toStatement.find(';')
    sP2_to = toStatement.find(';')
    bP2_to = toStatement.find(')')

    if (fP >= 0 and fP < bP1 and bP1 < sP1 and sP1 < sP2 and sP2 < bP2) and (
            fP_to >= 0 and fP_to < bP1_to and bP1_to < sP1_to and sP1_to < sP2_to and sP2_to < bP2_to):
        return True
    return False


def isWhile(fromStatement, toStatement):  # Old Loop, New Loop
    fP = fromStatement.find('while')
    bP1 = fromStatement.find('(')
    bP2 = fromStatement.find(')')

    fP_to = toStatement.find('while')
    bP1_to = toStatement.find('(')
    bP2_to = toStatement.find(')')

    if (fP >= 0 and fP < bP1 and bP1 < bP2) and (fP_to >= 0 and fP_to < bP1_to and bP1_to < bP2_to):
        return True
    return False


def notComment(fromStatement, toStatement):
    fS = fromStatement.find('*')
    fSL = fromStatement.find('/')

    tS = toStatement.find('*')
    tSL = toStatement.find('/')

    flagF = flagT = True

    for i in range(1, fS):
        if fromStatement[i] != ' ':
            flagF = False
            break
    for i in range(1, fSL):
        if fromStatement[i] != ' ':
            flagF = False
            break
    for i in range(1, tS):
        if toStatement[i] != ' ':
            flagT = False
            break
    for i in range(1, tSL):
        if toStatement[i] != ' ':
            flagT = False
            break

    if flagF == True and flagT == True:
        return True
    return False


def isAnyInvalidCharacter(fromStatement):  # Return 0 if there is not invalid substring for method, 1 otherwise
    invalidCharacter = ['=', '.print', '//', '%', '""', '" "', '.']  # Method Signature Can't contain these
    validation = 0
    for j in invalidCharacter:
        if fromStatement.find(j) >= 0:
            validation = validation | 1
    return validation


dataTypes = ['void', 'int', 'double', 'float', 'String', 'boolean', 'char', 'long', 'short',
             'byte']  # Possible Datatypes a method can have


def isMethod(fromStatement, toStatement):  # Deleted Statement and Added statement are methods or not
    if isParameterAdded(fromStatement, toStatement) == True:
        #        print(fromStatement)
        #        print(toStatement)
        for i in dataTypes:
            dataTypeIn = fromStatement.find(i)  # Should have a return data type
            openingParenthesis = fromStatement.find('(')
            validation = isAnyInvalidCharacter(fromStatement)  # Has invalid character or not
            if dataTypeIn > 0 and openingParenthesis > dataTypeIn and validation == 0:  # Datatype should present, opening paranthesis after the datatype, and no invalid substring, all these ensures the method
                return True
    return False


def isClass(fromStatement, toStatement):  # To check Class modification
    if isClassAdded(fromStatement, toStatement) == True:
        return True
    return False


def isLibrary(fromStatement, toStatement):  # To check Library modification
    if isLibraryAdded(fromStatement, toStatement) == True:
        return True
    return False


def isLoop(fromStatement, toStatement):  # To check looping modification
    if isFor(fromStatement, toStatement) == True:
        return True
    elif isWhile(fromStatement, toStatement) == True:
        return True
    return False


def RepoMiner(gitName):
    WriteToCSV = []
    loopCounter = methodCounter = classCounter = libraryCounter= 0
    for commit in RepositoryMining(gitName).traverse_commits():  # For every commits
        for mod in commit.modifications:  # For every modifications
            if (mod.filename).find('.java') >= 0:  # Only for Java Files
                totalRows = len(mod.diff.splitlines())
                lines = mod.diff.splitlines()
                for rowNumber in range(totalRows):
                    if rowNumber < (totalRows - 1):
                        if len(lines[rowNumber]) > 0 and len(lines[rowNumber + 1]) > 0:
                            if lines[rowNumber][0] == '-' and lines[rowNumber + 1][0] == '+' and notComment(
                                    lines[rowNumber], lines[rowNumber + 1]):
                                if isMethod(lines[rowNumber], lines[
                                    rowNumber + 1]):  # A deletion and after that an addition of methods with parameter addition
                                    SourceCode = mod.source_code  # New Source code
                                    SourceFile = mod.filename  # File Changed
                                    Hash = commit.hash  # Commit SHA
                                    OldMethodSignature = str(lines[rowNumber])
                                    NewMethodSignature = str(lines[rowNumber + 1])
                                    upto = OldMethodSignature.find(')') + 1
                                    OldMethodSignature = OldMethodSignature[
                                                         1:upto]  # Extracting the old function Signature
                                    upto = NewMethodSignature.find(')') + 1
                                    NewMethodSignature = NewMethodSignature[
                                                         1:upto]  # Extracting the new function signature
                                    WriteToCSV.append([Hash, SourceFile, OldMethodSignature,
                                                       NewMethodSignature])  # Ready for report printing
                                    methodCounter = methodCounter + 1
                                elif isClass(lines[rowNumber], lines[
                                    rowNumber + 1]):  # A deletion and after that an addition of Class with parameter addition
                                    SourceCode = mod.source_code  # New Source code
                                    SourceFile = mod.filename  # File Changed
                                    Hash = commit.hash  # Commit SHA
                                    OldClass = str(lines[rowNumber])
                                    NewClass = str(lines[rowNumber + 1])
                                    WriteToCSV.append(
                                        [Hash, SourceFile, OldClass[1:], NewClass[1:]])  # Ready for report printing
                                    classCounter = classCounter + 1
                                elif isLibrary(lines[rowNumber], lines[
                                    rowNumber + 1]):  # A deletion and after that an addition of Library with parameter addition
                                    SourceCode = mod.source_code  # New Source code
                                    SourceFile = mod.filename  # File Changed
                                    Hash = commit.hash  # Commit SHA
                                    OldLibrary = str(lines[rowNumber])
                                    NewLibrary = str(lines[rowNumber + 1])
                                    WriteToCSV.append(
                                        [Hash, SourceFile, OldLibrary[1:], NewLibrary[1:]])  # Ready for report printing
                                    libraryCounter = libraryCounter + 1
                                elif isLoop(lines[rowNumber], lines[
                                    rowNumber + 1]):  # A deletion and after that an addition of Library with parameter addition
                                    SourceCode = mod.source_code  # New Source code
                                    SourceFile = mod.filename  # File Changed
                                    Hash = commit.hash  # Commit SHA
                                    OldLoop = str(lines[rowNumber])
                                    NewLoop = str(lines[rowNumber + 1])
                                    WriteToCSV.append(
                                        [Hash, SourceFile, OldLoop[1:], NewLoop[1:]])  # Ready for report printing
                                    loopCounter = loopCounter + 1
    WriteToCSV.append([methodCounter, classCounter, libraryCounter, loopCounter])
    return WriteToCSV


if __name__ == "__main__":
    GitFileName = input("Enter the git name with path: ")  # Repository name with Path
    GitResultFile = input("Result File Name: ") # Name for result file
    Result = RepoMiner(GitFileName)  # Finds the Result
    WriteReport(Result, GitResultFile)  # Print to CSV
    print("\nOutput printed successfully...")
