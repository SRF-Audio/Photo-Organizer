import os
import sys
import re

# This is a function that recursively searches a directory for files that match a regular expression pattern.
# It returns a list of files that match the pattern of my duplicate file names, and then deletes them.

def fileCollector(files, pattern):
    file_list = []
    for file in files:
        # print("The current file is: " + file +
        #       ", and the bool test for file shows: " + str(os.path.isfile(file)))
        if os.path.isfile(file) and pattern.search(file):
            # print("The data type of the regex pattern match is: " +
            #       str(type(pattern.search(file))))
            # print("I matched the pattern")
            file_list.append(str(os.getcwd()) + "/" + file)
            # print(file)
        elif os.path.isdir(file):
            os.chdir(file)
            # print(os.getcwd())
            file_list += fileCollector(os.listdir(), pattern)
            os.chdir("..")
    return file_list


print(sys.getrecursionlimit())
sys.setrecursionlimit(5000)
path = "/Volumes/Storage Drive/Known Good Photos"
pattern = re.compile('(?:[(][a-z][)][.](?:[a-zA-Z]{3}))')
files = []

os.chdir(path)

files = fileCollector(os.listdir(), pattern)

for file in files:
    print("Deleting: " + file)
    os.remove(file)

if __name__ == "__main__":
    main(
        duplicate_files = fileCollector(files, pattern)
        for file in duplicate_files:
            print(file)
    )
