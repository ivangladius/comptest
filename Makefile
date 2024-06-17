
COMPTEST = comptest
INPUTFILE = input_file
NAME = sol

all: $(NAME).cpp
	@g++ -g -o $(NAME) $(NAME).cpp
	@$(COMPTEST) $(PWD) $(NAME) $(INPUTFILE)
	
