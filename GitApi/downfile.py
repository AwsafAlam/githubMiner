import os
from git import Repo
import shutil
import tempfile


'''
    For the given path, get the List of all files in the directory tree 
'''
def getListOfFiles(dirName):
    # create a list of file and sub directories 
    # names in the given directory 
    listOfFile = os.listdir(dirName)
    allFiles = list()
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        # If entry is a directory then get the list of files in this directory 
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfFiles(fullPath)
        else:
            allFiles.append(fullPath)
                
    return allFiles


# Create temporary dir
t = tempfile.mkdtemp()
# Clone into temporary dir
Repo.clone_from('https://github.com/AwsafAlam/Datastructures-Algorithms.git', t, branch='master', depth=1)
# Copy desired file from temporary dir
# print(os.path.dirname(t))
# print(os.listdir(t))

print(getListOfFiles(t))

shutil.move(os.path.join(t, 'DataStructures/'), '.')
# shutil.copytree(os.path.join(t, ''), '~/Desktop/gitCrawler/', symlinks=False, ignore=None, ignore_dangling_symlinks=False)
# Remove temporary dir
shutil.rmtree(t)
