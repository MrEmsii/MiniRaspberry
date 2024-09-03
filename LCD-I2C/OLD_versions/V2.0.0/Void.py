import sqlite3, time, traceback
import LCD_I2C
import leds
import pilot
import threading, os


lcd = LCD_I2C.start()
leds = leds.glowa()


class table:
	def Dane():
		con = sqlite3.connect('/samba/python/SQL.db')
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
			print("Istnieje")
			
		try:	
			cur.execute('INSERT INTO Dane VALUES(2, "pid_LCD" , 0);')
		except Exception:
			print("Istnieje")
			
		try:	
			cur.execute('INSERT INTO Dane VALUES(3, "pid_Leds" , 0);')
		except Exception:
			print("Istnieje")
			
		try:	
			cur.execute('INSERT INTO Dane VALUES(4, "pid_pilot" , 0);')
		except Exception:
			print("Istnieje")
			
		con.commit()	
		con.close()
			
	def temperatura():
		con = sqlite3.connect('/samba/python/SQL.db')
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
		con = sqlite3.connect('/samba/python/SQL.db')
		con.row_factory = sqlite3.Row
		cur = con.cursor()
		
		for num in range(2,5):
			cur.execute("SELECT Dane.id, wartosc FROM Dane WHERE id=?", (str(num)))
			lista = cur.fetchall()
			for id in lista:
				print(id['wartosc'])
				os.system("sudo kill -9 " + id['wartosc'] )
	
	def starter():
		pliki = ["LCD_I2C.py", "leds.py", "pilot.py"]
		
		for plik in pliki:
			os.system("sudo nohup python /samba/python/" + plik + " &")
			time.sleep(0.5)

def main():
	table.temperatura()
	table.Dane()
	startowe.kill()
	startowe.starter()
	

try:   
	main()

except Exception:
	traceback.print_exc()
# Start new Threads


