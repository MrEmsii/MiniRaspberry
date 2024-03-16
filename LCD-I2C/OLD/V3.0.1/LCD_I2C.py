# Author: Emsii 
# Date: 26.10.2022 
# https://github.com/EmsiiDiss

import API_LCD_I2C, offs_programs
import time, w1thermsensor, psutil, datetime
from gpiozero import CPUTemperature
from subprocess import check_output
from bs4 import BeautifulSoup
import sqlite3, os, requests, json, threading 

opoznienie = " " * 16

mylcd = API_LCD_I2C.lcd()
sensor = w1thermsensor.W1ThermSensor()
i_program = offs_programs.bledy()

godzina_start = 7
godzina_stop = 22
status = 1
start_time = float(time.time()) + 5
temp_time = float(time.time()) + 10
temp_time_1 = float(time.time())
miesiace = ["Stycznia", 'Lutego', 'Marca', 'Kwietnia', 'Maja', 'Czerwca', 'Lipca', 'Sierpnia', 'Wrzesnia', 'Pazdziernika', 'Listopada', 'Grudnia']
ost_status = status

class funkcje:
	def zegar():
		godzina = "Time: " + time.strftime("%H:%M:%S")
		godzina_UTC = "UTC: " + str(datetime.datetime.utcnow())[11:19]
		data = time.strftime("%d") + " " + miesiace[int(time.strftime("%m")) - 1]
		rok = str(time.strftime("%Y"))
		
		mylcd.lcd_display_string_pos(godzina, 1, int((20 - len(godzina))/2)-1)
		mylcd.lcd_display_string_pos(godzina_UTC, 2, int((20 - len(godzina_UTC))/2))
		mylcd.lcd_display_string_pos(data, 3, int((20 - len(data))/2))
		mylcd.lcd_display_string_pos(rok, 4, int((20 - len(rok))/2))

	def termometr():
		temp_1 = " T Pokoj = " + termometr_1 + chr(223) + "C "
		temp_2 = " T RasPI = " + str(CPUTemperature().temperature)[0:4] + chr(223) + "C "
		mylcd.lcd_display_string_pos(str(temp_1), 2, int((20 - len(str(temp_1)))/2) - 1)
		mylcd.lcd_display_string_pos(str(temp_2), 3, int((20 - len(str(temp_2)))/2) - 1)

	def get_ip():
		cmd = str(check_output("hostname -I | cut -d\' \' -f1", shell=True).decode("utf-8").strip())
		if len(cmd) > 5 and len(cmd) < 16:
			return cmd
		else:
			return "     No IP     "

	def stats():
		cpu_proc = "  CPU= " + str(psutil.cpu_percent(interval = 0.5)) + "%  "
		RAM_proc = "  RAM= " + str(psutil.virtual_memory().percent) + "%  "
		disk_proc = "  DISK= " + str(psutil.disk_usage('/').percent) + "%  "

		mylcd.lcd_display_string_pos(str(funkcje.get_ip()), 1, int((20 - len(str(funkcje.get_ip())))/2) - 1)
		mylcd.lcd_display_string_pos(str(cpu_proc), 2, 2)
		mylcd.lcd_display_string_pos(str(disk_proc), 3, 1)
		mylcd.lcd_display_string_pos(str(RAM_proc), 4, 2)

	def pogodynka():
		try:
			global info_weather
			opoznienie_info_weather = opoznienie + info_weather + opoznienie
			mylcd.lcd_display_string_pos(str(location_raspi), 1, int((20 - len(str(location_raspi)))/2))
			mylcd.lcd_display_string_pos(str(time_update), 2, int((20 - len(str(time_update)))/2))
			mylcd.lcd_display_string_pos(str(temp_weather), 4, int((20 - len(str(temp_weather)))/2))

			if len(info_weather) >= 18:
				for i in range (0, len(info_weather)):
					lcd_text = opoznienie_info_weather[i:(i+20)]
					mylcd.lcd_display_string(lcd_text,3)
					time.sleep(0.3)
					mylcd.lcd_display_string(opoznienie[(22+i):i], 3)
			else:
				mylcd.lcd_display_string_pos(str(info_weather), 3, int((20 - len(str(info_weather)))/2))		
		except:	
			mylcd.lcd_display_string_pos("No INFO", 1, int((20 - len("No INFO"))/2))
			mylcd.lcd_display_string_pos("No INFO", 2, int((20 - len("No INFO"))/2))
			mylcd.lcd_display_string_pos("No INFO", 4, int((20 - len("No INFO"))/2))
			definicje.lokalizacja()
			#i_program.error_SQL()
			time.sleep(10)



	def timer():
		global start_time, status, ost_status

		if float(time.strftime("%H.%M%S")) >= godzina_start and float(time.strftime("%H.%M%S")) <= godzina_stop:
			if float(time.time()) >= start_time:
				start_time = float(time.time())	+ 4
				status = status + 1
				mylcd.backlight(1)
			if status >= 5:
				status = 1
			if status != ost_status:
				ost_status = status
				mylcd.lcd_clear()
		else:
			if status != 0:
				mylcd.lcd_clear()
			mylcd.backlight(0)
			status = 0

