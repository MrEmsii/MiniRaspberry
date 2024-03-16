import time, w1thermsensor, psutil, socket
from gpiozero import CPUTemperature
from subprocess import check_output
import sqlite3, time, traceback

class czasem:
	def czytaj_dane():
		print("Podaj sciezke  ")
		sciezka = input()
		con = sqlite3.connect(sciezka)
		con.row_factory = sqlite3.Row
		cur = con.cursor()
		cur.execute(
			"""
			SELECT temperatura.id, godzina, temp_dot FROM temperatura
			""")
		temperatury = cur.fetchall()
		for temperatura in temperatury:
			print(str(temperatura['temp_dot'].replace('.',',')))
			
	def przenies_dane():
		print("Podaj sciezke biorcy  ")
		sciezka_biorca = input()
		
		print("Podaj sciezke dawcy ")
		sciezka_dawca = input()
		
		biorca = sqlite3.connect(sciezka_biorca)
		biorca.row_factory = sqlite3.Row
		cur_biorca = biorca.cursor()
		cur_biorca.execute(		
			"""
			SELECT temperatura.id, data, godzina, temp_dot, temp_comma, jednostka FROM temperatura
			""")
				
		dawca = sqlite3.connect(sciezka_dawca)
		dawca.row_factory = sqlite3.Row
		cur_dawca = dawca.cursor()
		cur_dawca.execute(
			"""
			SELECT temperatura.id, data, godzina, temp, jednostka FROM temperatura
			""")
		
		temperatury = cur_dawca.fetchall()
		for temperatura in temperatury:
			biorca.execute('INSERT INTO temperatura VALUES(NULL, ?, ?, ?, ?, ?);', (temperatura['data'], temperatura['godzina'], temperatura['temp'], str(temperatura['temp'].replace('.',',')), temperatura['jednostka'])) #tutaj przenies z do  XDDD
			#print(temperatura['id'])	
		biorca.commit()

	def zczyt():
		print("Podaj sciezke biorcy  ")
		sciezka_biorca = input()
		
		print("Podaj sciezke dawcy ")
		sciezka_dawca = input()
		
		f = open(sciezka_dawca, "r")
		for line in f:
			#print(f.readline()[0:2] + " " + f.readline()[20:24])
			con = sqlite3.connect(sciezka_biorca)
			con.row_factory = sqlite3.Row
			cur = con.cursor()

			cur.execute("""
				CREATE TABLE IF NOT EXISTS temperatura (
					id INTEGER PRIMARY KEY ASC,
					data varchar(250) NOT NULL,
					godzina varchar(250) NOT NULL,
					temp varchar(250) NOT NULL,
					jednostka varchar(250) NOT NULL
				)""")
			cur.execute('INSERT INTO temperatura VALUES(NULL,?, ?, ?, ?);', ('2022-10-' + f.readline()[0:2], f.readline()[11:19], f.readline()[20:24], str(chr(176) + "C")))
			con.commit()
			con.close()

def erroro():
		f = open('/samba/python/Error.txt', "a")
		f.write(20*"*--*" + "\n" + time.strftime("%Y-%m-%d") + "   " + time.strftime("%H:%M:%S\n") + "\n" + traceback.format_exc() + "\n" + 20*"*--*")
		traceback.print_exc()

class bledy:
	def error_SQL(self):
		try:
			con = sqlite3.connect('/samba/python/SQL.db')
			con.row_factory = sqlite3.Row
			cur = con.cursor()

			cur.execute("""
				CREATE TABLE IF NOT EXISTS Error (
					id INTEGER PRIMARY KEY ASC,
					data varchar(250) NOT NULL,
					godzina varchar(250) NOT NULL,
					error varchar(250) NOT NULL
				)""")
			cur.execute('INSERT INTO Error VALUES(NULL,?, ?, ?);', ((time.strftime("%Y-%m-%d"), time.strftime("%H:%M:%S"), traceback.format_exc() )))
			traceback.print_exc()
			con.commit()
			con.close()
		except Exception:
			print("ERROR!")
			traceback.print_exc()
			time.sleep(1)

def main():
	print("""
	Witaj w moim programie!
	Co chcesz zrobić? 
		1. x 
		2. x
		9. Inne""")
	scan = int(input("Wiec? "))
	
	
	if scan == 9:
		print("""Co chcesz zrobić? 
			1. Print SQL 
			2. Kopiowanie danych
			3. Zczytywanie danych z pliku \n""")
			
		scan = int(input("Wiec? "))
		if scan == 1:
			czasem.czytaj_dane()
		elif scan == 2:
			czasem.przenies_dane()
		elif scan == 3:		
			czasem.zczyt()
		else:
			bledy.error_SQL()	
	else:
		bledy.error_SQL()	
			
		
