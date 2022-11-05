from asyncio.windows_events import NULL
import sqlite3, shutil, hashlib

def tablica():
    cursor.execute("DROP TABLE IF EXISTS STATS")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS STATS (
            DATA varchar(250) NOT NULL,
            TEMP_SR varchar(250) NOT NULL,
            TEMP_MIN varchar(250) NOT NULL,
            TEMP_MAX varchar(250) NOT NULL
        )""")

    print ("Table created successfully")

def stats_data():
    min  = 9*10^3
    max = NULL
    sr = NULL
    sr_ind = 0

    cursor = conn.execute("SELECT MAX(data), MAX(godzina) from temperatura")
    for row in cursor:
        koniec = str(str(row[0])[0:4] + "-" + str(int(row[0][5:7])) + "-" + str(int(row[0][8:12])) + " " + str(int(row[1][0:2])))
        teraz = NULL

    cursor = conn.execute("SELECT id, godzina, temp_dot, data FROM temperatura WHERE id=1")
    for row in cursor: 
        rok = int(row[3][0:4])
        miesiac = int(row[3][5:7])
        dzien = int(row[3][8:12])
        godzina = int(row[1][0:2])

    last = NULL

    while koniec != teraz:
        cursor = conn.execute("SELECT id, godzina, temp_dot, data from temperatura")
        for row in cursor:
            teraz = str(str(rok) + "-" + str(miesiac) + "-" + str(dzien) + " " + str(godzina))
            wiersz = str(str(row[3])[0:4] + "-" + str(int(row[3][5:7])) + "-" + str(int(row[3][8:12])) + " " + str(int(row[1][0:2])))
            if wiersz == teraz:
                
                if min > float(row[2]):
                    min = float(row[2])
                if max < float(row[2]):
                    max = float(row[2])
                sr = sr + float(row[2])
                sr_ind = sr_ind + 1

                if godzina < 10:
                    days = row[3] + str(" 0" + str(godzina) + ":00:00")
                else:
                    days = row[3] + str(" " + str(godzina) + ":00:00")     
        godzina = godzina + 1

        if days != last:
            print(days + ", Min = " + str(min) + ", Max = " + str(max) + ", Sr = " + str(sr/sr_ind)[0:5])
            cursor.execute('INSERT INTO STATS VALUES(?, ?, ?, ?);', ((days, str(sr/sr_ind)[0:5], min, max)))
            conn.commit()
            last = days

            min = 9999
            max = NULL
            sr = NULL
            sr_ind = NULL

        if godzina == 24:
            dzien = dzien + 1
            godzina = 0 
        if dzien == 32:
            miesiac = miesiac + 1
            dzien = 1
        if miesiac == 13:
            rok = rok + 1
            miesiac = 1
            
    print("\nPrint Data successfully\n")

def main():
    global cursor, conn

    conn = sqlite3.connect("C:/Users/Lenovo/Desktop/Bluetooth/SQL.db")
    cursor = conn.cursor()
    print("\nOpened database successfully\n")

    tablica()

    stats_data()
    
    conn.commit()
    conn.close()

    print("Print database successfully\n")    

def file_as_bytes(file):
    with file:
        return file.read()

def hex_def():
    global hex_source,hex_dsk
    path_dsk = "C:/Users/Lenovo/Desktop/Bluetooth/SQL.db"
    path_source = "Y:/SQL.db"
    hex_dsk = (hashlib.md5(file_as_bytes(open(path_dsk, 'rb'))).hexdigest())
    hex_source = (hashlib.md5(file_as_bytes(open(path_source, 'rb'))).hexdigest()) 
    if hex_dsk != hex_source:
        shutil.copyfile("Y:/SQL.db", "C:/Users/Lenovo/Desktop/Bluetooth/SQL.db")

try:
    hex_def()
    main()
    if hex_dsk != hex_source:
        shutil.copyfile("C:/Users/Lenovo/Desktop/Bluetooth/SQL.db", "Y:/SQL.db")
    print("Done")

except KeyboardInterrupt:
    print("STOP_KIboard")    