class definicje:
	def removeAccents(input_text):
		strange='ŮôῡΒძěἊἦëĐᾇόἶἧзвŅῑἼźἓŉἐÿἈΌἢὶЁϋυŕŽŎŃğûλВὦėἜŤŨîᾪĝžἙâᾣÚκὔჯᾏᾢĠфĞὝŲŊŁČῐЙῤŌὭŏყἀхῦЧĎὍОуνἱῺèᾒῘᾘὨШūლἚύсÁóĒἍŷöὄЗὤἥბĔõὅῥŋБщἝξĢюᾫაπჟῸდΓÕűřἅгἰშΨńģὌΥÒᾬÏἴქὀῖὣᾙῶŠὟὁἵÖἕΕῨčᾈķЭτἻůᾕἫжΩᾶŇᾁἣჩαἄἹΖеУŹἃἠᾞåᾄГΠКíōĪὮϊὂᾱიżŦИὙἮὖÛĮἳφᾖἋΎΰῩŚἷРῈĲἁéὃσňİΙῠΚĸὛΪᾝᾯψÄᾭêὠÀღЫĩĈμΆᾌἨÑἑïოĵÃŒŸζჭᾼőΣŻçųøΤΑËņĭῙŘАдὗპŰἤცᾓήἯΐÎეὊὼΘЖᾜὢĚἩħĂыῳὧďТΗἺĬὰὡὬὫÇЩᾧñῢĻᾅÆßшδòÂчῌᾃΉᾑΦÍīМƒÜἒĴἿťᾴĶÊΊȘῃΟúχΔὋŴćŔῴῆЦЮΝΛῪŢὯнῬũãáἽĕᾗნᾳἆᾥйᾡὒსᾎĆрĀüСὕÅýფᾺῲšŵкἎἇὑЛვёἂΏθĘэᾋΧĉᾐĤὐὴιăąäὺÈФĺῇἘſგŜæῼῄĊἏØÉПяწДĿᾮἭĜХῂᾦωთĦлðὩზკίᾂᾆἪпἸиᾠώᾀŪāоÙἉἾρаđἌΞļÔβĖÝᾔĨНŀęᾤÓцЕĽŞὈÞუтΈέıàᾍἛśìŶŬȚĳῧῊᾟάεŖᾨᾉςΡმᾊᾸįᾚὥηᾛġÐὓłγľмþᾹἲἔбċῗჰხοἬŗŐἡὲῷῚΫŭᾩὸùᾷĹēრЯĄὉὪῒᾲΜᾰÌœĥტ'
		ascii_replacements='UoyBdeAieDaoiiZVNiIzeneyAOiiEyyrZONgulVoeETUiOgzEaoUkyjAoGFGYUNLCiIrOOoqaKyCDOOUniOeiIIOSulEySAoEAyooZoibEoornBSEkGYOapzOdGOuraGisPngOYOOIikoioIoSYoiOeEYcAkEtIuiIZOaNaicaaIZEUZaiIaaGPKioIOioaizTIYIyUIifiAYyYSiREIaeosnIIyKkYIIOpAOeoAgYiCmAAINeiojAOYzcAoSZcuoTAEniIRADypUitiiIiIeOoTZIoEIhAYoodTIIIaoOOCSonyKaAsSdoACIaIiFIiMfUeJItaKEISiOuxDOWcRoiTYNLYTONRuaaIeinaaoIoysACRAuSyAypAoswKAayLvEaOtEEAXciHyiiaaayEFliEsgSaOiCAOEPYtDKOIGKiootHLdOzkiaaIPIIooaUaOUAIrAdAKlObEYiINleoOTEKSOTuTEeiaAEsiYUTiyIIaeROAsRmAAiIoiIgDylglMtAieBcihkoIrOieoIYuOouaKerYAOOiaMaIoht'
		translator=str.maketrans(strange,ascii_replacements)
		return input_text.translate(translator)

	def termometr():
		global termometr_1
		while True:
			try:
				termometr_1 = str(float(sensor.get_temperature() - 3.5))[0:5] 
				time.sleep(0.3)
			except:
				try:
					termometr_1 = str(float(sensor.get_temperature() - 3.5))[0:5]
				except:
					termometr_1 = "100.0"
			time.sleep(1)

	headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

	def weather(city):
		global location_raspi, time_update, info_weather, temp_weather
		while True:
			try:
				city = city.replace(" ", "+")
				res = requests.get(
					f'https://www.google.com/search?q={city}&oq={city}&aqs=chrome.0.35i39l2j0l4j46j69i60.6128j1j7&sourceid=chrome&ie=UTF-8', headers=definicje.headers)
				soup = BeautifulSoup(res.text, 'html.parser')
				location_raspi = soup.select('#wob_loc')[0].getText().strip()
				location_raspi = definicje.removeAccents(input_text = location_raspi)
				time_update = soup.select('#wob_dts')[0].getText().strip()
				time_update = definicje.removeAccents(input_text = time_update)
				info_weather = soup.select('#wob_dc')[0].getText().strip()
				info_weather = definicje.removeAccents(input_text = info_weather)
				temp_weather = soup.select('#wob_tm')[0].getText().strip() + chr(223) + "C "
			except:
				info_weather = "brak info"
				temp_weather = "brak info"
				time_update = "brak info"
				location_raspi = "brak info"
				i_program.error_SQL()
				time.sleep(60)
				
			time.sleep(5*60)	

	def lokalizacja():
		global city
		url = ''
		r = requests.get(url)
		data = json.loads(r.content.decode())
		city = data["city"] + " weather"

