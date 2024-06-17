
COMPTEST = comptest
TESTFILE = test-file
NAME = sol

all: $(NAME).cpp
	@g++ -g -o $(NAME) $(NAME).cpp
	@$(COMPTEST) $(PWD) $(NAME) $(TESTFILE)
	
