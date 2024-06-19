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
        # Read files and remove only newlines
        with open(file1, 'r') as f1, open(file2, 'r') as f2:
            lines1 = [''.join(line.rstrip('\n')) for line in f1 if line.rstrip('\n') != '']
            lines2 = [''.join(line.rstrip('\n')) for line in f2 if line.rstrip('\n') != '']

        # Compare line by line
        differences = []
        for i, (line1, line2) in enumerate(zip(lines1, lines2)):
            if line1 != line2:
                differences.append((i + 1, line1, line2))

        # Check for extra lines only if differences are found or lengths differ
        if differences or len(lines1) != len(lines2):
            print(f"{RED}Fail{RESET}")
            print("Differences:")
            for diff in differences:
                print(f"Line {diff[0]} differs:")
                print(f"    Output: {RED}{repr(diff[1])}{RESET}")
                print(f"    Expected: {GREEN}{repr(diff[2])}{RESET}")

            # If one file has more lines than the other
            if len(lines1) > len(lines2):
                print(f"Additional lines in output_file:")
                for i in range(len(lines2), len(lines1)):
                    print(f"    Line {len(lines2) + i + 1}: {RED}{repr(lines1[len(lines2) + i])}{RESET}")
            elif len(lines2) > len(lines1):
                print(f"Additional lines in expected_file:")
                for i in range(len(lines1), len(lines2)):
                    print(f"    Line {len(lines1) + i + 1}: {GREEN}{repr(lines2[len(lines1) + i])}{RESET}")
        else:
            print(f"{GREEN}Pass{RESET}")

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
