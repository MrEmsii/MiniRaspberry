# Author: Emsii 
# Date: 26.10.2022 
# https://github.com/EmsiiDiss

import API_LCD_I2C, offs_programs
import time, w1thermsensor, psutil, datetime
from gpiozero import CPUTemperature
from subprocess import check_output
from bs4 import BeautifulSoup
import sqlite3, os, requests, json 


opoznienie = " " * 16

mylcd = API_LCD_I2C.lcd()
sensor = w1thermsensor.W1ThermSensor()
i_program = offs_programs.bledy()

status = 1
start_time = float(time.time()) + 5
temp_time = float(time.time()) + 10
miesiace = ["Stycznia", 'Lutego', 'Marca', 'Kwietnia', 'Maja', 'Czerwca', 'Lipca', 'Sierpnia', 'Wrzesnia', 'Pazdziernika', 'Listopada', 'Grudnia']
ost_status = status

class funkcje:
	def zegar():
		godzina = "Time: " + time.strftime("%H:%M:%S")
		godzina_UTC = "UTC: " + str(datetime.datetime.utcnow())[11:19]
		data = time.strftime("%d") + " " + miesiace[int(time.strftime("%m")) - 1]
		rok = str(time.strftime("%Y"))
		
		mylcd.lcd_display_string(godzina, 1, int((20 - len(godzina))/2)-1)
		mylcd.lcd_display_string(godzina_UTC, 2, int((20 - len(godzina_UTC))/2))
		mylcd.lcd_display_string(data, 3, int((20 - len(data))/2))
		mylcd.lcd_display_string(rok, 4, int((20 - len(rok))/2))

	def termometr():
		temp_1 = " T Pokoj = " + definicje.termometr() + chr(223) + "C "
		temp_2 = " T RasPI = " + str(CPUTemperature().temperature)[0:4] + chr(223) + "C "
		mylcd.lcd_display_string(str(temp_1), 2, int((20 - len(str(temp_1)))/2) - 1)
		mylcd.lcd_display_string(str(temp_2), 3, int((20 - len(str(temp_2)))/2) - 1)

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

		mylcd.lcd_display_string(str(funkcje.get_ip()), 1, int((20 - len(str(funkcje.get_ip())))/2) - 1)
		mylcd.lcd_display_string(str(cpu_proc), 2, 2)
		mylcd.lcd_display_string(str(disk_proc), 3, 1)
		mylcd.lcd_display_string(str(RAM_proc), 4, 2)

	def pogodynka():
		opoznienie_info_weather = opoznienie + info_weather + opoznienie
		mylcd.lcd_display_string(str(location_raspi), 1, int((20 - len(str(location_raspi)))/2))
		mylcd.lcd_display_string(str(time_update), 2, int((20 - len(str(time_update)))/2))
		mylcd.lcd_display_string(str(temp_weather), 4, int((20 - len(str(temp_weather)))/2))
		for i in range (0, len(info_weather)):
			lcd_text = opoznienie_info_weather[i:(i+20)]
			mylcd.lcd_display_string(lcd_text,3)
			time.sleep(0.1)
			mylcd.lcd_display_string(opoznienie[(22+i):i], 3)

	def timer():
		global start_time, status, ost_status

		if float(time.time()) >= start_time:
			start_time = float(time.time())	+ 8
			status = status + 1
		if status >= 5:
			status = 1
		if status != ost_status:
			ost_status = status
			mylcd.lcd_clear()

