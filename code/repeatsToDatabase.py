import sqlite3
try:
    #conn = sqlite3.connect('../repeats/repeats51.db')
    #conn = sqlite3.connect('../repeats/repeats41.db')
    #conn = sqlite3.connect('../repeats/repeats31.db')
    #conn = sqlite3.connect('../repeats/repeats21.db')
    conn = sqlite3.connect('../repeats/repeats11.db')
    cursor = conn.cursor()
    print("Database created and Successfully Connected to SQLite")

    sqlite_select_Query = "select sqlite_version();"
    cursor.execute(sqlite_select_Query)
    record = cursor.fetchall()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS repeatMap1 (
        SEQUENCE TEXT PRIMARY KEY,
        d INTEGER DEFAULT  0,
        i INTEGER DEFAULT  0,
        o INTEGER DEFAULT  0
        )
        ''')
    with open('../repeats/allMaxRepeats1.txt', 'r') as file:
    #with open('../repeats/allMaxRepeats2.txt', 'r') as file:
    #with open('../repeats/allMaxRepeats3.txt', 'r') as file:
    #with open('../repeats/allMaxRepeats4.txt', 'r') as file:
    #with open('../repeats/allMaxRepeats5.txt', 'r') as file:
        i = 0
        for line in file:
            # Parse the line to extract the necessary fields
            # Adjust the split or parsing method as per your file's format
            #field1, field2, field3 = line.strip().split(',')
            parts = line.strip().split(':')
            key = parts[0].strip()
            values = parts[1].replace('[', '').replace(']', '').split() #.replace('  ', ' ').strip().split(' ')

            i+= 1
            if (i%1000000 == 0):
                print(i/1000000)
            
            cursor.execute('SELECT d, i, o FROM repeatMap1 WHERE SEQUENCE = ?', (key,))
            result = cursor.fetchone()
        
            if result:
                # Record exists, add old and new values
                d_old, i_old, o_old = result
                d_new = d_old + int(values[0])
                i_new = i_old + int(values[1])
                o_new = o_old + int(values[2])
            
                # Update the record
                cursor.execute('''
                UPDATE repeatMap1
                SET d = ?, i = ?, o = ? 
                WHERE SEQUENCE = ?
                ''', (d_new, i_new, o_new, key))
            else:
                # Record does not exist, insert new record
                count = cursor.execute('''
                INSERT INTO repeatMap1 (SEQUENCE, d, i, o) 
                VALUES (?, ?, ?, ?)
                ''', (key, int(values[0]), int(values[1]), int(values[2])))
             #   conn.commit()
            #    print("Record inserted successfully into repeatMap1 table ", cursor.rowcount)

                
    # Commit the changes and close the connection
    conn.commit()
    cursor.close()  # Close the cursor explicitly
    #conn.close()
    
    print("Data has been successfully stored in the SQLite database.")
except sqlite3.Error as error:
    print("Error while connecting to sqlite", error)
finally:
    if conn:
        conn.close()
        print("The SQLite connection is closed")