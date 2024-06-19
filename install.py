
#!/usr/bin/env python3

import os
import sys
import subprocess

usage_string = """
usage: python3 install.sh <install-path>
"""

def get_cpp_template():
  with open("template_cpp", "r") as t:
   return t.read()

# generate bash function to create a comp prog dir with Makefile 
template_content = get_cpp_template()
gen_func = f'''
COMPTEST_PATH={os.getenv("PWD")}
TEMPLATE_CONTENT="{get_cpp_template()}"
generate_compdir() {{
  mkdir "$1"
  cp "$COMPTEST_PATH"/Makefile "$1"/Makefile
  touch "$1"/input_file
  touch "$1"/expected_file
  echo "$TEMPLATE_CONTENT" > "$1"/sol.cpp
}}
alias compgen='generate_compdir'
'''

home_prefix = os.getenv("HOME")
sh_configs = [f"{home_prefix}/.zshrc", 
              f"{home_prefix}/.bashrc"]

    
compgen_script = ".compgen.sh"




def append_to_shell_configs(source_command):
  for config in sh_configs:
    with open(config, "r+") as c:
      content = c.read()
      if source_command not in content:
        c.write(source_command)

def install_at(install_path):
  try:
    pwd = os.getenv("PWD")
    subprocess.run(["sudo", "ln", "-sf", f"{pwd}/comptest.py", f"{install_path}/comptest"],
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
  install_at(install_path)

  source_command = f"source {home_prefix}/{compgen_script}\n"
  append_to_shell_configs(source_command)

  with open(f"{home_prefix}/{compgen_script}", "w") as gen:
    gen.write(gen_func)


if __name__ == "__main__":
  main()
