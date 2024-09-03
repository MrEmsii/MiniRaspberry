import sqlite3, threading, time
import LCD_I2C
import leds

lcd = LCD_I2C.start()
leds = leds.glowa()

class top:
	def main():
		t1 = Thread(target=lcd.main())
		t2 = Thread(target=leds.main())
try:
	top.main()
except Exception:
	print("cos")
