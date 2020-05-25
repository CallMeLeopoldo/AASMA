FULLHOUSE PROJECT EXECUTING INSTRUCTIONS

To run the program on Command Line with Standard Agent Profiles:
table.py
<number of Game Rounds> <number of Agents> <value of Big Blind> <number of start chips>

To run the program on Command Line with personalized Agent Profiles:
table.py
<number of Game Rounds> <number of Agents> <value of Big Blind> <number of start chips> <profileNumber 1>,<profileNumber 2>,...,<profileNumber k>

The programs waits for user input to progress. User must press key "1" when prompted.

IMPORTANT:
all numbers must be int 
K must be equal to the number of Agents. Inputing more or less profiles than the given number of Agents will result in error and the program will not launch

MUST HAVE INSTALLED THE FOLLOWING LIBRARIES:
itertools
keyboard
copy

PROFILE GUIDE:
1 = "Risky"
2 = "Safe"
3 = "Dummy"
4 = "Balanced"
5 = "Copycat"

Standard Agent Profiles only choose profiles randomly.