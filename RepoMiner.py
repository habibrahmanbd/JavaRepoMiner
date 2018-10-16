#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 15 19:23:02 2018

@author: Habibur Rahman
@email: habib[dot]rahman[at]uits[dot]edu[dot]bd
"""

from pydriller import RepositoryMining

for commit in RepositoryMining('../JavaTestingRepo').traverse_commits():
#    print(commit.hash)
#    print(commit.author.name)
#    print(commit.author_date)
#
    for mod in commit.modifications:
#        print(mod.filename)
#        print((mod.filename).find('java')>0)
        if (mod.filename).find('java')>0:
            print(mod.filename + " is changed!")
            for row in mod.diff.splitlines():
                if row[0]== '-'  or  row[0]== '+':
                    print(row)
