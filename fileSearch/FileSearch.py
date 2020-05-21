#!/usr/bin/python

# -------------------------------------------------------------------------------

# FileSearch.py - stand-alone script that recursively searches a 'root_dir' for 
# all files with the string 'keyword' in it using os.walk. Returns a dictionary
# data structure with directory names and file counts as well as a bar graph 
# created using the matplotlib module. Prints to stdout and FileSearch.log.

# Argument Inputs: 
    # - root_dir: File path to the directory to recursively search in. 
    # - keyword: String to search for in root_dir and its subdirectories.   

# Outputs: 
    # - Data Structure Containing all directories and file counts:
    # - An output graph with a plot with X-axis as subdir name string, Y-axis as 
    # count values. 
    
    # NOTE: output bar graph does not include directories with 0 
    # file counts to remove sparsity.

# -------------------------------------------------------------------------------

# Import necessary modules

import sys, getopt
import matplotlib.pyplot as plt
import numpy
import os
 
# graphResults(pathDictionary,keyword,root_dir)
# Desc: Graphs the results of the recursiveSearch using matplotlib
# Inputs: 
# - pathDictionary: ditionary data structure with 
#   keys = directory names
#   values = file counts with "keyword" in them
# - keyword: String to search for in root_dir and its subdirectories
# - root_dir: File path to the directory to recursively search in. 
# Preconditions: recursiveSearch() called beforehand. 
# Postconditions: Output Graph with X-axis as directory names and Y-axis as file 
# counts

def graphResults(pathDictionary,keyword,root_dir):

    # uncomment to plot every directory 
    # x = numpy.arange(len(pathDictionary))
    # plt.figure(figsize=(20, 3))  # width:20, height:3
    # plt.bar(range(len(pathDictionary)), pathDictionary.values(), align='center', width=0.3)
    # plt.xticks(x,pathDictionary.keys())
    
    # uncomment to plot nonempty directories
    newDict = dict(filter(lambda elem: elem[1] > 0, pathDictionary.items()))
    x = numpy.arange(len(newDict))
    plt.figure(figsize=(20, 4))  # width:20, height:3
    plt.bar(range(len(newDict)),newDict.values(), align='center', width=0.3)
    plt.xticks(x,newDict.keys())

    
    plt.xlabel('Directory Names')
    plt.ylabel('File Count')
    plt.title("Search Results for: " + keyword + " in " + root_dir)
    plt.show()

# writeToFile(pathDictionary,keyword,root_dir)
# Desc: writes the results of the recursiveSearch using matplotlib
# Inputs: 
# - logname: string of filename to write 
# - pathDictionary: ditionary data structure with 
#   keys = directory names
#   values = file counts with "keyword" in them
# - keyword: String to search for in root_dir and its subdirectories
# - root_dir: File path to the directory to recursively search in. 
# Preconditions: recursiveSearch() called beforehand. 
# Postconditions: logname will have the results of recursiveSearch
    
def writeToFile(logname,pathDictionary,keyword,root_dir):
    file = open(logname,"w")
    file.write("Output Dictionary\n")
    file.write(str(pathDictionary) + "\n")
    file.write("directory names: " + str(pathDictionary.keys()) + "\n")
    file.write("directory counts: " + str(pathDictionary.values()) + "\n")
    file.close()
    
    
# recursiveSearch(pathDictionary,keyword,root_dir)
# Desc: writes the results of the recursiveSearch using matplotlib
# Inputs: 
# - pathDictionary: ditionary data structure with (empty)
#   keys = directory names
#   values = file counts with "keyword" in them
# - keyword: String to search for in root_dir and its subdirectories
# - root_dir: File path to the directory to recursively search in. 
# Preconditions: root_dir is a valid directory path, pathDictionary is empty
# Postconditions: pathDictionary 

def recursiveSearch(pathDictionary,keyword,root_dir):

    for dirpath, dirnames, files in os.walk(root_dir):
        count = 0
        for name in files:
            # str = name
            foundFlag = name.find(keyword)
            if foundFlag != -1:
                count = count + 1
        pathDictionary.update({dirpath:count})



# recursiveSearch(pathDictionary,keyword,root_dir)
# Desc: writes the results of the recursiveSearch using matplotlib
# Inputs: 
# - argList: string containing system arguments from command line
# Preconditions: argList is a string containing arguments from cmdline
# Postconditions: boolean, True = Valid Input, False = Invalid Input

def testInput(argList):
    # Test for the following Format
    # sys.argv[0] = File Name
    # sys.argv[1] = root_dir
    # sys.argv[2] = keyword 

    if len(argList) != 3:
        print ('Usage: <root_dir> <keyword>')
        print ('Error: Number of arguments != 3')
        # normally would sys.exit(1), returns false for testing purposes
        return False
    if  os.path.isdir(argList[1]) == False:
        print ('Usage: <root_dir> <keyword>')
        print ("Error: root_dir: " + argList[1] + " - does not exist.")
        print ("Check to see if: directory exists, syntax error(s) or for spaces in file path")
        return False
    return True


def main(argv):    
    # Initial variable settings
    logname = 'fileSearch.log'
    pathDictionary = dict()
    argList = sys.argv
    # If input areuments are invalid, exit with error
    if testInput(argList) == False:
        sys.exit(1)
    else:
        # all error cases handled, perform nominal execution 
        root_dir = sys.argv[1]
        keyword = sys.argv[2]
        # PERFORM THE RECURSIVE SEARCH
        recursiveSearch(pathDictionary,keyword,root_dir)
        print(pathDictionary)
        writeToFile(logname,pathDictionary,keyword,root_dir)
        graphResults(pathDictionary,keyword,root_dir)
        
    
if __name__ == "__main__":
    main(sys.argv[1:])