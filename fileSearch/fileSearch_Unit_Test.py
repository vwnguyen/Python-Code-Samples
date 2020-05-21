#!/usr/bin/python

# -------------------------------------------------------------------------------

# fileSearch_Unit_Test.py - stand-alone script, tests functionality of the 
# testInput and recursiveSearch methods from fileSearch.py Features 2 tests:
# test_testInput_Invalid_Inputs: evaluates unusable inputs for the cases: 
# 1) test input <= 1
# 2) test input >= 3
# 3) test input with invalid directory
# 
# test_recursiveSearch: generates a directory architecture and tests 1 -> testMax
# pseudorandom combinations of targetfiles and junkfiles. After testing, the 
# testing directories are cleaned up. 
# 
# DIRECTORY ARCHITECTURE: a->b->c->d-> . . .  -> z
# 
# Test Cases:
# 1) root_dir has no files with 'keyword'
# 2) 1 -> testMax combinations of files with targetfiles and junkfiles 
# -------------------------------------------------------------------------------

import unittest
import FileSearch
import shutil
import os

# generate random integer values
from random import seed
from random import randint


class TestFileSearchMethods(unittest.TestCase):
    
    
    def test_testInput_Invalid_Inputs(self):
        print("\n")
        print("-------------------------------------------------------------------------------")
        print("TESTING INVALID INPUTS")
        print("-------------------------------------------------------------------------------")
        print("testing input sizes <= 1")
        # input size <= 1 
        self.assertEqual(FileSearch.testInput(''), False)
        self.assertEqual(FileSearch.testInput('foo'), False)
        print("-------------------------------------------------------------------------------")
        print("testing input sizes >= 2")
        # input size >= 3
        self.assertEqual(FileSearch.testInput('foo bar'),False)
        self.assertEqual(FileSearch.testInput('foo bar foxtrot'), False)
        self.assertEqual(FileSearch.testInput('foo bar foxtrot foo bar foxtrot foo bar foxtrot'), False)
        print("-------------------------------------------------------------------------------")
        print("testing input size == 3")
        # input size = 3, i.e. filename root_dir keyword usage is correct, but root_dir path not a directory
        self.assertEqual(FileSearch.testInput('filename Definitely_An_Invalid_Directory keyword'), False)



    def test_recursiveSearch(self):
        testMax = 20
        print("\n")
        print("-------------------------------------------------------------------------------")
        print("TESTING RECURSIVESEARCH")
        cwd = os.getcwd()
        dir_list = os.listdir(cwd)  
        print("List of directories and files before creation:") 
        print(dir_list) 
        print() 
        # create all directories and subdirs recursively
        subDirs = "/a/b/c/d/e/f/g/h/i/j/k/l/m/n/o/p/q/r/s/t/u/v/w/x/y/z"
        os.makedirs(cwd+subDirs, exist_ok=True)
        print("List of directories and files after creation:") 
        dir_list = os.listdir(cwd)  
        print(dir_list) 
        print() 
        print("-------------------------------------------------------------------------------")
        print("TESTING EMPTY DIRECTORY")
        pathDictionary = dict()
        keyword = 'target'
        root_dir = os.path.join(cwd,'a')
             
        print("root_dir: " + root_dir)
        print("keyword: " + keyword)
        
        # 1) root_dir and subdir(s) have no files with keyword        
        FileSearch.recursiveSearch(pathDictionary,keyword,root_dir)
        print(pathDictionary)
        self.assertEqual(sum(pathDictionary.values()),0)
        print("-------------------------------------------------------------------------------")
        print("TESTING SEARCH WITH RANDOM FILE ADDITIONS")
        
        # test recursiveSearch in a for loop. Different seed generates new directory file layouts
        for testCount in range(0,testMax):
        
            shutil.rmtree(root_dir)
            subDirs = "/a/b/c/d/e/f/g/h/i/j/k/l/m/n/o/p/q/r/s/t/u/v/w/x/y/z"
            os.makedirs(cwd+subDirs, exist_ok=True)
            seed(testCount)
            pathDictionary = dict()
            totalTargetFiles = 0
            totalDummyFiles = 0
            answerDictionary = dict()
            # add files randomly to root_dir for testing
            for dirpath, dirnames, files in os.walk(root_dir):
                targetFiles = 0
                for dir in dirnames:
                    dummyFiles = randint(0, testMax)
                    targetFiles = randint(0, testMax)
                    totalTargetFiles = totalTargetFiles + targetFiles
                    totalDummyFiles = totalDummyFiles + dummyFiles
                    subDir = (os.path.join(dirpath,dir))
                    for i in range (0,targetFiles):
                        targetString = "targetFile{}.{}".format(i,keyword) 
                        with open(subDir + targetString,'w') as fp:
                            pass
                    for j in range (0,dummyFiles):
                        dummyString = "dummyFile{}.junk".format( j ) 
                        with open(subDir + dummyString,'w') as fp:
                            pass
                answerDictionary.update({dirpath:targetFiles})
            
            cwd = os.getcwd()
            dir_list = os.listdir(cwd)
            FileSearch.recursiveSearch(pathDictionary,keyword,root_dir)        
            print("total files to find: " + str(totalTargetFiles))
            print("total TargetFiles Found = "  + str(sum(pathDictionary.values())))
            accuracy = sum(pathDictionary.values()) / totalTargetFiles
            print("file count accuracy = " + str(accuracy*100) )
            print("answerDictionary == pathDictionary? " + str(pathDictionary == answerDictionary))
            # pathDictionary and answerDictionary check
            self.assertEqual(sum(pathDictionary.values()),totalTargetFiles)
            self.assertEqual(pathDictionary == answerDictionary,True)

        # clean up all directories and subdirs
        print("recursiveSearch passed " + str(testCount) + " search test configurations") 
        shutil.rmtree(root_dir)
        
suite = unittest.TestLoader().loadTestsFromTestCase(TestFileSearchMethods)
unittest.TextTestRunner(verbosity=2).run(suite)