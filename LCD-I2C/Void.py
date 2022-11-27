# Author: Emsii 
# Date: 26.10.2022 
# https://github.com/EmsiiDiss

import offs_programs
import os, sqlite3, time

i_program = offs_programs.bledy()

class table:
	def Dane():
		con = sqlite3.connect(way + 'SQL.db')
		con.row_factory = sqlite3.Row
		cur = con.cursor()
		cur.execute("""
			CREATE TABLE IF NOT EXISTS Dane (
				id INTEGER PRIMARY KEY ASC,
				dana varchar(250) NOT NULL,
				wartosc varchar(250) NOT NULL
			)""")
		try:	
			cur.execute('INSERT INTO Dane VALUES(1, "stan_led" , 0);')
		except Exception:
			return
			
		try:	
			cur.execute('INSERT INTO Dane VALUES(2, "pid_LCD" , 0);')
		except Exception:
			return
			
		try:	
			cur.execute('INSERT INTO Dane VALUES(3, "pid_Leds" , 0);')
		except Exception:
			return
			
		try:	
			cur.execute('INSERT INTO Dane VALUES(4, "pid_pilot" , 0);')
		except Exception:
			return
			
		con.commit()	
		con.close()
			
	def temperatura():
		con = sqlite3.connect(way + 'SQL.db')
		con.row_factory = sqlite3.Row
		cur = con.cursor()

		cur.execute("""
			CREATE TABLE IF NOT EXISTS temperatura (
				id INTEGER PRIMARY KEY ASC,
				data varchar(250) NOT NULL,
				godzina varchar(250) NOT NULL,
				temp_dot varchar(250) NOT NULL,
				temp_comma varchar(250) NOT NULL,
				jednostka varchar(250) NOT NULL
			)""")
			
		con.commit()
		con.close()

class startowe:
	def kill():
		con = sqlite3.connect(way + 'SQL.db')
		con.row_factory = sqlite3.Row
		cur = con.cursor()
		
		print("\nOLD PID:")	
		for num in range(2,5):
			cur.execute("SELECT Dane.id, wartosc, dana FROM Dane WHERE id=?", (str(num)))
			lista = cur.fetchall()
			for id in lista:
				print(id['dana'] +" = " + id['wartosc'])
				if id['wartosc'] != "0":
					os.system("sudo kill -9 " + id['wartosc'] )
					time.sleep(0.01)
		print("\n")			
		con.close()			
	
	def starter():
		pliki = ["LCD_I2C.py", "leds.py", "pilot.py"]
		
		for plik in pliki:
			os.system("sudo nohup python " + way + plik + " &")
			time.sleep(0.5)

		print("\nNew PID:")	
		con = sqlite3.connect(way + 'SQL.db')
		con.row_factory = sqlite3.Row
		cur = con.cursor()
		
		for num in range(2,5):
			cur.execute("SELECT Dane.id, wartosc, dana FROM Dane WHERE id=?", (str(num)))
			lista = cur.fetchall()
			for id in lista:
				print(id['dana'] +" = " + id['wartosc'])	
			
	def scanner():
		global way
		way = input("Enter way, where are programs:\n 0. DEFAULT\n 1. NOT DEFAULT\n")	
		if way == "0":
			way = str("/samba/python/")
		elif way == "1":
			way = input()
		else:
			print("\nWTF? Enter again\n")
			startowe.scanner()
			
		    
def main():
	table.temperatura()
	table.Dane()
	startowe.kill()
	startowe.starter()
	
def startup():
		global way
		i = 0
		way = 0
		while i <= 4:
			print("Hit KeyboardInterrupt if you need change DEFAULT way programs!")
			i = i + 1
			time.sleep(1)
		way = str("/samba/python/")	
		main()	
	

if __name__ == '__main__':
	try:
		startup()
	except Exception:
		i_program.error_SQL()
	except KeyboardInterrupt:
		startowe.scanner()	


