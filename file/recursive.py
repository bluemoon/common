from collections import deque
import os


def rmDirectoryRecursive(path):
    ''' Recursively remove a directory '''
    for i in os.listdir(path):
        fullPath = path + "/" + i
        if os.path.isdir(fullPath):
            ## Recursively delete
            rmDirectoryRecursive(fullPath)
        

    ## Finally delete the parent
    os.rmdir(path)