#-----------------------------------------#
# Name - IR-Finalized.py
# Description - The finalized code to read data from an IR sensor and then reference it with stored values
# Author - Lime Parallelogram
# License - Completely Free
# Date - 12/09/2019
#------------------------------------------------------------#
# Add more 26.10.2022 Emsii

import RPi.GPIO as GPIO
from datetime import datetime
import time, sqlite3
import inne

i_program = inne.bledy()

# Static program vars
pin = 38  # Input pin of sensor (GPIO.BOARD)
Buttons = [0x300FF30CF, 0x300FF18E7,  0x300FF7A85, 0x300FF10EF, 0x300FF38C7, 0x300FF5AA5, 0x300FF42BD, 0x300FF4AB5, 0x300FF52AD, 0x300FF6897, 0x300FF9867, 0x300FFB04F, 0x300FFE01F, 0x300FFA857, 0x300FF906F] 
ButtonsNames = ["1",   		"2",     	 "3",      		 "4",    	  "5",		"6", 	 		"7", 		 "8", 			"9", 	"0", 		"100+", 		"200+", 	"-", 		"+", 		"eq"]  
# Sets up GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(pin, GPIO.IN)

def getBinary():
	# Internal vars
	num1s = 0  # Number of consecutive 1s read
	binary = 1  # The binary value
	command = []  # The list to store pulse times in
	previousValue = 0  # The last value
	value = GPIO.input(pin)  # The current value

	# Waits for the sensor to pull pin low
	while value:
		time.sleep(0.0001) # This sleep decreases CPU utilization immensely
		value = GPIO.input(pin)
		
	# Records start time
	startTime = datetime.now()
	
	while True:
		# If change detected in value
		if previousValue != value:
			now = datetime.now()
			pulseTime = now - startTime #Calculate the time of pulse
			startTime = now #Reset start time
			command.append((previousValue, pulseTime.microseconds)) #Store recorded data
			
		# Updates consecutive 1s variable
		if value:
			num1s += 1
		else:
			num1s = 0
		
		# Breaks program when the amount of 1s surpasses 10000
		if num1s > 10000:
			break
			
		# Re-reads pin
		previousValue = value
		value = GPIO.input(pin)
		
	# Converts times to binary
	for (typ, tme) in command:
		if typ == 1: #If looking at rest period
			if tme > 1000: #If pulse greater than 1000us
				binary = binary *10 +1 #Must be 1
			else:
				binary *= 10 #Must be 0
			
	if len(str(binary)) > 34: #Sometimes, there is some stray characters
		binary = int(str(binary)[:34])
		
	return binary
	
# Convert value to hex
def convertHex(binaryValue):
	tmpB2 = int(str(binaryValue),2) #Temporarely propper base 2
	return hex(tmpB2)


def pilot():
	con = sqlite3.connect('/samba/python/SQL.db')
	con.row_factory = sqlite3.Row
	cur = con.cursor()
	inData = convertHex(getBinary()) #Runs subs to get incoming hex value
	for button in range(len(Buttons)):#Runs through every value in list
		if hex(Buttons[button]) == inData: #Checks this against incoming
			print(ButtonsNames[button]) #Prints corresponding english name for button
			#if ButtonsNames[button] == "1":
			cur.execute('UPDATE Dane SET wartosc=? WHERE id=?', (ButtonsNames[button], 1))
			con.commit()	
			con.close()
	pilot()
	
try:
	try:	
		con = sqlite3.connect('/samba/python/SQL.db')
		con.row_factory = sqlite3.Row
		cur = con.cursor()
		cur.execute("""
			CREATE TABLE IF NOT EXISTS Dane (
				id INTEGER PRIMARY KEY ASC,
				dana varchar(250) NOT NULL,
				wartosc varchar(250) NOT NULL
			)""")
		cur.execute('INSERT INTO Dane VALUES(1, "stan_led" , 0);')
		con.commit()
		con.close()

	except Exception:
		print("Istnieje!")
		cur.execute('UPDATE Dane SET wartosc=? WHERE id=?', ("0", 1))
		con.commit()	
		con.close()
		
	
	pilot()

	
#zmienic przepisywanie wartosci - pilot
except Exception:
	i_program.error_SQL()

