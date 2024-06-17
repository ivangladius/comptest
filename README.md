
# Competetive Programming Tool
## Create and Test very efficient Competetive Programming environments 
### installation: 
```
https://github.com/ivangladius/comptest.git
cd comptest
python3 install.py /usr/local/bin
```
source your shell script: 
```
  source ~/.zshrc
```
or 
```
  source ~/.bashrc
```
### usage 
```
compgen mydir
cd mydir
```
directory structure:
```
├── Makefile
├── expected_file
├── input_file
└── sol.cpp
```

### input_file 
#### the input for your problem, paste it into the file
```
8 5
10 9 8 7 7 7 5 5
```
### expected_file 
#### the expected output for your problem, paste it into the file
```
8 2
```
### testing
```
make
```
if it passes, green text: 
```
pass!
```
if it fails, red text: 
```
fail!
```
