# Author: Emsii 
# Date: 26.10.2022 
# https://github.com/EmsiiDiss

from asyncio.windows_events import NULL
import sqlite3, shutil, hashlib, datetime

def tablica():
    try:
        cursor.execute("DROP TABLE IF EXISTS STATS")
        conn.execute("""
            CREATE TABLE IF NOT EXISTS STATS (
                DATA varchar(250) NOT NULL,
                TEMP_SR varchar(250) NOT NULL,
                TEMP_MIN varchar(250) NOT NULL,
                TEMP_MAX varchar(250) NOT NULL
            )""")

        print ("Table creating successfully")

    except:
        print("\n\nCRASH Table creating\n\n")
        raise SystemExit(0) 
            

def stats_calculator():
    min  = 9*10^3
    max = NULL
    sr = NULL
    sr_ind = NULL
    kolej = NULL

    print("Starting calculation")
    
    cursor = conn.execute("SELECT MAX(data), MAX(godzina) from temperatura")
    for row in cursor:
        koniec = str(int(row[0][0:4]))  + "-" + str(int(row[0][5:7])) + "-" + str(int(row[0][8:12])) + "-" + str(int(row[1][0:2]))
        koniec_dni = datetime.date(int(str(row[0])[0:4]), int(row[0][5:7]), int(row[1][0:2]))
        teraz = NULL

    cursor = conn.execute("SELECT id, godzina, temp_dot, data FROM temperatura WHERE id=1")
    for row in cursor: 
        rok = int(row[3][0:4])
        miesiac = int(row[3][5:7])
        dzien = int(row[3][8:12])
        godzina = int(row[1][0:2])
        chwila = datetime.date(rok, miesiac, dzien)
        minelo_start = (koniec_dni - chwila).days 

    last = NULL

    while koniec != teraz:
        cursor = conn.execute("SELECT id, godzina, temp_dot, data from temperatura")
        for row in cursor:
            teraz = str(rok) + "-" + str(miesiac) + "-" + str(dzien) + "-" + str(godzina)
            wiersz = str(int(row[3][0:4])) + "-" + str(int(row[3][5:7])) + "-" + str(int(row[3][8:12])) + "-" + str(int(row[1][0:2]))

            local_1 = float(str(row[3][5:7] + "." + row[3][8:12]))
            local_2 = float(str(miesiac) + "." + str(dzien))

            if local_1 > local_2:
                break  

            if wiersz == teraz:
                if min > float(row[2]):
                    min = float(row[2])
                if max < float(row[2]):
                    max = float(row[2])
                sr = sr + float(row[2])
                sr_ind = sr_ind + 1
                
                if godzina < 10:
                    days_hour = row[3] + str(" 0" + str(godzina) + ":00:00")
                else:
                    days_hour = row[3] + str(" " + str(godzina) + ":00:00")
      
        godzina = godzina + 1
        
        if days_hour != last:
            #print(days_hour + ", Min = " + str(min) + ", Max = " + str(max) + ", Sr = " + str(sr/sr_ind)[0:5])
            cursor.execute('INSERT INTO STATS VALUES(?, ?, ?, ?);', ((days_hour, str(sr/sr_ind)[0:5], min, max)))
            conn.commit()
            last = days_hour

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

        chwila = datetime.date(rok, miesiac, dzien)
        minelo = (koniec_dni - chwila).days
        procent = str(int((1 - minelo/minelo_start)*100))

        if kolej != chwila:
            print(procent + "%")
            kolej = chwila

    print("Calculation successfully")

def main():
    try:
        global cursor, conn, stan

        hex_def()

        conn = sqlite3.connect(way_1)
        cursor = conn.cursor()
        print("Opened database successfully")

    except:
        print("\n\nCRASH Opened database\n\n")
        raise SystemExit(0) 

    tablica()

    stats_calculator()
    
    conn.commit()
    conn.close()

    if hex_dsk != hex_source:
        shutil.copyfile(way_1, way_2)
    print("Done")    

def file_as_bytes(file):
    with file:
        return file.read()

def hex_def():
    try:
        global hex_source,hex_dsk
    
        print("Dowloading file")
        hex_dsk = (hashlib.md5(file_as_bytes(open(way_1, 'rb'))).hexdigest())
        hex_source = (hashlib.md5(file_as_bytes(open(way_2, 'rb'))).hexdigest()) 
        if hex_dsk != hex_source:
            shutil.copyfile(way_2, way_1)
        print("Downloading succesfully")

    except:
        print("\n\nCRASH dowloading\n\n")
        raise SystemExit(0) 
        
def scanner():
    global stan, way_1, way_2

    stan = int(input("\nPlease enter STAN: \n  0. DEFAULT \n  1. NON DEFAULT\n ="))
    if int(stan) < 0 or int(stan) > 1:
        print("WTF?! \n REPEAT")
        scanner()

    if stan == 0:
        way_1 = "C:/Users/Lenovo/Desktop/VisualStudio/SQL.db"
        way_2 = "Y:/SQL.db"
    elif stan == 1:
        way_1 = input("Please enter destiny\n")
        way_2 = input("Please enter source\n")

    main()

try:
    scanner()

except KeyboardInterrupt:
    print("STOP_KIboard")    