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

pixel_pin = board.D21
num_pixels = 12
ORDER = neopixel.GRB

brightness = 0.5

pixels = neopixel.NeoPixel(
	pixel_pin, num_pixels, brightness = brightness, auto_write=False, pixel_order=ORDER
)

brightness_stop = 0.8


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
	global i, pixels
	i = 1

	for j in range(255):
		for i in range(num_pixels):
			pixel_index = (i * 256 // num_pixels) + j
			pixels[i] = wheel(pixel_index & 255)
			
		pixels.show()
		
		time.sleep(wait)
class glowa:
	def effects(effect):
		global pixels, brightness, brightness_stop, i

		if effect == 2:
			glowa.stale()
			glowa.miganie()

		elif effect == 1:
			cur.execute("""SELECT Dane.id,wartosc FROM Dane where id=6""")
			brightnessTab = cur.fetchall()
			for Dane in brightnessTab:
				brightness = float(Dane['wartosc'])
			glowa.stale()	

		elif effect == 3:
			glowa.tyncza()

	def stale():
		cur.execute("""SELECT Dane.id,wartosc FROM Dane where id=1""")
		stan_ledTab = cur.fetchall()
			
		for Dane in stan_ledTab:
			color = int(Dane['wartosc'])
			if color == 1:
				pixels.fill((255, 0, 0))

			if color == 2:
				pixels.fill((0, 255, 0))
				
			if color == 3:
				pixels.fill((0, 0, 255))
				
			if color == 4:
				pixels.fill((255, 255, 0))
				
			if color == 5:
				pixels.fill((0, 255, 255))
				
			if color == 6:
				pixels.fill((255, 0, 255))
				
			if color == 7:
				pixels.fill((255, 255, 120))
				
			if color == 8:
				pixels.fill((120, 255, 255))
				
			if color == 9:
				pixels.fill((255, 120, 255))
								
			if color == 0:
				pixels.fill((0, 0, 0))	

	def miganie():
		global brightness_stop, brightness
		if brightness_stop >= 0.8:
			brightness = brightness + 0.01
			if brightness >= 0.8:
				brightness_stop = 0
		if brightness_stop <= 0:
			brightness = brightness - 0.01
			if brightness <= 0.1:
				brightness_stop = 1
		#print(brightness)		
	def tyncza():
		global brightness
		brightness = 0.5
		rainbow_cycle(0.01) 

	def main():		
		global pixels, brightness, cur, pixels

		con = sqlite3.connect('/samba/python/SQL.db', check_same_thread=3)
		con.row_factory = sqlite3.Row
		cur = con.cursor()
		
		glowa.effects(1)

		while True:
			pixels = neopixel.NeoPixel(
				pixel_pin, num_pixels, brightness = brightness, auto_write=False, pixel_order=ORDER
			)
			cur.execute("""SELECT Dane.id,wartosc FROM Dane where id=5""")
			effectsTab = cur.fetchall()
			for Dane in effectsTab:
				effect = int(Dane['wartosc'])
			glowa.effects(effect)
			
			# print(color,brightness,effect)
			pixels.show()
			time.sleep(0.05)

class inne:
	def pid_Leds():
		con = sqlite3.connect('/samba/python/SQL.db', check_same_thread=3)
		con.row_factory = sqlite3.Row
		cur = con.cursor()
		cur.execute('UPDATE Dane SET wartosc=? WHERE id=?', (os.getpid(), 3))
		cur.execute('UPDATE Dane SET wartosc=? WHERE id=?', (0, 1))
		con.commit()
		con.close()	

if __name__ == '__main__':
	try:
		inne.pid_Leds()
		glowa.main()
	except Exception:
		print("XD")	
		i_program.error_SQL()
