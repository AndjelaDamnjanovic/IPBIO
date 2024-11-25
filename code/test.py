from typing import List
from Bio import SeqIO
import numpy as np
import json
import sqlite3

def update_rolling_hash(current_hash: int, old_char: str, new_char: str, window_size: int, base: int = 31, mod: int = 10**9 + 9) -> int:

    current_hash = (current_hash - ord(old_char) * pow(base, window_size - 1, mod)) % mod
    current_hash = (current_hash * base + ord(new_char)) % mod
    
    return current_hash if current_hash >= 0 else current_hash + mod

def calculate_initial_hash(s: str, window_size: int, base: int = 31, mod: int = 10**9 + 9) -> int:
    current_hash = 0
    for i in range(window_size):
        current_hash = (current_hash * base + ord(s[i])) % mod
    return current_hash

def extractSequences(testSet):
    try:
        fasta_sequences = SeqIO.parse(open(testSet), 'fasta')
        conn = sqlite3.connect('../sequences/sequences2.db')
        cursor = conn.cursor()
        print("Database created and Successfully Connected to SQLite")

        sqlite_select_Query = "select sqlite_version();"
        cursor.execute(sqlite_select_Query)
        record = cursor.fetchall()

        for fasta in fasta_sequences:
            name, sequence = fasta.id, str(fasta.seq)
            if name == "DP00072":
                continue

            seq_len = len(sequence)
            print(name)
            for n in range(3, seq_len + 1):
                # Compute the initial hash for the first window of size n
                if seq_len >= n:
                    current_hash = calculate_initial_hash(sequence[:n], n)
                    cursor.execute('SELECT d, i, o FROM sequenceMap WHERE SEQUENCE = ?', (current_hash,))
                    records = cursor.fetchall()
                    
                    for row in records:
                        print("d: ", row[0])
                        print("i: ", row[1])
                        print("o: ", row[2])
                        print("\n")
                    

                    # Sliding window with rolling hash
                    for i in range(1, seq_len - n + 1):
                        current_hash = update_rolling_hash(current_hash, sequence[i - 1], sequence[i + n - 1], n)
                        cursor.execute('SELECT d, i, o FROM sequenceMap WHERE SEQUENCE = ?', (current_hash,))
                        records = cursor.fetchall()
                        
                        for row in records:
                            print("d: ", row[0])
                            print("i: ", row[1])
                            print("o: ", row[2])
                            print("\n")
                
        cursor.close()  # Close the cursor explicitly
        print("Data has been successfully stored in the SQLite database.")
    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
    finally:
        if conn:
            conn.close()
        print("The SQLite connection is closed") 

#extractSequences("../testSets/testSet1.fasta")
extractSequences("../sequences/proba.fasta")