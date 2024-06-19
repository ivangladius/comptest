#!/usr/bin/env python3

import subprocess
import sys
from pathlib import Path

def usage():
    usage_string = """
    usage: ./comptest <directory> <executable> <input_file>
  """
    print(usage_string)

def remove_newlines_and_compare(file1, file2):
    # Read the files and remove newlines
    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        content1 = f1.read().replace('\n', '')
        content2 = f2.read().replace('\n', '')

    # Compare the content
    if content1 == content2:
            print(result.stdout)
            print("\033[31mfailed!\033[0m")
    else:
            print("\033[32mPass!\033[0m")



def main():
    if len(sys.argv) != 4:
        usage()
        exit(0)

    cwd = Path(sys.argv[1])
    executable = cwd / sys.argv[2]
    inputfile = cwd / sys.argv[3]
    # read all test cases from testfile
    # test cases are seperated by a empty line
    test_cases = []
    with open (inputfile, "r") as tf:
        test = ""
        last_line_was_space = False
        for line in tf:
            if line.isspace():
                if not last_line_was_space:
                    test_cases.append(test)
                    test = ""
                    last_line_was_space = True
                continue
            test += line.lstrip()
            last_line_was_space = False
        if not test.isspace():
            test_cases.append(test)


    # now test each testcase with the executable and stdout
    buffer = ""
    for test in test_cases:
        try:
            output = subprocess.check_output([executable],
                                              input=test,
                                              stderr=subprocess.STDOUT,
                                              text=True)

            buffer += output + "\n"
        except subprocess.CalledProcessError as e:
            print(e.output)

    with open("output_file", "w") as out:
        out.write(buffer)

    remove_newlines_and_compare("expected_file", "output_file")


if __name__ == "__main__":
    main()
