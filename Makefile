
COMPTEST = comptest
TESTFILE = testfile
NAME = sol

all: $(NAME).cpp
	@g++ -g -o $(NAME) $(NAME).cpp
	@$(COMPTEST) $(PWD) $(NAME) testfile
	
