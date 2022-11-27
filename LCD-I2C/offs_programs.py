import traceback, sqlite3,time

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