class definicje:
	def removeAccents(input_text):
		strange='ŮôῡΒძěἊἦëĐᾇόἶἧзвŅῑἼźἓŉἐÿἈΌἢὶЁϋυŕŽŎŃğûλВὦėἜŤŨîᾪĝžἙâᾣÚκὔჯᾏᾢĠфĞὝŲŊŁČῐЙῤŌὭŏყἀхῦЧĎὍОуνἱῺèᾒῘᾘὨШūლἚύсÁóĒἍŷöὄЗὤἥბĔõὅῥŋБщἝξĢюᾫაπჟῸდΓÕűřἅгἰშΨńģὌΥÒᾬÏἴქὀῖὣᾙῶŠὟὁἵÖἕΕῨčᾈķЭτἻůᾕἫжΩᾶŇᾁἣჩαἄἹΖеУŹἃἠᾞåᾄГΠКíōĪὮϊὂᾱიżŦИὙἮὖÛĮἳφᾖἋΎΰῩŚἷРῈĲἁéὃσňİΙῠΚĸὛΪᾝᾯψÄᾭêὠÀღЫĩĈμΆᾌἨÑἑïოĵÃŒŸζჭᾼőΣŻçųøΤΑËņĭῙŘАдὗპŰἤცᾓήἯΐÎეὊὼΘЖᾜὢĚἩħĂыῳὧďТΗἺĬὰὡὬὫÇЩᾧñῢĻᾅÆßшδòÂчῌᾃΉᾑΦÍīМƒÜἒĴἿťᾴĶÊΊȘῃΟúχΔὋŴćŔῴῆЦЮΝΛῪŢὯнῬũãáἽĕᾗნᾳἆᾥйᾡὒსᾎĆрĀüСὕÅýფᾺῲšŵкἎἇὑЛვёἂΏθĘэᾋΧĉᾐĤὐὴιăąäὺÈФĺῇἘſგŜæῼῄĊἏØÉПяწДĿᾮἭĜХῂᾦωთĦлðὩზკίᾂᾆἪпἸиᾠώᾀŪāоÙἉἾρаđἌΞļÔβĖÝᾔĨНŀęᾤÓцЕĽŞὈÞუтΈέıàᾍἛśìŶŬȚĳῧῊᾟάεŖᾨᾉςΡმᾊᾸįᾚὥηᾛġÐὓłγľмþᾹἲἔбċῗჰხοἬŗŐἡὲῷῚΫŭᾩὸùᾷĹēრЯĄὉὪῒᾲΜᾰÌœĥტ'
		ascii_replacements='UoyBdeAieDaoiiZVNiIzeneyAOiiEyyrZONgulVoeETUiOgzEaoUkyjAoGFGYUNLCiIrOOoqaKyCDOOUniOeiIIOSulEySAoEAyooZoibEoornBSEkGYOapzOdGOuraGisPngOYOOIikoioIoSYoiOeEYcAkEtIuiIZOaNaicaaIZEUZaiIaaGPKioIOioaizTIYIyUIifiAYyYSiREIaeosnIIyKkYIIOpAOeoAgYiCmAAINeiojAOYzcAoSZcuoTAEniIRADypUitiiIiIeOoTZIoEIhAYoodTIIIaoOOCSonyKaAsSdoACIaIiFIiMfUeJItaKEISiOuxDOWcRoiTYNLYTONRuaaIeinaaoIoysACRAuSyAypAoswKAayLvEaOtEEAXciHyiiaaayEFliEsgSaOiCAOEPYtDKOIGKiootHLdOzkiaaIPIIooaUaOUAIrAdAKlObEYiINleoOTEKSOTuTEeiaAEsiYUTiyIIaeROAsRmAAiIoiIgDylglMtAieBcihkoIrOieoIYuOouaKerYAOOiaMaIoht'
		translator=str.maketrans(strange,ascii_replacements)
		return input_text.translate(translator)

	def termometr():
		try:
			term_1 = str(float(sensor.get_temperature() - 3.5))[0:5] 
			time.sleep(0.3)
		except:
			try: 
				term_1 = str(float(sensor.get_temperature() - 3.5))[0:5]
			except:
				term_1 = "19.0"
		return term_1		

	headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

	def weather(city):
		global location_raspi, time_update, info_weather, temp_weather
		city = city.replace(" ", "+")
		res = requests.get(
			f'https://www.google.com/search?q={city}&oq={city}&aqs=chrome.0.35i39l2j0l4j46j69i60.6128j1j7&sourceid=chrome&ie=UTF-8', headers=definicje.headers)
		soup = BeautifulSoup(res.text, 'html.parser')
		location_raspi = soup.select('#wob_loc')[0].getText().strip()
		location_raspi = definicje.removeAccents(input_text = location_raspi)
		time_update = soup.select('#wob_dts')[0].getText().strip()
		info_weather = soup.select('#wob_dc')[0].getText().strip()
		info_weather = definicje.removeAccents(input_text = info_weather)
		temp_weather = soup.select('#wob_tm')[0].getText().strip() + chr(223) + "C "

	def lokalizacja():
		url = ''
		r = requests.get(url)
		data = json.loads(r.content.decode())

		return data["city"]

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
		termo = definicje.termometr()
		con = sqlite3.connect('/samba/python/SQL.db')
		con.row_factory = sqlite3.Row
		cur = con.cursor()
		time.sleep(0.01)
		cur.execute('INSERT INTO temperatura VALUES(NULL,?, ?, ?, ?, ?);', ((time.strftime("%Y-%m-%d"), time.strftime("%H:%M:%S"), termo, termo.replace('.',','), str(chr(176) + "C"))))
		con.commit()
		con.close()
		
class start:
	def main():
		global status,start_time, city
		inne.pid_LCD()
		city = definicje.lokalizacja() + " weather"
		definicje.weather(city)
		mylcd.lcd_clear()
		while True:
						
			funkcje.timer()
			
			if status == 1:
				funkcje.zegar()
					
			elif status == 2:
				funkcje.termometr()
				inne.save()

			elif status == 3:
				funkcje.stats()
				
			elif status == 4:
				funkcje.pogodynka()
				definicje.weather(city)

			time.sleep(0.7)


if __name__ == '__main__':
	try:
		inicjal = "INICJALIZACJA"
		for init in range(1,5):
			mylcd.lcd_display_string(inicjal, init, int((20 - len(str(inicjal)))/2))

		

		start.main()
	except Exception:
		print("XD")	
		i_program.error_SQL()
