import API_LCD_I2C, inne
import time, w1thermsensor, psutil, socket
from gpiozero import CPUTemperature
from subprocess import check_output
import sqlite3, traceback, os

mylcd = API_LCD_I2C.lcd()
sensor = w1thermsensor.W1ThermSensor()
i_program = inne.bledy()

status = 1
start_time = float(time.time()) + 5
temp_time = float(time.time()) + 10
miesiace = ["Stycznia", 'Lutego', 'Marca', 'Kwietnia', 'Maja', 'Czerwca', 'Lipca', 'Sierpnia', 'Wrzesnia', 'Pazdziernika', 'Listopada', 'Grudnia']
ost_status = status

class funkcje:
	def zegar():
		godzina = time.strftime("%H:%M:%S")
		data = time.strftime("%d") + " " + miesiace[int(time.strftime("%m")) - 1]
		rok = str(time.strftime("%Y"))
		
		mylcd.lcd_display_string(godzina, 1, int((20 - len(godzina))/2))
		mylcd.lcd_display_string(data, 3, int((20 - len(data))/2))
		mylcd.lcd_display_string(rok, 4, int((20 - len(rok))/2))

	def termometr():
		temp_1 = " T Pokoj = " + str(float(sensor.get_temperature() - 3.5))[0:5] + "" + chr(223) + "C "
		temp_2 = " T RasPI = " + str(CPUTemperature().temperature)[0:4] + "" + chr(223) + "C "
		mylcd.lcd_display_string(str(temp_1), 2, int((20 - len(str(temp_1)))/2) - 1)
		mylcd.lcd_display_string(str(temp_2), 3, int((20 - len(str(temp_2)))/2) - 1)

	def get_ip():
		cmd = str(check_output("hostname -I | cut -d\' \' -f1", shell=True).decode("utf-8").strip())
		if len(cmd) > 5 and len(cmd) < 16:
			return cmd
		else:
			return "No IP"

	def stats():
		cpu_proc = "  CPU= " + str(psutil.cpu_percent(interval = 0.5)) + "%  "
		RAM_proc = "  RAM= " + str(psutil.virtual_memory().percent) + "%  "
		disk_proc = "  DISK= " + str(psutil.disk_usage('/').percent) + "%  "

		mylcd.lcd_display_string(str(funkcje.get_ip()), 1, int((20 - len(str(funkcje.get_ip())))/2) - 1)
		mylcd.lcd_display_string(str(cpu_proc), 2, 2)
		mylcd.lcd_display_string(str(disk_proc), 3, 1)
		mylcd.lcd_display_string(str(RAM_proc), 4, 2)

	def timer():
		global start_time, status, ost_status

		if float(time.time()) >= start_time:
			start_time = float(time.time())	+ 8
			status = status + 1
		if status >= 4:
			status = 1
		if status != ost_status:
			ost_status = status
			mylcd.lcd_clear()

class inne:			
	def save():
		global temp_time
		if float(time.time()) >= temp_time:
			temp_time = float(time.time())	+ 173
			inne.baza_danych()
	
	def pid_LCD():
		con = sqlite3.connect('/samba/python/SQL.db')
		con.row_factory = sqlite3.Row
		cur = con.cursor()
		cur.execute('UPDATE Dane SET wartosc=? WHERE id=?', (os.getpid(), 2))
		con.commit()
		con.close()		
	
	def baza_danych():
		termo = str(float(sensor.get_temperature() - 3.5))[0:5]
		
		con = sqlite3.connect('/samba/python/SQL.db')
		con.row_factory = sqlite3.Row
		cur = con.cursor()
		cur.execute('INSERT INTO temperatura VALUES(NULL,?, ?, ?, ?, ?);', ((time.strftime("%Y-%m-%d"), time.strftime("%H:%M:%S"), termo, termo.replace('.',','), str(chr(176) + "C"))))
		con.commit()
		con.close()
class start:
	def main(self):
		global status,start_time
		inne.pid_LCD()	
		while True:
				
			inne.save()
			funkcje.timer()
			if status == 1:
				funkcje.zegar()
					
			elif status == 2:
				funkcje.termometr()

			elif status == 3:
				funkcje.stats()
				
			elif status == 4:
				mylcd.lcd_display_string(sey(), 3, int((20 - len(sey()))/2))			
			time.sleep(0.5)


if __name__ == '__main__':
	try:
		start.main('')
	except KeyboardInterrupt:
		print("XD")	
		i_program.error_SQL()
