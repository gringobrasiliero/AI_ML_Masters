Critical Thinking 4 

Overview:
	- This program allows you to constuct an 8-puzzle for the program to solve. 
	- You will define what the initial puzzle will look like, as well as the final puzzle. 
	- The Program will then display the amount of Moves it took to solve the puzzle, and show you the steps taken to solve it.


Instructions:

1) Open CMD to the Directory where CriticalThinking4.py exists on your Computer.

2) Execute command "python CriticalThinking4.py" in the CMD Window.

3) Construct the 3 rows of the Initial State of the 8-puzzle by typing 3 characters at a time and then pressing enter.
	- One of the 9 characters you insert for the three rows must include an Underscore.

	HINT: Below are three initial puzzles that you can use for testing.
	
	Example 1:
		
		4 1 2
		7 _ 3
		8 5 6

	Example 2:
		
		_ 1 2
		4 5 3
		7 8 6
	
	Example 3:
		1 _ 3
		4 2 6
		7 5 8
		
		


4) Constuct the order of the 9 characters you placed for the initial into what the final solution should be.
	- You must use the same characters that you used to construct the inital puzzles state.
	
	HINT:
		- I recommend ordering the numbers from least to greatest, with the Underscore being the last block:
		
		1 2 3
		4 5 6 
		7 8 _

5) Program will calculate a best route to solve the 8-puzzle, showing you the steps made, and the final solution.