class inne:			
	def save():
		try:
			global temp_time, termometr_1 
			while True:
				con = sqlite3.connect('/samba/python/Heat.db', check_same_thread=3)
				con.row_factory = sqlite3.Row
				cur = con.cursor()
				time.sleep(0.01)
				cur.execute('INSERT INTO temperatura VALUES(NULL,?, ?, ?, ?, ?);', ((time.strftime("%Y-%m-%d"), time.strftime("%H:%M:%S"), termometr_1, termometr_1.replace('.',','), str(chr(176) + "C"))))
				con.commit()
				con.close()
				time.sleep(60*3)
		except:
			i_program.error_SQL()
			inne.save()		

	def pid_LCD():
		con = sqlite3.connect('/samba/python/SQL.db', check_same_thread=3)
		con.row_factory = sqlite3.Row
		cur = con.cursor()
		cur.execute('UPDATE Dane SET wartosc=? WHERE id=?', (os.getpid(), 2))
		con.commit()
		con.close()		
		
class start:
	def main():
		try:
			global status,start_time, city
			inne.pid_LCD()
			while True:
				funkcje.timer()
				if status == 1:
					funkcje.zegar()
				elif status == 2:
					funkcje.termometr()
				elif status == 3:
					funkcje.stats()
				elif status == 4:
					funkcje.pogodynka()
				time.sleep(0.7)
		except KeyboardInterrupt:
			print("OFF - KeyBoaord")
		except:
			print("XD")	
			i_program.error_SQL()
			
if __name__ == '__main__':
	try:
		ttermometr = threading.Thread(target=definicje.termometr, args=())
		ttermometr.start()
		time.sleep(1)
		tmain = threading.Thread(target=start.main, args=())
		tmain.start()
		
		t_save = threading.Thread(target=inne.save, args=())
		
		t3 = threading.Thread(target=definicje.lokalizacja, args=())
		t3.start()	
		t3.join()

		t2 = threading.Thread(target=definicje.weather, args=(city,))
		t2.start()
		t_save.start()

	except KeyboardInterrupt:
		print("OFF - KeyBoaord")
	except:
		print("XD")	
		i_program.error_SQL()
