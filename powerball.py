#powerball.py
#Justin MacIntosh

import operator
import random

#GLOBALS
POWERBALL_NUMBER = 6 #Powerball is the 6th number
NON_POWERBALL_MAX = 69
POWERBALL_MAX = 26

#HELPER FUNCTIONS
#Increment dictionary value
#If value not found, then set the value to 1
def increment_include(dict, key):
	if (key in dict):
		dict[key] += 1
	else:
		dict[key] = 1

#User Input Branching
def ask_for_number(current_num, numbers_picked):
	number_chosen = 0
	if (current_num < POWERBALL_NUMBER): #Non-Powerball
		if (current_num == 1):
			number_chosen = int(input("Enter Number #" + str(current_num) + "(1-69): "))
		else:
			number_chosen = int(input("Enter Number #" + 
					str(current_num) + "(1-" + str(NON_POWERBALL_MAX) + ") excluding [" + 
					', '.join(str(num) for num in numbers_picked) + "]: "))
	else: #Powerball
		number_chosen = int(input("Enter Powerball Number(1-" + str(POWERBALL_MAX) + "): "))
	return number_chosen

#Choose max value of a dictionary
def choose_max_value(cur_num, dict, powerball):
	max_key = ""
	max_value = -1
	tied = False
	for key, value in dict.items():
		if (value > max_value):
			max_key = key
			max_value = value
			tied = False
		elif (value == max_value):
			tied = True
	
	if not tied: #Parse prefixed dict key
		return max_key.replace(cur_num + "-", "")
	else: #When tied, return a random number based on if it's powerball or not
		if(powerball):
			return str(random.randint(1, POWERBALL_MAX))
		else:
			return str(random.randint(1, NON_POWERBALL_MAX))

#MAIN METHOD
powerball_dict = {}
number_dict = {}

while (True):
	#User input for giving a name
	status = ""
	while (status != "y" and status != "n"):
		status = input("Enter a name? (y/n): ")
	if (status == 'n'):
		break
	user_firstname = input("Enter the user's first name: ")
	user_lastname  = input("Enter the user's last name: ")
	
	#Main while loop
	current_num = 1
	numbers_picked = []
	while (current_num < POWERBALL_NUMBER+1):
		while (True):
			#Try/Except in case user gives a non-integer value
			try:
				number_chosen = ask_for_number(current_num, numbers_picked)
			except ValueError:
				print("ERROR: Invalid Number")
				continue
				
			if (current_num < POWERBALL_NUMBER): #Non-Powerball
				if(number_chosen > 0 and number_chosen < NON_POWERBALL_MAX+1 and not (number_chosen in numbers_picked)):
					numbers_picked.append(number_chosen)
					#number_dict includes values prefixed based on their position (i.e. 1-47, 4-28)
					dict_key = str(current_num) + "-" + str(number_chosen)
					increment_include(number_dict, dict_key)
					break
				else:
					print("ERROR: Value Not In Range OR Value Already Selected")
			else: #Powerball
				if(number_chosen > 0 and number_chosen < POWERBALL_MAX+1):
					numbers_picked.append(number_chosen)
					#Powerball is enetered into the number_dict with a P- prefix (i.e. P-34, P-4)
					dict_key = "P-" + str(number_chosen)
					increment_include(number_dict, dict_key)
					break
				else:
					print("ERROR: Value not in range")
		current_num += 1
		
	#powerball_dict is a simple user->choices dict that allows easy output of user's favorites later
	powerball_dict[user_firstname + " " + user_lastname] = numbers_picked
	print()

final_result = []
#Get the max duplicate for 1-5, and append it to the result
for cur_num in range(1,POWERBALL_NUMBER):
	cur_num_dict = dict((key, value) for (key, value) in number_dict.items() if key.startswith(str(cur_num) + "-"))
	max_value = choose_max_value(str(cur_num), cur_num_dict, False)
	final_result.append(max_value)

#Get the max duplicate for powerball
cur_num_dict = dict((key, value) for (key, value) in number_dict.items() if key.startswith("P-"))
max_value = choose_max_value("P", cur_num_dict, True)
final_result.append(max_value)

print()
print("USERS:")
for key, value in powerball_dict.items():
	#Tiny list manipluation that takes the final value in the list as the Powerball
	modified_value = value[0:len(value)-1]
	print(key + ": " + ', '.join(str(num) for num in modified_value) +
				" | Powerball: " + str(value[len(value)-1]))
	
print()
print("POWERBALL RESULT:")
#Same list manipulation, that allows the final value in "final_result" to be the Powerball
modified_final_result = final_result[0:len(final_result)-1]
print(', '.join(str(num) for num in modified_final_result) + " | Powerball: " + str(final_result[len(final_result)-1]))
		
#divider for command line reading
print("-----------------------------------------------------------------------------------------------------")