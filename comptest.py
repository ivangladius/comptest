#!/usr/bin/env python3

import subprocess
import sys
from pathlib import Path

def usage():
    usage_string = """
    usage: ./comptest <directory> <executable> <testcases>
  """
    print(usage_string)


def main():
    if len(sys.argv) != 4:
        usage()
        exit(0)

    cwd = Path(sys.argv[1])
    executable = cwd / sys.argv[2]
    testfile = cwd / sys.argv[3]
    # print(cwd)
    #print(f"exe: {executable}")
    # print(testfile)

    # read all test cases from testfile
    # test cases are seperated by a empty line
    test_cases = []
    with open (testfile, "r") as tf:
        test = ""
        for line in tf:
            if line.isspace():
                test_cases.append(test)
                test = ""
            test += line.lstrip()

    #print(test_cases)

    # now test each testcase with the executable and stdout
    for test in test_cases:
        try:
            output = subprocess.check_output([executable],
                                              input=test,
                                              stderr=subprocess.STDOUT,
                                              text=True)
            print(output)
        except subprocess.CalledProcessError as e:
            print(e.output)

if __name__ == "__main__":
    main()
