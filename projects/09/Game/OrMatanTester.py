# v1.1, added sending directories as arguments (mattan)

#############################################################################
# ONLY HERE A CHANGE IS NEEDED (MAYBE):

# the path to the tests directory (containing all subdirectories):


# This file needs to be the main file, the one that i can call from the
# terminal as: $ python3 my_main.py some_dir
# Please change it if it is not the case:
mainFileName = "JackAnalyzer.py"

tests_address = "tests"
printAll = True
send_directories_as_argument = False

# Notice: if you think something is wrong with your code or the tester
# (like infinite loop), the unComment the next line to get some more info
# printAll = True

#############################################################################
import os
import re
from subprocess import *


pattern = re.compile(r'\s+')

def syscmd(cmd, encoding=''):
    """
    Runs a command on the system, waits for the command to finish, and then
    returns the text output of the command. If the command produces no text
    output, the command's return code will be returned instead.
    """
    p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT,
        close_fds=True)
    p.wait(3)
    output = p.stdout.read()
    if len(output) > 1:
        if encoding: return output.decode(encoding)
        else: return output
    return p.returncode


def diff(f1, f2):
    try:
        ff1 = open(f1)
        fr1 = re.sub(pattern, '', ff1.read())
        ff2 = open(f2)
        fr2 = re.sub(pattern, '', ff2.read())
        return fr1 != fr2
    except FileNotFoundError:
        print(f"+++++++++++++++++++++++++++++++ERROR+++++++++++++++++++++++++++++++++++++++++++")
        print(f"Your code Failed to create the file {f1}")
        print("please make sure that the 'tests_address' and the 'mainFileName' vars in the tester are set correctly")
        print(f"+++++++++++++++++++++++++++++++ERROR+++++++++++++++++++++++++++++++++++++++++++")
        return True

def getFileList(path):
    res = []
    for filename in os.listdir(path):
        if filename.endswith(".jack"):
            res.append(os.path.join(path, filename))
        else:
            continue
    return res


def test():
    fails = 0
    total = 0

    # delete old outputs
    for folder in os.listdir(tests_address):
        if os.path.isdir(os.path.join(tests_address, folder)):
            for file_name in os.listdir(os.path.join(tests_address, folder)):
                if file_name.endswith('.xml'):
                    os.remove(os.path.join(tests_address, folder, file_name))

    for curDir in os.listdir(tests_address):
        if curDir[0] == ".":
            continue
        curDir = os.path.join(tests_address, curDir)
        files = [curDir]
        if os.path.isdir(curDir):
            files = getFileList(curDir)
        # print files
        if not send_directories_as_argument:
            fails, total = go_over_files(fails, files, total)
        else:
            fails, total = go_over_folders(fails, files, total, curDir)

    print("=" * 40 + "\n")
    if fails:
        fails = str(fails)
        total = str(total)
        print("\t\tFailed " + fails + " out of " + total + " tests.\n")
    else:
        print("\t\t\tPassed All Tests!\n")
    print("=" * 40 + "\n")


def go_over_files(fails, files, total):
    for curFile in files:
        filepassed = True
        curFile = curFile
        total += 1
        if printAll:
            print(f"Running your code on {curFile}...")
        syscmd(f"python3 {mainFileName} {curFile}")
        syscmd("py " + mainFileName + " " + curFile)
        syscmd("python " + mainFileName + " " + curFile)
        testname = curFile.split(".")[0]
        if printAll:
            print("Checking for diff between " + testname + ".xml and " +
                  testname + ".xml.cmp" + "...")
        if testname.split(os.path.sep)[-1] and diff(testname + ".xml",
                                                    testname
                                                    + ".xml.cmp"):
            fails += 1
            filepassed = False
            print("[X] Failed on " + testname + ".jack")

        if filepassed:
            print("[V] Passed " + testname + ".jack")
        print("=" * 100)
    return fails, total


def go_over_folders(fails, files, total, curDir):
    if printAll:
        print(f"{'*'*50}Running your code on " + curDir + f"...{'*'*50}")
        print("=" * 100)
    syscmd("python3 " + mainFileName + " " + curDir)
    syscmd("py " + mainFileName + " " + curDir)
    syscmd("python " + mainFileName + " " + curDir)
    for curFile in files:
        filepassed = True
        curFile = curFile
        total += 1
        testname = curFile.split(".")[0]
        if printAll:
            print("Checking for diff between " + testname + ".xml and " +
                  testname + ".xml.cmp" + "...")
        if testname.split(os.path.sep)[-1] and diff(testname + ".xml",
                                                    testname
                                                    + ".xml.cmp"):
            fails += 1
            filepassed = False
            print("[X] Failed on " + testname + ".jack")
        if filepassed:
            print("[V] Passed " + testname + ".jack")
        print("=" * 100)
    return fails, total


if __name__ == '__main__':

    test()

