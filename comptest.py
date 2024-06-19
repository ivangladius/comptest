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
    # ANSI color codes for green and red
    GREEN = '\033[92m'
    RED = '\033[91m'
    RESET = '\033[0m'
    
    try:
        # Read the files and remove only newlines
        with open(file1, 'r') as f1, open(file2, 'r') as f2:
            content1 = ''.join(line.strip('\n') for line in f1)
            content2 = ''.join(line.strip('\n') for line in f2)

        # Compare the content
        if content1 == content2:
            print(f"{GREEN}Pass{RESET}")
        else:
            print(f"{RED}Fail{RESET}")
            # Optional: Show differences
            for i, (c1, c2) in enumerate(zip(content1, content2)):
                if c1 != c2:
                    print(f"Difference at character {i}: '{c1}' vs '{c2}'")
            print(f"Content of file1: {content1}")
            print(f"Content of file2: {content2}")

    except FileNotFoundError as e:
        print(f"{RED}Error: {e}{RESET}")
    except Exception as e:
        print(f"{RED}An unexpected error occurred: {e}{RESET}")


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
