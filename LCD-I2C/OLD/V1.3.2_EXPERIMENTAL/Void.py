import sqlite3, time, traceback
import LCD_I2C
import leds
import pilot
import threading


lcd = LCD_I2C.start()
leds = leds.glowa()

exitFlag = 0

class myThread1 (threading.Thread):
   def __init__(self, threadID, name, counter):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.counter = counter
   def run(self):
      print ("Starting " + self.name)
      lcd.main()
      print ("Exiting " + self.name)

class myThread2 (threading.Thread):
   def __init__(self, threadID, name, counter):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.counter = counter
   def run(self):
      print ("Starting " + self.name)
      leds.main()
      print ("Exiting " + self.name)

class myThread3 (threading.Thread):
   def __init__(self, threadID, name, counter):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.counter = counter
   def run(self):
      print ("Starting " + self.name)
      pilot.main(self)
      print ("Exiting " + self.name)

def print_time(threadName, delay, counter):
   while counter:
      if exitFlag:
         threadName.exit()
      time.sleep(delay)
      print ("%s: %s" % (threadName, time.ctime(time.time())))
      counter -= 1


try:   
	thread3 = myThread3(3, "Thread-3", 1)
	# Create new threads
	thread1 = myThread1(1, "Thread-1", 1)
	thread2 = myThread2(2, "Thread-2", 1)


	thread3.start()

	thread2.start()
	thread1.start()

except Exception:
	traceback.print_exc()
# Start new Threads


