
#!/usr/bin/env python3

import os
import sys
import subprocess

usage_string = """
usage: python3 install.sh <install-path>
"""


# generate bash function to create a comp prog dir with Makefile 
gen_func = f'''
COMPTEST_PATH={os.getenv("PWD")}
generate_compdir() {{
  mkdir "$1"
  cp "$COMPTEST_PATH"/Makefile "$1"/Makefile
  touch "$1"/testfile
}}
alias compgen='generate_compdir'
'''

home_prefix = os.getenv("HOME")
sh_configs = [f"{home_prefix}/.zshrc", 
              f"{home_prefix}/.bashrc"]

    
compgen_script = ".compgen.sh"

source_command = f"source {os.getenv("HOME")}/{compgen_script}\n"

def write_to_shell_configs():
  for config in sh_configs:
    with open(config, "r+") as c:
      content = c.read()
      if source_command not in content:
        c.write(source_command)

def link_exe_to_PATH(install_path):
  try:
    subprocess.run(["sudo", "ln", "-sf", f"{os.getenv("PWD")}/comptest.py", f"{install_path}/comptest"],
                    stdout=None, 
                    stdin=None,
                    stderr=subprocess.STDOUT,
                    text=True)  
  except subprocess.SubprocessError as e:
    print(e)



def main():
  if len(sys.argv) != 2:
    print(usage_string)
    exit(1)

  install_path = sys.argv[1]
  link_exe_to_PATH(install_path)
  write_to_shell_configs()

  with open(f"{compgen_script}", "w") as gen:
    gen.writelines(gen_func)


if __name__ == "__main__":
  main()
