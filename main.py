import sys
from program import start_program  # Importing the 'start_program' function from the 'program' module

# Prompting the user for input on whether they want to start the program
choice = input("\n\nWould you like to start this program? (Y/N): ").lower()

# Checking if the user entered 'Y' or 'yes' to start the program
if choice in ["y", "yes"]:
    start_program()  # Calling the function to start the program

# If the user entered 'N' or 'no', exit the program with a message
elif choice in ["n", "no"]:
    sys.exit("Exiting program...")  # Gracefully exiting the program
