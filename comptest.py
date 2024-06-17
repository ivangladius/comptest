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
    # read all test cases from testfile
    # test cases are seperated by a empty line
    test_cases = []
    with open (testfile, "r") as tf:
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

    result = subprocess.run(["diff", "-B", "-w", "output_file", "input_file"],
                             capture_output=True,
                             text=True)
    if result.returncode != 0:
        print("\033[31mfailed!\033[0m")
    else:
        print("\033[32mPass!\033[0m")

if __name__ == "__main__":
    main()
