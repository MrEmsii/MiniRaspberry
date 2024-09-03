# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# Simple test for NeoPixels on Raspberry Pi
# Add more 26.10.2022 Emsii
#https://github.com/EmsiiDiss

import time
import board, sqlite3, random, os
import neopixel
import offs_programs

i_program = offs_programs.bledy()
g = (random.randint(1,80))/100

pixel_pin = board.D21
num_pixels = 12
ORDER = neopixel.GRB


pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness = g, auto_write=False, pixel_order=ORDER
)


def wheel(pos):
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos * 3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos * 3)
        g = 0
        b = int(pos * 3)
    else:
        pos -= 170
        r = 0
        g = int(pos * 3)
        b = int(255 - pos * 3)
    return (r, g, b) if ORDER in (neopixel.RGB, neopixel.GRB) else (r, g, b, 0)


def rainbow_cycle(wait):
	global i, g

	for j in range(255):
		for i in range(num_pixels):
			pixel_index = (i * 256 // num_pixels) + j
			pixels[i] = wheel(pixel_index & 255)
			
		pixels.show()
		time.sleep(wait)
class glowa:
	def main(self):
		
		inne.pid_Leds()
		
		global i, pixels, g
		i = 0
		g = 0.1
		g_stop = 1
		
		con = sqlite3.connect('/samba/python/SQL.db')
		con.row_factory = sqlite3.Row
		cur = con.cursor()

		while True:
			try:
				cur.execute(
					"""
					SELECT Dane.id,wartosc FROM Dane
					""")
				tablica = cur.fetchall()
			except Exception:
				continue
				
			if g_stop == 1:
				g = g + 0.01
				if g >= 0.8:
					g_stop = 0
			
			if g_stop == 0:
				g = g - 0.01
				if g <= 0.1:
					g_stop = 1
			
			pixels = neopixel.NeoPixel(
				pixel_pin, num_pixels, brightness = g, auto_write=False, pixel_order=ORDER
			)
			
			
			for Dane in tablica:
				#print(g)
				tab = Dane['wartosc']
				if tab == "1":
					pixels.fill((255, 0, 0))

				if tab == "2":
					pixels.fill((0, 255, 0))
					
				if tab == "3":
					pixels.fill((0, 0, 255))
					
				if tab == "4":
					pixels.fill((255, 255, 0))
					
				if tab == "5":
					pixels.fill((0, 255, 255))
					
				if tab == "6":
					pixels.fill((255, 0, 255))
					
				if tab == "7":
					pixels.fill((255, 255, 120))
					
				if tab == "8":
					pixels.fill((120, 255, 255))
					
				if tab == "9":
					pixels.fill((255, 120, 255))
									
				if tab == "eq":
					g = 0.6
					rainbow_cycle(0.01) 
					i = i + 1 
									
				if tab == "0":
					pixels.fill((0, 0, 0))	
			
			pixels.show()
			time.sleep(0.025)


class inne:
	def pid_Leds():
		con = sqlite3.connect('/samba/python/SQL.db')
		con.row_factory = sqlite3.Row
		cur = con.cursor()
		cur.execute('UPDATE Dane SET wartosc=? WHERE id=?', (0, 1))
		cur.execute('UPDATE Dane SET wartosc=? WHERE id=?', (os.getpid(), 3))
		con.commit()
		con.close()	


if __name__ == '__main__':
	try:
		glowa.main('')
	except Exception:
		print("XD")	
		i_program.error_SQL()
